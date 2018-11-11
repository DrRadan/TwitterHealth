#  TwitterHealth
<h3>Use NLP approaches to extract features relating to DIET and PHYSICAL ACTIVITY from real-time Twitter stream, and understand their temporal and spatial variation in the US. </h3>


/notebooks/ : the directory for code demo
1. [Week7, Oct29- Nov5]Activity_Classifier_Random_Forest_new.ipynb: uses random forest to predict whether a tweet contains activity or not
2. [Week 3 Oct2-Oct8] Activity_List_General.ipynb: uses website scrapping to obtain a list of activity
3. [Week 1,2 Sep17-Oct2] Activity_List_Specific.ipynb: a more specific list of activity
4. [Week 3 Oct2-Oct8] Food_Nutrient_Report.ipynb: includes how to use USDA API to access food nutrient database and define food health scale indicator
5. [Week 4 Oct8-Oct15] NMF.ipynb: nmf model based on small sample
6. [Week 4 Oct8-Oct15] NMF_Model_2015Data.ipynb: runs NMF model with 5 million tokenized tweets from 2015 to see its performance 
7. [Week 5,6 Oct15 - Oct29] RF_Baseline_for_Food.ipynb: uses random forest to predict whether a tweet contains food or not
8. [Week 1,2 Sep17-Oct2] Raw_Data_Process.ipynb: shows how the data is processed from json fomrat to csv format
9. [Week 1,2 Sep17-Oct2] Raw_Data_Process_new_version.ipynb: New version (add files to the Raw_Data_Process.ipynb version)
10. [Week 1,2 Sep17-Oct2] USDA_foodlist_Basic.ipynb: some data visualization on food nutrient by different category level
11. [Week 5,6 Oct15 - Oct29] key_word_match.ipynb: a demo for key word serach(Aho–Corasick algorithm) and some analysis for the result
12. [Week7, Oct29- Nov5]resample_confidence_interval.ipynb: add resampling confidence interval
13. [Week 3 Oct2-Oct8] statics_analysis.ipynb: shows the statistic analysis in terms of the number and length of tweet, language, emojis, hashtags for different states.
14. [Week4 Oct8-Oct15] tokenization + LDA.ipynb: tokenizes the text tata and runs LDA model at different scenario
15. [Week8, Nov5-Nov11] Run_Statistic.ipynb: Applied the Kolmogorov-Smirnov test to each LDA model and visulization.


/pyhton script/: the code run on HPC
1. [Week 1,2 Sep17-Oct2] process_raw_data.py: the code used to convert original twitter data in json format to csv format for future analysis
2. [Week 3 Oct2-Oct8] filter_en_text.py: the code used to remove all the tweets that are not in english
3. [Week 3 Oct2-Oct8] token_by_spark.py: using spark to do tokenization, stemming, and lemmatization
4. [Week 3 Oct2-Oct8] token_by_whole_file.py: read entire csv file (require a lot of memeory) and then do tokenization, stemming, and lemmatization
5. [Week 3 Oct2-Oct8] token_row_by_row.py: read a csv file row by row, for each row do tokenization, stemming, and lemmatization (require less memeory)
6.[Week 4,5 Oct8-Oct29] key_word_process.py: read a csv file containing tweets and find whether the tweet mentions food or activity key words
7. [Week 4 Oct8-Oct15] Run_LDA.py: run LDA topic modeling with different configurations.
8. [Week7, Oct29- Nov5] Run_LDAwithPlot.py: Loading trained LDA model with different configurations and made plots for each model.
