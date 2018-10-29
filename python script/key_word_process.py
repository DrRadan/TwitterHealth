import ahocorasick
import pickle
import csv

food = pickle.load(open('./store_key_word/food.pickle','rb'))
activity = pickle.load(open('./store_key_word/activity.pickle','rb'))

food_tree = ahocorasick.Automaton()
for index, word in enumerate(food):
    food_tree.add_word(word,word.strip())
food_tree.make_automaton()

activity_tree = ahocorasick.Automaton()
for index, word in enumerate(activity):
    activity_tree.add_word(word,word.strip())
activity_tree.make_automaton()

from_file_name = '/scratch/ql819/Tweets/token_text/small_2014-06.csv'
to_file_name = '/scratch/ql819/Tweets/token_text/small_2014-06_key_word.csv'

fp = open(to_file_name, "a") 
wr = csv.writer(fp, dialect='excel')

with open(from_file_name) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        activity_temp = list(activity_tree.iter(' '+row[1]+' '))
        food_temp = list(food_tree.iter(' '+row[1]+' '))
        if len(activity_temp) > 0:
            activity_str = ','.join([j for i,j in list(activity_temp)])
        else:
            activity_str = ''
        if len(food_temp) > 0:
            food_str = ','.join([j for i,j in list(food_temp)])
        else:
            food_str = ''
            
        target = 0
        if len(food_str) > 0:
            if len(activity_str) >0:
                target = 3
            else:
                target = 1
        elif len(activity_str)>0:
            target = 2
        wr.writerow([row[0], row[1], food_str, activity_str, target])
        
fp.close()


