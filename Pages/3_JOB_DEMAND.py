# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 23:34:22 2023

@author: khush
"""
import sys
import pymysql
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
#from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

#from sklearn.preprocessing import PolynomialFeatures


sys.path.append('..')

from KakushIn_Dashboard.password import check_password

#%%
st.set_page_config(
    page_title="BuildTogether: Job Demand",
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
    
    df = pd.read_sql('SELECT * FROM OPEN_ROLES', con=conn)
    df['YEAR'] = pd.DatetimeIndex(df['CREATION_DATE']).year
    
    df_departments=pd.read_sql('SELECT * FROM DEPARTMENTS', con=conn)
    
    emp_df= pd.read_sql("SELECT * FROM EMPLOYEE where status = 'LIVE'", con=conn)
    emp_df['HIRING_YEAR'] = pd.DatetimeIndex(emp_df['HIRING_DATE']).year
    
    #%%
    
    with st.sidebar:
        
        positions=st.multiselect('Designation:',df['POSITION'].unique(),df['POSITION'].unique())
        bu = st.multiselect('Business Unit:',df['BUSINESS_UNIT'].unique(),df['BUSINESS_UNIT'].unique())
        
        departments=st.multiselect('Departments:',df_departments['DEPARTMENT_NAME'].unique(),df_departments['DEPARTMENT_NAME'].unique())
        
    #%%    
        deps=""
        for department in departments:
            if department == departments[-1]:
                deps=deps+"'"+department+"'"
            else:
                deps= deps+"'"+department+"'"+','
        sql= "SELECT DEPARTMENT_ID FROM DEPARTMENTS WHERE DEPARTMENT_NAME IN ("+deps+")"
        
        
        cur.execute(sql)
        department_id=[i[0] for i in cur.fetchall()]
    
        
    #%%
    
    df_subset = df.loc[ (df['BUSINESS_UNIT'].isin(bu)) & (df['DEPARTMENT_ID'].isin(department_id)) & (df['POSITION'].isin(positions))]
    
    emp_df_subset = emp_df.loc[ (emp_df['BUSINESS_UNIT'].isin(bu)) & (emp_df['DEPARTMENT_ID'].isin(department_id)) & (emp_df['POSITION'].isin(positions))]
    
  
    #%%
    
    col1,col2 = st.columns(2)
    
    #%%
    
    linregress_df = df_subset.groupby('YEAR').size().reset_index(name='NO. OF AVAILABLE JOBS')
    
    #linregress_df
    
    #%%
    
    year=col1.text_input("ENTER YEAR",value='2024')
    
    #%%
    
    # Linear Regression
    
    with col1:
        
        try:
    
            best_fit=px.scatter(linregress_df, x='YEAR', y= 'NO. OF AVAILABLE JOBS', trendline='ols', title="DEMAND PREDICTION", color_discrete_sequence=px.colors.qualitative.Pastel)
            
            best_fit.update_layout(yaxis_range=[0,40])
            
            st.plotly_chart(best_fit, use_container_width=True)
            
            x=linregress_df["YEAR"]
            
            y=linregress_df["NO. OF AVAILABLE JOBS"]
            
        
            
            x=np.array([x])
            y=np.array([y])
            
            
            x=x.reshape(-1,1)
            y=y.reshape(-1,1)
            
            model= LinearRegression()
            model.fit(x,y)
            
            predict_year=np.array([int(year)])
            predict_year=predict_year.reshape(-1,1)
            prediction=model.predict(predict_year)
            
            
            
            if prediction[0][0]%1 > 0.5:
                predicted_jobs= int(prediction[0][0])+1
            else:
                predicted_jobs= int(prediction[0][0])
            #st.write("training score:",training_score," testing score:",testing_score)
            
            st.write("PREDICTED JOB DEMAND IN",year,"IS",str(predicted_jobs),"JOB(S)")
        except:
            st.write("FOR THE CHOSEN PARAMETERS THERE ARE NO VALUES IN DATABASE THUS PREDICTION CANNOT BE MADE")
    
    #%%
    #emp_df_subset2 = emp_df_subset.loc[emp_df_subset['STATUS']=='LIVE']
    pie_df = emp_df_subset.groupby('GENDER').size().reset_index(name='FREQUENCY')
    with col2:
        jobs_entered=st.text_input("ENTER AVAILABLE JOBS")
        st.write("TARGET GENDER RATIO IS 50:50 MALE : FEMALE")
        
        
        pie = px.pie(pie_df, values='FREQUENCY', names='GENDER', title='GENDER RATIO OF CURRENT EMPLOYEES', color_discrete_sequence=px.colors.qualitative.Pastel)
            
        st.plotly_chart(pie, use_container_width=True)
    
    try:
        num_men=int(pie_df['FREQUENCY'].loc[pie_df['GENDER']=='M'])
    except:
        num_men=0
    try:
        num_women=int(pie_df['FREQUENCY'].loc[pie_df['GENDER']=='F'])
    except:
        num_women=0
    
    
    
    
    
    try:
        if jobs_entered:
            jobs=int(jobs_entered)
        else:
            jobs=int(predicted_jobs)
        
        #%%
        
        if num_men > num_women:      
            rw=num_men-num_women
            if rw < jobs:
                extra=jobs-rw
                rm=extra/2
                rw=rw+(extra/2)
            else:
                rm=0
                rw=jobs
        elif num_men < num_women:
            rm = num_women-num_men
            if rm < jobs:
                extra=jobs-rm
                rw=extra/2
                rm=rm+(extra/2)
            else:
                rw=0
                rm=jobs
        else:
            rm=jobs/2
            rw=jobs/2
        if rw%1 !=0:
            rw=int(rw)+1
            rm=int(rm)
        
        new_percent_w=((num_women+rw)*100)/(num_women+rw+num_men+rm)
        new_percent_m=((num_men+rm)*100)/(num_women+rw+num_men+rm)
            
            
            
        
        #%%
        with col2:
# =============================================================================
#             st.write("TARGET GENDER RATIO IS 50:50 MALE : FEMALE")
#             
#             pie = px.pie(pie_df, values='FREQUENCY', names='GENDER', title='GENDER RATIO OF CURRENT EMPLOYEES', color_discrete_sequence=px.colors.qualitative.Pastel)
#                 
#             st.plotly_chart(pie, use_container_width=True)
# =============================================================================
            
            st.write("OUT OF",str(jobs),"JOBS IN YEAR",str(year),str(rw),"JOBS SHOULD BE FILLED BY WOMEN AND",str(rm),"JOBS SHOULD BE FILLED BY MEN TO ACHIEVE BEST GENDER RATIO")
            st.write("IF FOLLOWED, THE NEW GENDER RATIO WILL BE",str(round(new_percent_m,2)),":",str(round(new_percent_w,2)),"MALE : FEMALE")
            
    except:
        col2.write("FOR THE CHOSEN PARAMETERS THERE ARE NO VALUES IN DATABASE THUS PREDICTION CANNOT BE MADE")
    
# =============================================================================
#     bar_df = emp_df_subset.groupby(['HIRING_YEAR','GENDER']).size().reset_index(name='NO OF EMPLOYEES')
#     bar = px.bar(bar_df, x='HIRING_YEAR', y='NO OF EMPLOYEES', title = 'GENDER RATIO OF EMPLOYEES OVER THE YEARS', color='GENDER', barmode = 'group')
#     st.plotly_chart(bar, use_container_width = True)
# =============================================================================
    


# =============================================================================
#     X_train, X_test, Y_train, Y_test = train_test_split(
#     x,y, random_state=0,test_size=0.25)
#     
#     X_train=np.array([X_train])
#     Y_train=np.array([Y_train])
#     X_test=np.array([X_test])
#     Y_test=np.array([Y_test])
#     
#     X_train=X_train.reshape(-1,1)
#     Y_train=Y_train.reshape(-1,1)
#     X_test=X_test.reshape(-1,1)
#     Y_test=Y_test.reshape(-1,1)
#     
#     model= LinearRegression()
#     model.fit(X_train,Y_train)
#     training_score=model.score(X_train, Y_train)
#     testing_score=model.score(X_test, Y_test)
# =============================================================================