# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 17:09:45 2020

@author: acibi
"""
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as SIA

analyser = SIA()

def readdata():
    return pd.read_csv("reuters_data1.csv")

# Sentiment Analyzer Scores
def sas(sentence, sentiment):
    score = analyser.polarity_scores(sentence)
    return score[sentiment]

def sentiment_lister(sentiment, df):
    trlist = list()
    for sentence in df['processed_header']:
        trlist.append(sas(sentence,sentiment))
    return trlist

def add_sentiments(df):
    df['neg'] = sentiment_lister('neg', df)
    df['neu'] = sentiment_lister('neu', df)
    df['pos'] = sentiment_lister('pos', df)
    df['compound'] = sentiment_lister('compound', df)
    
    return df
    
def output(df):
    df.to_csv(r"reuters_data2.csv",header = True)

def main_function():
    df = readdata()
    df = add_sentiments(df)
    output(df)
    
if (__name__== '__main__'):
    main_function()