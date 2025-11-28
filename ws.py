# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 23:03:05 2023

@author: khush
"""

import requests
import lxml.html
import pandas as pd
import streamlit as st

@st.cache
def scrape_campus():

    url = 'https://www.nirfindia.org/2023/OverallRanking.html'
    
    response = requests.get(url)
    content = response.content
    
    print(response.status_code)
    
    html = lxml.html.fromstring(content)
    
    names = []
    ois = []
    
    for i in range(1,21):
        name = html.xpath('//*[@id ="tbl_overall"]/tbody/tr['+str(i)+']/td[2]/text()')
        oi = html.xpath('//*[@id ="tbl_overall"]/tbody/tr['+str(i)+']/td[2]/div[2]/table/tbody/tr/td[4]//text()')
        names.append(name[0])
        ois.append(float(oi[0]))
    d ={'SUGGESTED CAMPUS': names, 'OI SCORE':ois}
    
    # =============================================================================
    # print(d)
    # print(len(names),len(ois))
    # =============================================================================
    df = pd.DataFrame(d)
    
    
    df.sort_values(by=['OI SCORE'],inplace=True)
    df.reset_index(inplace=True)
    
    return df

# =============================================================================
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
# 
# url = 'https://www.google.com/localservices/prolist?g2lbs=AP8S6EN9BaPZYxzDZw61nkr-s2Ic_p3_shcjqmRjc87eDW6PhXKYdNy4Dc_-kqqS-zTUkkrokokz97o62DnBd_cQDzQC9dF1KkjH8sjhWGmqwO5-8L3JjO4tv164z4uhAF5k8biAiTKlFpFkCaST2xSuyecz2njVOA%3D%3D&hl=en-IN&gl=in&cs=1&ssta=1&q=recruitment%20agencies&oq=recruitment%20agencies&slp=MgA6HENoTUkwN1BRdGFfLV93SVZJTTBXQlIwS1hRYWtSAggCYACSAaICCg0vZy8xMWcwamI2OG5oCgsvZy8xdmQ5M2s4awoML2cvMWhjNWp4OWhuCgsvZy8xdGhyNW41NwoLL2cvMXRodGJsc2sKDS9nLzExYzFuajZnc20KDS9nLzExY3A3ZHdyeXIKCy9nLzF0ZDY4YmNtCgsvZy8xdnpuNDBmdgoLL2cvMXRnZjFwaGIKCy9nLzF0a2MwbDNiCgwvZy8xcHAydHozeDEKCy9nLzF0Y3ZtcjloCg0vZy8xMWdqMHQxNzljCgwvZy8xcHAyeDd2MTEKDS9nLzExajBieWh2emgKDS9nLzExZjhsbnF6MXIKDC9nLzEycTR3Z24wagoLL2cvMXRxY2pwYzEKDS9nLzExZGR4bGt3cDkSBBICCAESBAoCCAGaAQYKAhcZEAA%3D&src=2&serdesk=1&sa=X&ved=2ahUKEwjL5Ma1r_7_AhXqgVYBHbC4BqkQjGp6BAhCEAE&scp=ChZnY2lkOmVtcGxveW1lbnRfYWdlbmN5El4SEgkfYbG2H8jnOxHzoN9r2z4LfBoSCVP0JkRfzuc7Ed59jQL2WRGWIhxNdW1iYWkgU3VidXJiYW4sIE1haGFyYXNodHJhKhQNHfNPCxXvq2ArHSBPfAslXAmAKzABGhRyZWNydWl0bWVudCBhZ2VuY2llcyIUcmVjcnVpdG1lbnQgYWdlbmNpZXMqCkpvYiBDZW50cmU%3D'
# 
# # =============================================================================
# response = requests.get(url, headers=headers)
# content = response.content
# # 
# print(response.status_code)
# # 
# html = lxml.html.fromstring(content)
# # =============================================================================
# 
# # =============================================================================
# # parser = lxml.etree.HTMLParser(encoding='utf-8')
# # html = lxml.etree.parse(url, parser)
# # =============================================================================
# 
# # =============================================================================
# # #names
# # /html/body/div[4]/div/div[1]/div[6]/div/div[2]/div[1]/div[1]/div[2]/h3/a
# # /html/body/div[4]/div/div[1]/div[6]/div/div[3]/div[1]/div[1]/div[2]/h3/a
# # 
# # #rating
# # /html/body/div[4]/div/div[1]/div[6]/div/div[2]/div[1]/div[1]/div[2]/div/span[1]/span/span[1]
# # /html/body/div[4]/div/div[1]/div[6]/div/div[3]/div[1]/div[1]/div[2]/div/span[1]/span/span[1]
# # 
# # # review
# # /html/body/div[4]/div/div[1]/div[6]/div/div[2]/div[1]/div[1]/div[2]/div/a
# # /html/body/div[4]/div/div[1]/div[6]/div/div[3]/div[1]/div[1]/div[2]/div/a
# # =============================================================================
# 
# names = []
# ratings = []
# reviews = []
# 
# name = html.xpath('//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div[1]/div[3]/div[3]/c-wiz/div/div/div[1]/c-wiz/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div/text()')
# 
# 
# print(name[0])
# 
# # =============================================================================
# # for i in range(1,22):
# #     try:
# #         name= html.xpath('/html/body/div[4]/div/div[1]/div[6]/div/div['+str(i)+']/div[1]/div[1]/div[2]/h3/a')
# #         rating=html.xpath('//html/body/div[4]/div/div[1]/div[6]/div/div['+str(i)+']/div[1]/div[1]/div[2]/div/span[1]/span/span[1]')
# #         review=html.xpath('/html/body/div[4]/div/div[1]/div[6]/div/div['+str(i)+']/div[1]/div[1]/div[2]/div/a')
# #         print(name)
# #         print(rating)
# #         print(review)
# #     except:
# #         pass
# # =============================================================================
# =============================================================================

@st.cache
def scrape_vendor():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    url = 'https://www.google.com/localservices/prolist?g2lbs=AP8S6EN9BaPZYxzDZw61nkr-s2Ic_p3_shcjqmRjc87eDW6PhXKYdNy4Dc_-kqqS-zTUkkrokokz97o62DnBd_cQDzQC9dF1KkjH8sjhWGmqwO5-8L3JjO4tv164z4uhAF5k8biAiTKlFpFkCaST2xSuyecz2njVOA%3D%3D&hl=en-IN&gl=in&cs=1&ssta=1&q=recruitment%20agencies&oq=recruitment%20agencies&slp=MgA6HENoTUkwN1BRdGFfLV93SVZJTTBXQlIwS1hRYWtSAggCYACSAaICCg0vZy8xMWcwamI2OG5oCgsvZy8xdmQ5M2s4awoML2cvMWhjNWp4OWhuCgsvZy8xdGhyNW41NwoLL2cvMXRodGJsc2sKDS9nLzExYzFuajZnc20KDS9nLzExY3A3ZHdyeXIKCy9nLzF0ZDY4YmNtCgsvZy8xdnpuNDBmdgoLL2cvMXRnZjFwaGIKCy9nLzF0a2MwbDNiCgwvZy8xcHAydHozeDEKCy9nLzF0Y3ZtcjloCg0vZy8xMWdqMHQxNzljCgwvZy8xcHAyeDd2MTEKDS9nLzExajBieWh2emgKDS9nLzExZjhsbnF6MXIKDC9nLzEycTR3Z24wagoLL2cvMXRxY2pwYzEKDS9nLzExZGR4bGt3cDkSBBICCAESBAoCCAGaAQYKAhcZEAA%3D&src=2&serdesk=1&sa=X&ved=2ahUKEwjL5Ma1r_7_AhXqgVYBHbC4BqkQjGp6BAhCEAE&scp=ChZnY2lkOmVtcGxveW1lbnRfYWdlbmN5El4SEgkfYbG2H8jnOxHzoN9r2z4LfBoSCVP0JkRfzuc7Ed59jQL2WRGWIhxNdW1iYWkgU3VidXJiYW4sIE1haGFyYXNodHJhKhQNHfNPCxXvq2ArHSBPfAslXAmAKzABGhRyZWNydWl0bWVudCBhZ2VuY2llcyIUcmVjcnVpdG1lbnQgYWdlbmNpZXMqCkpvYiBDZW50cmU%3D'

    response = requests.get(url, headers=headers)
    content = response.content

    # print(response.status_code)

    html = lxml.html.fromstring(content)

    names = []
    ratings = []
    reviews = []
    name = html.xpath(
        '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div[1]/div[3]/div[3]/c-wiz/div/div/div[1]/c-wiz/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div/text()')
    review = html.xpath(
        '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div[1]/div[3]/div[3]/c-wiz/div/div/div[1]/c-wiz/div/div[1]/div[1]/div/div/div/div[2]/div[2]/div/div[2]/text()')
    #
    # print(name[0])
    # print(review[0])
    # rating = html.xpath('//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div[1]/div[3]/div[3]/c-wiz/div/div/div[1]/c-wiz/div/div[1]/div[1]/div/div/div/div[2]/div[2]/div/div[1]/div[1]/text()')
    # print(rating[0])
    for i in range(1, 40, 2):
        if i == 13:
            pass
        else:
            name = html.xpath(
                '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div[1]/div[3]/div[3]/c-wiz/div/div/div[1]/c-wiz/div/div[' + str(
                    i) + ']/div[1]/div/div/div/div[2]/div[1]/div/text()')
            names.append(name[0])
            review = html.xpath(
                '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div[1]/div[3]/div[3]/c-wiz/div/div/div[1]/c-wiz/div/div[' + str(
                    i) + ']/div[1]/div/div/div/div[2]/div[2]/div/div[2]/text()')
            reviews.append(review[0][1:-1])
            rating = html.xpath(
                '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div[1]/div[3]/div[3]/c-wiz/div/div/div[1]/c-wiz/div/div[' + str(
                    i) + ']/div[1]/div/div/div/div[2]/div[2]/div/div[1]/div[1]/text()')
            ratings.append(rating[0])

    d = {"NAME OF VENDOR": names, "RATING": ratings, "REVIEW": reviews}
    df = pd.DataFrame(d)
    # Sort the DataFrame by 'rating' and 'reviews' in descending order
    sorted_df = df.sort_values(by=['RATING', 'REVIEW'], ascending=[False, False])
    return sorted_df
#scrape_vendor()
