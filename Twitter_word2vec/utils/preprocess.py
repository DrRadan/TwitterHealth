from collections import Counter
from tqdm import tqdm
import spacy
from spacy.matcher import Matcher
from spacymoji import *

def preprocess(docs, nlp, min_length, min_counts, max_counts, hashtag = True):
    """Tokenize, clean, and encode documents.

    Arguments:
        docs: A list of tuples (index, string), each string is a document.
        nlp: A spaCy object, like nlp = spacy.load('en').
        min_length: An integer, minimum document length.
        min_counts: An integer, minimum count of a word.
        max_counts: An integer, maximum count of a word.
        hashtag: An boolean, whether to tokenize hashtag in the foramt <#word>

    Returns:
        encoded_docs: A list of tuples (index, list), each list is a document
            with words encoded by integer values.
        idx2word: A dict, index -> word.
        word2idx: A dict, word -> index
        word2freq: A dict, counts of words that are in idx2word.
            word2freq[i] is the number of occurrences of word idx2word[i]
            in all documents in docs.
    """
    if hashtag:
            matcher = Matcher(nlp.vocab)
            matcher.add('HASHTAG', None, [{'ORTH': '#'}, {'IS_ASCII': True}])
          
    def clean_and_tokenize(doc, hashtag = True):     
        text = ' '.join(doc.split()) # remove excessive spaces
        text = nlp(text)
        cleaned = []
        if hashtag:
            spans = []
            hashlist = [] # The string-type version of the hashtag tokens
            matches = matcher(text)
            for match_id, start, end in matches:
                spans.append(text[start:end])
            for span in spans:
                span.merge()
                try:
                    hashlist.append(span.text)
                except:
                    pass
            for t in text:
                if t.text in hashlist or t._.is_emoji: # Directly recored the token if it's hashtag or emoji
                    cleaned.append(str(t))
                elif len(t) > 2 and len(t) < 18 and t.is_alpha and not t.is_stop: # Lemmatize plain vocabulary
                    cleaned.append(t.lemma_)
                else:
                    pass
        return cleaned

    tokenized_docs = [(i, clean_and_tokenize(doc, hashtag)) for i, doc in tqdm(docs)]
    
    
    # remove short documents
    n_short_docs = sum(1 for i, doc in tokenized_docs if len(doc) < min_length)
    tokenized_docs = [(i, doc) for i, doc in tokenized_docs if len(doc) >= min_length]
    print('number of removed short documents:', n_short_docs)

    # remove some tokens
    counts = _count_unique_tokens(tokenized_docs)
    tokenized_docs = _remove_tokens(tokenized_docs, counts, min_counts, max_counts)
    n_short_docs = sum(1 for i, doc in tokenized_docs if len(doc) < min_length)
    tokenized_docs = [(i, doc) for i, doc in tokenized_docs if len(doc) >= min_length]
    print('number of additionally removed short documents:', n_short_docs)

    counts = _count_unique_tokens(tokenized_docs)
    encoder, idx2word, word2freq = _create_token_encoder(counts)

    print('\nminimum word count number:', list(word2freq.values())[-1])
    print('this number can be less than MIN_COUNTS because of document removal')

    encoded_docs = _encode(tokenized_docs, encoder)
    word2idx = {y:x for x,y in idx2word.items()}
    
    return encoded_docs, idx2word, word2idx, word2freq


def _count_unique_tokens(tokenized_docs):
    tokens = []
    for i, doc in tokenized_docs:
        tokens += doc
    return Counter(tokens)


def _encode(tokenized_docs, encoder):
    return [(i, [encoder[t] for t in doc]) for i, doc in tokenized_docs]


def _remove_tokens(tokenized_docs, counts, min_counts, max_counts):
    """
    Words with count < min_counts or count > max_counts
    will be removed.
    """
    total_tokens_count = sum(
        count for token, count in counts.most_common()
    )
    print('total number of tokens:', total_tokens_count)

    unknown_tokens_count = sum(
        count for token, count in counts.most_common()
        if count < min_counts or count > max_counts
    )
    print('number of tokens to be removed:', unknown_tokens_count)

    keep = {}
    for token, count in counts.most_common():
        token = str(token)
        if token[0] == '#':
            keep[token] = True
        else:
            keep[token] = count >= min_counts and count <= max_counts

    return [(i, [t for t in doc if keep[t]]) for i, doc in tokenized_docs]


def _create_token_encoder(counts):

    total_tokens_count = sum(
        count for token, count in counts.most_common()
    )
    print('total number of tokens:', total_tokens_count)

    encoder = {}
    idx2word = {}
    word2freq = {}
    i = 0

    for token, count in counts.most_common():
        # counts.most_common() is in decreasing count order
        encoder[token] = i
        idx2word[i] = token
        word2freq[token] = count
        i += 1

    return encoder, idx2word, word2freq
