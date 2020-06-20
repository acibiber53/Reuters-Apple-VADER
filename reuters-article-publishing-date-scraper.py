# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 01:47:21 2020

@author: acibi
"""

from selenium import webdriver
import pandas as pd
from time import sleep
from progressbar.bar import ProgressBar as PB


def openbrowser():
    options = webdriver.ChromeOptions() 
    options.add_argument("start-maximized")
    
    driver = webdriver.Chrome(options=options)
    sleep(5)  
    
    return driver

def closebrowser(driver):
    driver.quit()

def readdata():
    return pd.read_csv("reuters_data2.csv")

def output(df):
    df = df.drop(columns=['Unnamed: 0','Unnamed: 0.1'])
    df.to_csv(r"reuters_data3.csv",header = True)
    
def get_the_time(driver, link, bar, index):
    driver.get(link)
    element = driver.find_element_by_xpath("/html/body/meta[8]")
    publish_date = element.get_attribute("content")
    bar.update(index)
    sleep(1)
    return publish_date
    
def iterate_urls(driver, df):
    length = len(df['reuters_url'])
    bar = PB(max_value = length).start()
    result = [get_the_time(driver, link, bar, index) for index, link in enumerate(df['reuters_url'])]
    bar.finish()
    return driver, result

def main_function():
    df = readdata()
    try:
        driver = openbrowser()
        driver, result = iterate_urls(driver, df)
        
        df['article_publish_date'] = result
        
        output(df)
    finally:
        closebrowser(driver)

if (__name__== '__main__'):
    main_function()