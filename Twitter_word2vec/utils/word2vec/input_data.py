import numpy
from collections import deque
numpy.random.seed(12345)

class InputData:
    """Store data for word2vec, such as word map, sampling table and so on.
    Attributes:
        word_frequency: Count of each word, used for sampling table
        idx2word: Map from word id to word
        sentence_count: Sentence count in input.
        word_count: Word count in files, without low-frequency words.
    """

    def __init__(self, encoded_sentences, idx2word):
        self.encoded_sentences = encoded_sentences
        self.idx2word = idx2word
        self.get_words()
        self.word_pair_catch = deque()
        self.init_sample_table()
        self.word2idx = {y:x for x,y in self.idx2word.items()}
        print('Word Count: %d' % self.word_count)
        print('Sentence Length: %d' % (self.sentence_length))

    def get_words(self):
        # self.input_file = open(self.input_file_name)
        self.sentence_length = 0
        self.sentence_count = len(self.encoded_sentences)
        wid = 0
        self.word_frequency = dict()
        for sentence in self.encoded_sentences:
            self.sentence_length += len(sentence)
            for w in sentence:
                try:
                    self.word_frequency[w] += 1
                except:
                    self.word_frequency[w] = 1
        self.word_count = len(self.idx2word)

    def init_sample_table(self):
        self.sample_table = []
        sample_table_size = 1e8
        pow_frequency = numpy.array(list(self.word_frequency.values()))**0.75
        words_pow = sum(pow_frequency)
        ratio = pow_frequency / words_pow
        count = numpy.round(ratio * sample_table_size)
        for wid, c in enumerate(count):
            self.sample_table += [wid] * int(c)
        self.sample_table = numpy.array(self.sample_table)

    # @profile
    def get_batch_pairs(self, batch_size, window_size):
        encoded_sentences_clone = self.encoded_sentences.copy()
        while len(self.word_pair_catch) < batch_size:
            word_ids = encoded_sentences_clone[0]
# #             if sentence is None or sentence == '':
# #                 self.input_file = open(self.input_file_name)
# #                 sentence = self.input_file.readline()
#             for idx in sentence:
#                 try:
#                     word_ids.append(idx)
#                 except:
#                     continue
            for i, u in enumerate(word_ids):
                for j, v in enumerate(
                        word_ids[max(i - window_size, 0):i + window_size]):
                    assert int(u) < self.word_count
                    assert int(v) < self.word_count
                    if i == j:
                        continue
                    self.word_pair_catch.append((u, v))
            encoded_sentences_clone.remove(word_ids)
        batch_pairs = []
        for _ in range(batch_size): # Problem: some word pairs might be discarded due to limit of batch_size
            batch_pairs.append(self.word_pair_catch.popleft())
        return batch_pairs

    # @profile
    def get_neg_v_neg_sampling(self, pos_word_pair, count):
        neg_v = numpy.random.choice(
            self.sample_table, size=(len(pos_word_pair), count)).tolist()
        return neg_v

    def evaluate_pair_count(self, window_size):
        return self.sentence_length * (2 * window_size - 1) - (
            self.sentence_count - 1) * (1 + window_size) * window_size