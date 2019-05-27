import pickle
from tqdm import tqdm
import os 
import imp

cwd = os.getcwd()
util_path = os.path.join(cwd, 'utils')
print('Loading preprocessed encoded docs, ix2word, and word2freq.')
encoded_docs = pickle.load( open( "encoded_docs.p", "rb" ))
idx2word = pickle.load( open( "idx2word.p", "rb" ))
word2idx = pickle.load( open( "word2idx.p", "rb" ))
word2freq = pickle.load( open( "word_counts.p", "rb" ) )
texts = [[str(j) for j in doc] for i, doc in encoded_docs]
print('Finished loading preprocessed data.')

# Setting parameter
vocab_size = len(idx2word)
emb_dim = 50
batch_size = 50
window_size = 2
num_epoch = 20
initial_lr = 0.025


# Loading word2vec
print('Loading Word2Vec model.')
Word2Vec = imp.load_source('Word2Vec', os.path.join(util_path, 'word2vec/Word2Vec.py'))
print('Word2Vec model loaded.')
model = Word2Vec.model(
	encoded_sentences=texts, 
	idx2word=idx2word, 
	output_file_name='word_vectors', 
	vocab_size = vocab_size, 
	emb_dim = emb_dim, 
	batch_size = batch_size, 
	window_size = window_size,
	num_epoch = num_epoch,
	initial_lr = initial_lr)
# Training model
print('Start training Word2Vec')
model.train()
print('Word2Vec done.')


