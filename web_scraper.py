# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 00:03:56 2023

@author: khush
"""

# =============================================================================
# //*[@id="tbl_overall"]/tbody/tr[1]/td[2]/text()
# 
# //*[@id="tbl_overall"]/tbody/tr[73]/td[2]/text()
# 
# 
# //*[@id="tbl_overall"]/tbody/tr[1]/td[2]/div[2]/table/tbody/tr/td[4]
# 
# //*[@id="tbl_overall"]/tbody/tr[5]/td[2]/div[2]/table/tbody/tr/td[4]

# =============================================================================
# //*[@id="tbl_overall"]/tbody/tr[1]/td[2]/div[1]/a[1]
# 
# //*[@id="tbl_overall"]/tbody/tr[6]/td[2]/div[1]/a[1]
# 
# //*[@id="tbl_overall"]/tbody/tr[1]/td[2]/div[1]/a[1]
# =============================================================================
# =============================================================================


import pandas as pd
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import streamlit as st

#%%

@st.cache
def scrape_campus():
    driver = webdriver.Chrome()
    name=[]
    oi=[]
    driver.set_window_position(0,-1000)
    driver.get('https://www.nirfindia.org/2023/OverallRanking.html')
    
    
    for i in range(1,21):
        
        namei = driver.find_element("xpath", '//*[@id="tbl_overall"]/tbody/tr['+str(i)+']/td[2]')
        namet=namei.text
        name.append(namet[:-5])
        
        element= WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH ,'//*[@id="tbl_overall"]/tbody/tr['+str(i)+']/td[2]/div[1]/a[1]')))
        element.click()
        
        WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH ,'//*[@id="tbl_overall"]/tbody/tr['+str(i)+']/td[2]/div[2]/table/tbody/tr/td[4]')))
        
        oii=driver.find_element("xpath", '//*[@id="tbl_overall"]/tbody/tr['+str(i)+']/td[2]/div[2]/table/tbody/tr/td[4]')
        
        oi.append(float(oii.text))
        
    
    data={'SUGGESTED CAMPUS':name,'OI SCORE':oi}
    #print(data)
    
    df=pd.DataFrame(data)
    df.sort_values(by=['OI SCORE'],inplace=True)
    df.reset_index(inplace=True)
    return df

scrape_campus()