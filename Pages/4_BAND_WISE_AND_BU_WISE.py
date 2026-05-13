# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 12:45:41 2023

@author: khush
"""

import sys
import pymysql
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

from sklearn.preprocessing import PolynomialFeatures
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from itertools import cycle


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
    #%%
    
    df2 = pd.read_sql('SELECT * FROM CANDIDATE', con=conn)
    df2['YEAR'] = pd.DatetimeIndex(df2['APPLICATION_DATE']).year
    
    #%%
    
    with st.sidebar:
        star_year, end_year =st.select_slider('Year:', options=sorted(df["YEAR"].unique()),value=(min(df["YEAR"].unique()),max(df["YEAR"].unique()) ))
        positions=st.multiselect('Designation:',df['POSITION'].unique(),df['POSITION'].unique())
        
    #%%
    
    df_subset=df.loc[(df['YEAR'] >= star_year) & (df['YEAR'] <= end_year) & (df['POSITION'].isin(positions))]
    
    df2_subset=df2.loc[(df2['YEAR'] >= star_year) & (df2['YEAR'] <= end_year) & (df2['APPLIED_POSITION'].isin(positions))]
    
    #%%
    
    container1=st.container()
    
    df_bar= df_subset.groupby(['YEAR', 'BUSINESS_UNIT']).size().reset_index(name='NO. OF AVAILABLE JOBS')
    
    bar_chart= px.bar(df_bar,x='YEAR', y='NO. OF AVAILABLE JOBS',color='BUSINESS_UNIT', barmode='group', title='BU WISE JOB DEMAND OVER THE YEARS',color_discrete_sequence=px.colors.qualitative.Pastel)
    
    with container1:
        st.plotly_chart(bar_chart, use_container_width=True)
    
    #%%
    container2=st.container()
    container3=st.container()
    col1,col2=st.columns(2)
    
    #%%
    df_hbar1=df_subset.groupby('POSITION').size().reset_index(name='NO. OF AVAILABLE JOBS')
    df_hbar1=df_hbar1.sort_values(by=['POSITION'])
    df_hbar2=df2_subset.groupby('APPLIED_POSITION').size().reset_index(name='NO. OF AVAILABLE CANDIDATES')
    df_hbar2=df_hbar2.sort_values(by=['APPLIED_POSITION'])
    
    hbar1=px.bar(df_hbar1, x='NO. OF AVAILABLE JOBS', y='POSITION', orientation='h',color_discrete_sequence=px.colors.qualitative.Pastel)
    #hbar1.update_yaxes(showticklabels=False)
    hbar1.update_xaxes(autorange='reversed')
    
    hbar2=px.bar(df_hbar2, x='NO. OF AVAILABLE CANDIDATES', y='APPLIED_POSITION', orientation='h',color_discrete_sequence=px.colors.qualitative.Pastel)
    hbar2.update_yaxes(visible=False)
    
    with container2:
        st.write("****BANDWISE DEMAND AND SUPPLY****")
    with container3:
        with col1:
            st.plotly_chart(hbar1, use_container_width=True)
        with col2:
            st.plotly_chart(hbar2, use_container_width=True)
            
#%%
    container4=st.container()
    
    df_figJ=df_subset.groupby('YEAR').size().reset_index(name='NO. OF AVAILABLE JOBS')
    
    df_figC=df2_subset.groupby('YEAR').size().reset_index(name='NO. OF AVAILABLE CANDIDATES')
    
    palette=cycle(px.colors.qualitative.Pastel)
    
    fig = go.Figure(
    data=[
        go.Bar(x=df_figJ['YEAR'], y=df_figJ['NO. OF AVAILABLE JOBS'], yaxis='y', offsetgroup=1,marker_color=next(palette), name='NO. OF AVAILABLE JOBS'),
        go.Bar(x=df_figC['YEAR'], y=df_figC['NO. OF AVAILABLE CANDIDATES'], yaxis='y2', offsetgroup=2,marker_color=next(palette), name='NO. OF AVAILABLE CANDIDATES')
    ],
    layout={
        'yaxis': {'title': 'NO. OF AVAILABLE JOBS'},
        'yaxis2': {'title': 'NO. OF AVAILABLE CANDIDATES', 'overlaying': 'y', 'side': 'right'}
    }
)

# Change the bar mode
    fig.update_layout(title='DEMAND AND SUPPLY OVER THE YEARS',barmode='group')
    
    
    with container4:
        st.plotly_chart(fig, use_container_width=True)

# Create figure with secondary y-axis
# =============================================================================
#     fig = make_subplots(specs=[[{"secondary_y": True}]])
#     
#     # Add traces
#     fig.add_trace(
#         go.Bar(x=df_figJ['YEAR'], y=df_figJ['NO. OF AVAILABLE JOBS'], name="yaxis data"),
#         secondary_y=False,
#     )
#     
#     fig.add_trace(
#         go.Bar(x=df_figC['YEAR'], y=df_figC['NO. OF AVAILABLE CANDIDATES'], name="yaxis2 data"),
#         secondary_y=True,
#     )
#     
#     # Add figure title
#     fig.update_layout(
#         title_text="BANDWISE RISE/FALL IN DEMAND AND SUPPLY OVER THE YEARS",barmode='group'
#     )
#     
#     # Set x-axis title
#     fig.update_xaxes(title_text="YEAR")
#     
#     # Set y-axes titles
#     fig.update_yaxes(title_text="NO. OF AVAILABLE JOBS", secondary_y=False)
#     fig.update_yaxes(title_text="NO. OF AVAILABLE CANDIDATES", secondary_y=True)
# =============================================================================  