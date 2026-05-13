# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 20:43:21 2023

@author: khush
"""
#import path
import sys
import pymysql
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

sys.path.append('..')

from KakushIn_Dashboard.password import check_password

st.set_page_config(
    page_title="BulidTogether: Candidate Diversity",
    page_icon= ':a:',
    layout="wide"
)


if check_password():
    
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
    
    df = pd.read_sql('SELECT * FROM CANDIDATE', con=conn)
    df['YEAR'] = pd.DatetimeIndex(df['APPLICATION_DATE']).year
    
    df_departments=pd.read_sql('SELECT * FROM DEPARTMENTS', con=conn)
    
    #%%
    container1=st.container()
    container2=st.container()
    col1, col2 = st.columns(2)
    
    #%%
    
    with st.sidebar:
        #st.success("FILTERS FOR BAR CHART")
        
        star_year, end_year =st.select_slider('Year:', options=sorted(df["YEAR"].unique()),value=(min(df["YEAR"].unique()),max(df["YEAR"].unique()) ))
        
        status=st.multiselect('Hiring Stage:',df['STATUS'].unique(),df['STATUS'].unique())
        
        positions=st.multiselect('Designation:',df['APPLIED_POSITION'].unique(),df['APPLIED_POSITION'].unique())
        
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
    
    df_subset=df.loc[(df['YEAR'] >= star_year) & (df['YEAR'] <= end_year) & (df['STATUS'].isin(status)) & (df['DEPARTMENT_ID'].isin(department_id)) & (df['APPLIED_POSITION'].isin(positions))]
    #df_subset
    
    #%%
    bar_chart= px.histogram(df_subset, x="YEAR", color="GENDER", title="NUMBER OF CANDIDATE BY GENDER OVER THE YEARS", text_auto=True, color_discrete_sequence=px.colors.qualitative.Pastel)
    bar_chart.update_layout(
            xaxis_title_text='Year',
            yaxis_title_text='No of Candidates',
            plot_bgcolor="white",
            bargap=0.3,
            title_x=0.5
        )
    with container1:
        st.plotly_chart(bar_chart, use_container_width=True)
    
    #%%
    
    pie1_subset=df_subset.groupby(['APPLIED_POSITION', 'GENDER']).size().reset_index(name='FREQUENCY')
    
    #pie1_subset
    pie1 = px.sunburst(pie1_subset, path=['APPLIED_POSITION', 'GENDER'], values='FREQUENCY',  color_discrete_sequence=px.colors.qualitative.Pastel, title='GENDER RATIO BY DESIGNATION')
    #pie1.update_layout(title_text='GENDER RATIO BY DESIGNATION',title_x=1)
    pie1.update_traces(textinfo="label+percent parent")
    
    with container2:
    
        with col1:
            st.plotly_chart(pie1,use_container_width=True)
    
    #%%
    
    pie2_subset=df_subset.groupby(['STATUS', 'GENDER']).size().reset_index(name='FREQUENCY')
    
    #pie2_subset
    pie2 = px.sunburst(pie2_subset, path=['STATUS', 'GENDER'], values='FREQUENCY', title="GENDER RATIO BY HIRING STAGE", color_discrete_sequence=px.colors.qualitative.Pastel)
    pie2.update_traces(textinfo="label+percent parent")
    
    with container2:
        with col2:
            st.plotly_chart(pie2, use_container_width=True)
        
    
    
    
    
    # =============================================================================
    # df_subset['STATUS'].value_counts().values
    # 
    # trace1 = go.Pie(
    #     hole=0.5,
    #     #sort=False,
    #     direction='clockwise',
    #     domain={'x': [0.15, 0.85], 'y': [0.15, 0.85]},
    #     values=df_subset['GENDER'].value_counts().values,
    #     labels=df_subset['GENDER'].value_counts().index,
    #     textinfo='label',
    #     textposition='inside',
    #     marker={'line': {'color': 'white', 'width': 1}}
    # )
    # trace2 = go.Pie(
    #     hole=0.7,
    #     #sort=False,
    #     direction='clockwise',
    #     values=df_subset['STATUS'].value_counts().values,
    #     labels=df_subset['STATUS'].value_counts().index,
    #     textinfo='label',
    #     textposition='outside',
    #     marker={'line': {'color': 'white', 'width': 1}}
    # )
    # 
    # fig = go.FigureWidget(data=[trace1, trace2])
    # st.plotly_chart(fig)
    # =============================================================================
    