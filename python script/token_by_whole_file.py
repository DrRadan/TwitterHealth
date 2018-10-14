import spacy
import re
import string
import pandas as pd
from spacy.matcher import Matcher
from spacy.tokens import Token
import csv
import sys

    
    
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


from_csv_list = ['/scratch/ql819/Tweets/refined_data/small_2014-06.csv',
                 '/scratch/ql819/Tweets/refined_data/small_2014-11.csv',
                 '/scratch/ql819/Tweets/refined_data/small_2015-06.csv',
                 '/scratch/ql819/Tweets/refined_data/small_2015-11.csv']

to_csv_list = ['/scratch/ql819/Tweets/token_text/small_2014-06.csv',
                 '/scratch/ql819/Tweets/token_text/small_2014-11.csv',
                 '/scratch/ql819/Tweets/token_text/small_2015-06.csv',
                 '/scratch/ql819/Tweets/token_text/small_2015-11.csv']

index = int(sys.argv[1])

from_csv = from_csv_list[index]
to_csv = to_csv_list[index]
print(from_csv,to_csv)
sys.stdout.flush()

data = pd.read_csv(from_csv,names=['id','text'])

fp = open(to_csv, "a") 
wr = csv.writer(fp, dialect='excel')
   
for index, row in data.iterrows():
    text_id = row['id']
    text = tokenize3(row['text'])
    wr.writerow([text_id, text])

fp.close()