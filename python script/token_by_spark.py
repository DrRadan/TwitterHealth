import pyspark
from pyspark.sql import SQLContext
import spacy
import re
import string
from spacy.matcher import Matcher
from spacy.tokens import Token


sc = pyspark.SparkContext()
ss = SQLContext(sc)


def get_id_and_text(txt_list):
    #print(len(txt_list))
    try:
        text_id, txt = txt_list[0], txt_list[1]
        txt = tokenize3(txt)
    except:
        print(txt)
    return [text_id, txt]
    
    
tokenizer = spacy.load('en_core_web_sm')
whitelist = {'cannot','neither','never',\
 'nevertheless',\
 'no',
 'nobody',
 'none',
 'noone',
 'nor',
 'not',
 'nothing','nowhere','unless'}

def change_stopwords(target_list):
    for word in target_list:
        tokenizer.vocab[word].is_stop = False


def tokenize3(sent):
    try:
        tokens = tokenizer(sent)
        result = []
        for token in tokens:
            if (token.is_punct) or (token.is_stop):
                pass
            elif token.lemma_ ==  '-PRON-':
                result.append(token.text.lower())
            else:
                result.append(token.lemma_)
        target_string = ' '.join(result) 
        return re.sub(r'[^\w\s]', '', target_string)
    except (KeyboardInterrupt, SystemExit):
        raise
    except TypeError: 
        pass


# remove negation from defaults stop words
change_stopwords(whitelist)


read_file = 'try.csv'


data = ss.read.csv('try.csv')
data = data.rdd
data_df = data.map(get_id_and_text).toDF()
data_df.write.csv('mycsv.csv')
