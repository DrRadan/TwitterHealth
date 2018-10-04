import pandas as pd
import numpy as np
import re,os,json,pprint
import datetime, sys, emoji, csv

def check_empty_and_unexist_files(file_path_list):
    good_file_path_list = []
    bad_file_path_list = []
    for file_path in file_path_list:
        if os.path.isfile(file_path) and (os.stat(file_path).st_size > 0):
            good_file_path_list.append(file_path)
        else:
            bad_file_path_list.append(file_path)
    if len(bad_file_path_list):
        print('These files are either empty or non-exist: ', bad_file_path_list)
    return good_file_path_list


def load_tweets_from_json(file_path):
    tweets = []
    for line in open(file_path,'r'):
        tweets.append(json.loads(line))
    return tweets


def get_value_by_two_steps(tweet,keys,targets,text):
    original_tweet_text = tweet['text']
    try:
        for key in keys:
            tweet = tweet[key]
    except KeyError:
        return None, text
    if len(tweet):
        if isinstance(targets,str):
            targets = (targets,)
        result = []
        for single_item in tweet:
            single_value = tuple((single_item[temp_target] for temp_target in targets))
            if len(single_value) == 1:
                single_value = single_value[0]
            result.append(single_value)
            
            #remove targets
            indices = single_item['indices']
            target_string = original_tweet_text[indices[0]:indices[1]]
            text = text.replace(target_string,'')
            
            
        if len(result) == 1:
            result = result[0]
        return result,text
    else:
        return None,text
    
def extract_emojis(txt):
    return ''.join(c for c in txt if c in emoji.UNICODE_EMOJI)

def extract_no_emojis_text(txt):
    txt =  ''.join(c for c in txt if c not in emoji.UNICODE_EMOJI)
    return ' '.join(word for word in txt.split() if '@' not in word)  

if __name__ == '__main__':    
    
    dirPath = sys.argv[1]
    file_name_list = os.listdir(dirPath)
    file_name_list = [file_name for file_name in file_name_list if re.findall('.+\.json$',file_name)]
    file_path_list = [dirPath + file_name for file_name in file_name_list]

    file_path_list = check_empty_and_unexist_files(file_path_list)


    fp = open("output_1.csv", "a") 
    wr = csv.writer(fp, dialect='excel')

    header = ['Tweet ID', 'timestamp', 'week', 'user_id', 'state', 'original text', 'with_emoji_text', 'without_emoji_text','in_reply_to_status_id_str',  'emoji',
          'hashtag', 'media(type, url)', 'user_mentions', 'language']

    for file_path in file_path_list:
        print(file_path)
        sys.stdout.flush()
        state_id = file_path.split('/')[-1].split('_')[1]
        tweets = load_tweets_from_json(file_path)
        for tweet in tweets:
            text = tweet['text']
            #print('---------------------------------------------------------')
            #print('original text:',text)
            tweet_id = tweet['id_str']
            user_id = tweet['user']['id']
            language = tweet['lang']
            in_reply_to_status_id_str = tweet.get('in_reply_to_status_id_str',None)
            timestamp = datetime.datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y').timestamp()
            week = datetime.datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y').strftime('%A')
            hashtags,text = get_value_by_two_steps(tweet,['entities','hashtags'],'text',text)
            media,text = get_value_by_two_steps(tweet,['entities','media'],('type','media_url_https'),text)
            symbols,text = get_value_by_two_steps(tweet,['entities','symbols'],'text',text)
            urls,text = get_value_by_two_steps(tweet,['entities','urls'],'url',text)
            user_mentions, text = get_value_by_two_steps(tweet,['entities','user_mentions'],'id_str',text)
            text = re.sub( '\s+', ' ', text ).strip()
            #print(hashtags,media,symbols,urls,user_mentions)
            #print(text)
            list_data = [tweet_id, timestamp, week, user_id, state_id, tweet['text'], text, extract_no_emojis_text(text),in_reply_to_status_id_str,extract_emojis(text),
                            hashtags, media, user_mentions, language]
            wr.writerow(list_data)
            
    fp.close()
