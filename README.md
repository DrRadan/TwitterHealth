#  TwitterHealth
<h3>Use NLP approaches to extract features relating to DIET and PHYSICAL ACTIVITY from real-time Twitter stream, and understand their temporal and spatial variation in the US. </h3>


/notebooks/ : the directory for code demo
1. [Week 1,2 Sep17-Oct2] __Activity_List_Specific.ipynb__: a more specific list of activity
2. [Week 1,2 Sep17-Oct2] __Raw_Data_Process.ipynb__: shows how the data is processed from json fomrat to csv format
3. [Week 1,2 Sep17-Oct2] __Raw_Data_Process_new_version.ipynb__: New version (add files to the Raw_Data_Process.ipynb version)
4. [Week 1,2 Sep17-Oct2] __USDA_foodlist_Basic.ipynb__: some data visualization on food nutrient by different category level
5. [Week 3 Oct2-Oct8] __Activity_List_General.ipynb__: uses website scrapping to obtain a list of activity
6. [Week 3 Oct2-Oct8] __Food_Nutrient_Report.ipynb__: includes how to use USDA API to access food nutrient database and define food health scale indicator
7. [Week 3 Oct2-Oct8] __statics_analysis.ipynb__: shows the statistic analysis in terms of the number and length of tweet, language, emojis, hashtags for different states.
8. [Week 4 Oct8-Oct15] __NMF.ipynb__: nmf model based on small sample
9. [Week 4 Oct8-Oct15] __NMF_Model_2015Data.ipynb__: runs NMF model with 5 million tokenized tweets from 2015 to see its performance 
10. [Week4 Oct8-Oct15] __tokenization + LDA.ipynb__: tokenizes the text tata and runs LDA model at different scenario
11. [Week 5,6 Oct15 - Oct29] __RF_Baseline_for_Food.ipynb__: uses random forest to predict whether a tweet contains food or not
12. [Week 5,6 Oct15 - Oct29] __key_word_match.ipynb__: a demo for key word serach(Aho–Corasick algorithm) and some analysis for the result
13. [Week7, Oct29- Nov5]__Activity_Classifier_Random_Forest_new.ipynb__: uses random forest to predict whether a tweet contains activity or not
14. [Week7, Oct29- Nov5]__resample_confidence_interval.ipynb__: add resampling confidence interval
15. [Week8, Nov5-Nov11] __Run_Statistic.ipynb__: Applied the Kolmogorov-Smirnov test to each LDA model and visulization.


/pyhton script/: the code run on HPC
1. [Week 1,2 Sep17-Oct2] __process_raw_data.py__: the code used to convert original twitter data in json format to csv format for future analysis
2. [Week 3 Oct2-Oct8] __filter_en_text.py__: the code used to remove all the tweets that are not in english
3. [Week 3 Oct2-Oct8] __token_by_spark.py__: using spark to do tokenization, stemming, and lemmatization
4. [Week 3 Oct2-Oct8] __token_by_whole_file.py__: read entire csv file (require a lot of memeory) and then do tokenization, stemming, and lemmatization
5. [Week 3 Oct2-Oct8] __token_row_by_row.py__: read a csv file row by row, for each row do tokenization, stemming, and lemmatization (require less memeory)
6.[Week 4,5 Oct8-Oct29] __key_word_process.py__: read a csv file containing tweets and find whether the tweet mentions food or activity key words
7. [Week 4 Oct8-Oct15] __Run_LDA.py__: run LDA topic modeling with different configurations.
8. [Week7, Oct29- Nov5] __Run_LDAwithPlot.py__: Loading trained LDA model with different configurations and made plots for each model.
