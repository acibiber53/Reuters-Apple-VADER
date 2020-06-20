# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 23:54:39 2020

@author: acibi
"""

from selenium import webdriver
from time import sleep
import pandas as pd
import re


def openbrowser():
    url='https://www.reuters.com/companies/AAPL.OQ/news'
    
    options = webdriver.ChromeOptions() 
    options.add_argument("start-maximized")
    
    driver = webdriver.Chrome(options=options)
    
    driver.get(url)
    sleep(5)  
    
    return driver

def closebrowser(driver):
    driver.quit()

def scrolldown(driver):
    print("Started Scrolling Down!")
    SCROLL_PAUSE_TIME = 3
    tmp = 0
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait to load page
        sleep(SCROLL_PAUSE_TIME)
        articles = driver.find_elements_by_class_name("TextLabel__text-label___3oCVw.TextLabel__black-to-orange___23uc0.TextLabel__medium___t9PWg.MarketStoryItem-headline-2cgfz")
        article_count = len(articles)
        
        if tmp == article_count:
            print(article_count)
            break
        
        if article_count > 2000:
            break
        tmp = article_count
    print("Finished Scrolling Down!")
    return driver, articles

def apd_calc(driver):
    dates = driver.find_elements_by_class_name("TextLabel__text-label___3oCVw.TextLabel__gray___1V4fk.TextLabel__regular___2X0ym.MarketStoryItem-date-H-tta")
    l = [elem.text for elem in dates]
    return l

def process_headers(col):
    print("Started Processsing!")
    exclusion_words = ['MEDIA-', 'BRIEF-', 'FACTBOX-', 'US STOCKS SNAPSHOT-', 
                   'US STOCKS-', 'CORRECTED-US STOCKS-', 'RPT-', 'REFILE-', 
                   'CORRECTED \(OFFICIAL\)-', 'IN BRIEF: ', 'GLOBAL MARKETS-', 
                   'EMERGING MARKETS-', 'PRECIOUS-', 'METALS-', 'DAVOS-',
                   'CORRECTED-UPDATE 1-', 'CORRECTED-', 'UPDATE 1-','BUZZ-U.S. STOCKS ON THE MOVE-',
                   'UPDATE 2-', 'Breakingviews - ', 'Factbox: ', 'Explainer: ',
                   'BUZZ-IQE: ', 'RPT-EXPLAINER-', 'Exclusive: ', 'UPDATE 5-',
                   'REFILE-UPDATE 1-', 'FOCUS-', 'CORRECTED-UPDATE 2-', 'FOREX-',
                   'CORRECTED-UPDATE 5-', 'BUZZ-', 'LIVE MARKETS-', 'INSTANT VIEW 2-',
                   'GRAPHIC-', 'RPT-GRAPHIC-', 'WITHDRAWAL: ', 'CANADA STOCKS-']
    
    exclusions = '|'.join(exclusion_words)
    for index, elem in enumerate(col):
        col[index] = re.sub(exclusions, '', elem)
    print("Finished Processing!")
    return col
    
def dfing(driver, articles):
    print("Transformation to DataFrame Initiated!")
    
    df = pd.DataFrame([article.text for article in articles], columns = ['raw_header'])
    df['reuters_url'] = [article.get_attribute('href') for article in articles]
    df['article_publish_date'] = apd_calc(driver)
    df['processed_header'] = process_headers(df['raw_header'].copy())
    
    print("Transformation has ended!")
    return df
    
def output(df):
    df.to_csv(r"reuters_data1.csv",header = True)
    
def main_function():
    try:
        driver = openbrowser()
        
        driver, articles = scrolldown(driver)
        
        df = dfing(driver, articles)
        
        output(df)
        
    finally:    
        closebrowser(driver)
    
    

if (__name__== '__main__'):
    main_function()