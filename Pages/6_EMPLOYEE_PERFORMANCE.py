# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 23:43:30 2023

@author: khush
"""

import sys
import pymysql
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

sys.path.append('..')

from KakushIn_Dashboard.password import check_password

st.set_page_config(
    page_title="BuildTogether: Candidate Data",
    page_icon= ':a:',
    layout="wide"
)



#%%

if check_password():

#%%

    # database connection
    conn = pymysql.connect(
        host='localhost',
        user='root', 
        password = "Khushi2002",
        db='ALWAYS_FIRST',
        )
    
    #%%
    
    cur = conn.cursor()
    
    #%%
    
    query= "SELECT P.EMPLOYEE_ID,  E.FNAME, E.LNAME, E.GENDER, E.POSITION, D.DEPARTMENT_NAME, E.BUSINESS_UNIT, P.SCORE_YEAR, P.SCORE FROM PERFORMANCE P LEFT JOIN EMPLOYEE E ON P.EMPLOYEE_ID = E.EMPLOYEE_ID LEFT JOIN DEPARTMENTS D ON E.DEPARTMENT_ID =  D.DEPARTMENT_ID"
    
    df= pd.read_sql(query, conn)
    
    
    #%%
    
    with st.sidebar:
        eid=st.text_input("ENTER EMPLOYEE_ID")
        fname=st.text_input("ENTER FIRST NAME")
        lname=st.text_input("ENTER LAST NAME")
        gender=st.multiselect("GENDER:",df['GENDER'].unique(), df['GENDER'].unique())
        departments=st.multiselect('DEPARTMENTS:',df['DEPARTMENT_NAME'].unique(),df['DEPARTMENT_NAME'].unique())
        positions=st.multiselect('DESIGNATION:',df['POSITION'].unique(),df['POSITION'].unique())
        bu=st.multiselect('BUSINESS UNIT:',df['BUSINESS_UNIT'].unique(),df['BUSINESS_UNIT'].unique())
        
        
    #%%
    
    if eid:
        eid=int(eid)
        df_subset=df.loc[(df['EMPLOYEE_ID']==eid)]
    
    else:
        
        #%%
        df_subset=df.loc[(df['DEPARTMENT_NAME'].isin(departments)) & (df['POSITION'].isin(positions)) & (df['GENDER'].isin(gender)) & (df['BUSINESS_UNIT'].isin(bu))]
        
    #%%
        
        if fname:
            df_subset=df_subset.loc[df_subset['FNAME']==fname]
        #%%
            
        if lname:
            df_subset=df_subset.loc[df_subset['LNAME']==lname]
            
    
    #%%
    p_df=np.round(pd.pivot_table(df_subset, values='SCORE', index=['EMPLOYEE_ID', 'FNAME', 'LNAME', 'GENDER', 'POSITION','DEPARTMENT_NAME', 'BUSINESS_UNIT'], columns= ['SCORE_YEAR']))
    p_df = pd.DataFrame(p_df.to_records())
        
    
    container1=st.container()
    
    container1.write('****EMPLOYEE PERFORMANCE****')
    container1.dataframe(p_df)
    
    #%%
    
    line_df= df_subset.groupby(['SCORE_YEAR','GENDER'])['SCORE'].mean().reset_index(name='PERFORMANCE_SCORE')
    
    line_df = pd.DataFrame(line_df)
    
    line = px.line(line_df, x= 'SCORE_YEAR', y= 'PERFORMANCE_SCORE', color='GENDER',title="EMPLOYEE PERFORMANCE GRAPH", color_discrete_sequence=px.colors.qualitative.Pastel, line_group='GENDER')
    
    container2=st.container()
    container2.plotly_chart(line, use_container_width=True)
    
