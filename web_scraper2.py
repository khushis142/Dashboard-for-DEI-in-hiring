# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 23:00:58 2023

@author: khush
"""

import pandas as pd
import streamlit as st
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


@st.cache
def scrape_vendor():
    driver = webdriver.Chrome()
    driver.set_window_position(0,-1000)
    driver.get('https://vendordirectory.shrm.org/category/recruitment')
    final =[]
    for i in range(1,4):
        names = driver.find_element(By.XPATH,
                                    '/html[1]/body[1]/div[4]/div[1]/div[1]/div[4]/div[1]/div[' + str(i) + ']/div[1]/h3[1]/a[1]')
        i = i + 1
        final.append(names.text)
    
    for i in range(1,3):
        names = driver.find_element(By.XPATH,
                                    '/html[1]/body[1]/div[4]/div[1]/div[1]/div[5]/div[1]/div[' + str(i) + ']/div[1]/h3[1]/a[1]')
        i = i + 1
        final.append(names.text)
    # print(final)
    Rank = [1,2,3,4,5]
    df = pd.DataFrame(list(zip(Rank, final)),
                   columns =['Rank', 'NAME OF VENDOR'])
    return df