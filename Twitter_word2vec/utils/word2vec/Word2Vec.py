import numpy
from torch.autograd import Variable
import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm
import sys
import imp
import os

cwd = os.getcwd()
InputData_module = imp.load_source('InputData', os.path.join(cwd, 'utils/word2vec/input_data.py'))
InputData = InputData_module.InputData

SkipGramModel_module = imp.load_source('SkipGramModel', os.path.join(cwd, 'utils/word2vec/skip_gram.py'))
SkipGramModel = SkipGramModel_module.SkipGramModel

class model:
    def __init__(self,
                 encoded_sentences,
                 idx2word,
                 output_file_name,
                 vocab_size,
                 emb_dim=100,
                 batch_size=1024,
                 window_size=2,
                 num_epoch=20,
                 initial_lr=0.025):
        """Initilize class parameters.
        Args:
            encoded_sentences: list of idx_encoded documents.
            output_file_name: Name of the final embedding file.
            emb_dim: Embedding dimention, typically from 50 to 500.
            batch_size: The count of word pairs for one forward.
            window_size: Max skip length between words.
            iteration: Control the multiple training iterations.
            initial_lr: Initial learning rate.
        Returns:
            None.
        """
        self.data = InputData(encoded_sentences, idx2word)
        self.output_file_name = output_file_name
        self.vocab_size = vocab_size
        self.emb_dim = emb_dim
        self.batch_size = batch_size
        self.window_size = window_size
        self.num_epoch = num_epoch
        self.initial_lr = initial_lr
        self.skip_gram_model = SkipGramModel(self.vocab_size, self.emb_dim)
        self.use_cuda = torch.cuda.is_available()
        print('Using GPU: {}'.format(self.use_cuda))
        if self.use_cuda:
            self.skip_gram_model.cuda()
        self.optimizer = optim.SGD(
            self.skip_gram_model.parameters(), lr=self.initial_lr)
        self.word_vectors = dict()
    
    def train(self):
        """Multiple training.
        Returns:
            None.
        """
        pair_count = self.data.evaluate_pair_count(self.window_size)
        batch_count = self.num_epoch * pair_count / self.batch_size
        process_bar = tqdm(range(int(batch_count)))
        print('Using GPU: {}'.format(self.use_cuda))
        for i in process_bar:
            pos_pairs = self.data.get_batch_pairs(self.batch_size,
                                                  self.window_size)
            neg_v = self.data.get_neg_v_neg_sampling(pos_pairs, 5)
            pos_u = [pair[0] for pair in pos_pairs]
            pos_v = [pair[1] for pair in pos_pairs]
            pos_u = Variable(torch.LongTensor(list(map(int, pos_u))))
            pos_v = Variable(torch.LongTensor(list(map(int, pos_v))))
            neg_v = Variable(torch.LongTensor(neg_v))
            if self.use_cuda:
                pos_u = pos_u.cuda()
                pos_v = pos_v.cuda()
                neg_v = neg_v.cuda()

            self.optimizer.zero_grad()
            loss = self.skip_gram_model.forward(pos_u, pos_v, neg_v)
            loss.backward()
            self.optimizer.step()

            process_bar.set_description("Loss: %0.8f, lr: %0.6f" %
                                        (loss.item(),
                                         self.optimizer.param_groups[0]['lr']))
            if i * self.batch_size % 100000 == 0:
                lr = self.initial_lr * (1.0 - 1.0 * i / batch_count)
                for param_group in self.optimizer.param_groups:
                    param_group['lr'] = lr
        self.word_vectors = self.skip_gram_model.get_embedding(
            self.data.idx2word, self.output_file_name, self.use_cuda)