#!/usr/bin/env python3

import pandas as pd
import numpy as np
import os.path
from sklearn.feature_extraction.text import CountVectorizer
import pickle as pkl
from time import time
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.model_selection import ParameterGrid
from random import sample


def Prepare_corpus(dataset,text):
    for i in dataset['1']:
        try:
            ### Remove sentence length> 4
            if len(i.split(" ")) > 4:
                text.append(i)
        except AttributeError:
            continue
    return text

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()
    
    
def LDA(corpus,n_topics,max_features,max_df,min_df,n_top_words):
    
    if os.path.isfile("saved_model/tfVectorizer_topics={}_maxFeatures={}_maxDf={}_minDf={}.pickle"
                      .format(n_topics,max_features,max_df,min_df)):
        tf_vectorizer = pkl.load(open("saved_model/tfVectorizer_topics={}_maxFeatures={}_maxDf={}_minDf={}.pickle"
                 .format(n_topics,max_features,max_df,min_df), "rb"))
        tf = tf_vectorizer.transform(corpus)
    else:
        tf_vectorizer = CountVectorizer(max_df=max_df, min_df=min_df, 
                                        max_features=max_features,token_pattern = r"(?u)\b[A-Za-z0-9]{3,}\b")
        tf = tf_vectorizer.fit_transform(corpus)
        pkl.dump(tf_vectorizer, open("saved_model/tfVectorizer_topics={}_maxFeatures={}_maxDf={}_minDf={}.pickle"
                                     .format(n_topics,max_features,max_df,min_df), "wb"))
    
    
    n_samples = len(corpus)
    print("Fitting LDA models with tf features, n_samples=%d and n_features=%d..."
       % (n_samples, max_features))
    lda = LatentDirichletAllocation(n_components=n_topics,
                                 learning_method='online', learning_offset=50.,
                                 random_state=0,max_iter =5,verbose = 1)
    lda.fit(tf)
    pkl.dump(lda, open("saved_model/LDA_topics={}_maxFeatures={}_maxDf={}_minDf={}.pickle"
                                 .format(n_topics,max_features,max_df,min_df), "wb"))

    print("\nTopics in LDA model:")
    tf_feature_names = tf_vectorizer.get_feature_names()
    print_top_words(lda, tf_feature_names, n_top_words)



def tuning(corpus,grid,n_top_words):
    
    num_comb = len(ParameterGrid(grid))
    count = 0

    for j in range(len(ParameterGrid(grid))):
        count += 1
        print("Now it is {} out of {} combinations".format(count, num_comb))
        n_topics,min_df,max_features,max_df = ParameterGrid(grid)[j].values()
        myCsvRow = "n_topics = {} max_features = {} max_df = {} min_df = {}".format(n_topics,max_features,max_df,min_df)
        print(myCsvRow)
        LDA(corpus,n_topics,max_features,max_df,min_df,n_top_words)
        print("Done\n")


if __name__ == '__main__':
    data201506 = pd.read_csv("data/small_2015-06_key_word.csv",index_col=False, header=None)
    data201511 = pd.read_csv("data/small_2015-11_key_word.csv",index_col=False, header=None)
    data201506.columns = np.array([str(i) for i in data201506.columns.values])
    data201511.columns = np.array([str(i) for i in data201511.columns.values])
    corpus = Prepare_corpus(data201506,[])
    corpus = Prepare_corpus(data201511,corpus)
    ### randomly sample 1000000 out of the original size
    # corpus = sample(corpus,1000000)
    
    
    grid = {'n_topics':[75],
           'max_features':[16000],
           'max_df':[0.5,0.6],
           'min_df':[100]}
    n_top_words = 25
    tuning(corpus,grid,n_top_words)
