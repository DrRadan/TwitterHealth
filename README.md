#  TwitterHealth


/notebooks/ : the directory for code demo
1. Raw_Data_Process.ipynb: show how the data is processed from json fomrat to csv format
2. statics_analysis.ipynb: show the statistic analysis in terms of the number and length of tweet, language, emojis, hashtags for different states.
3.
4.


/pyhton script/: the code run on HPC
1. process_raw_data.py: the code used to convert original twitter data in json format to csv format for future analysis
2. filter_en_tezt.py: the code used to remove all the tweets that are not in english
3. token_by_spark.py: using spark to do tokenization, stemming, and lemmatization
4. token_by_whole_file.py: read entire csv file (require a lot of memeory) and then do tokenization, stemming, and lemmatization
5. token_row_by_row.py: read a csv file row by row, for each row do tokenization, stemming, and lemmatization (require less memeory)
