To be able to run the files in this directory you should already have the datasets of old tweets and locations.

we'll walk through each file here.
1.Streaming.py
    To run this file you should have a Twitter developer account.

2.old_tweets_collecting.py
    To run this file you should have the old tweets datasets in the "Old Datasets" directory.

3.FoldersGenerator.py
    To run this file you should already have "json_old_tweets.json" in the same directory or run "Streaming.py" or "old_tweets_collecting.py"         before.

4.Total_countries_sentiment.py
    To run this file you should run "FoldersGenerator.py" first.
    
5.Country_sentiment_perweek.py
    To run this file you should run "FoldersGenerator.py" first.
    
6.Countries_Time_Series.py
    To run this file you should run "Country_sentiment_perweek.py" first.
    
7.World Time Series.py
    To run this file you should run "old_tweets_collecting.py" first.
    
8.User_location_handling_1.ipynb and User_location_handling_2.ipynb.
    Those files created to genereate a suitable dataset to use in the pervious files, you can avoid runing them if you download the whole files,
    because they did their job once they run in the first time.
    
Thank You