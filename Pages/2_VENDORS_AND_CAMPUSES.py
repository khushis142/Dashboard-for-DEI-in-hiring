# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 15:56:21 2023

@author: khush
"""
import sys
import pymysql
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
#%%

st.set_page_config(
    page_title="BuildTogether: Vendors And Campuses",
    page_icon= ':a:',
    layout="wide"
)


#%%

sys.path.append('..')

from KakushIn_Dashboard.password import check_password

#sys.path.append('..')
from KakushIn_Dashboard.ws import scrape_campus, scrape_vendor
#from KakushIn_Dashboard.web_scraper2 import scrape_vendor




#%%
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
    
    col1, col2 = st.columns(2)
    
    #%%
    
    #df= pd.read_sql('SELECT * FROM CANDIDATE', con=conn)
    
    query="""SELECT c.CANDIDATE_ID, c.CANDIDATE_FNAME, c.CANDIDATE_LNAME, c.GENDER, c.DEPARTMENT_ID, c.APPLIED_POSITION, c.APPLIED_THROUGH, c.STATUS, c.EXPERIENCE_YEARS, c.VENDOR_ID, c.CAMPUS_ID, c.APPLICATION_DATE, v.VENDOR_NAME
      FROM CANDIDATE c
      LEFT JOIN VENDORS v
      ON v.VENDOR_ID = c.VENDOR_ID"""
    
    df= pd.read_sql(query, conn)
    df['YEAR'] = pd.DatetimeIndex(df['APPLICATION_DATE']).year
    
    query2="""SELECT c.CANDIDATE_ID, c.CANDIDATE_FNAME, c.CANDIDATE_LNAME, c.GENDER, c.DEPARTMENT_ID, c.APPLIED_POSITION, c.APPLIED_THROUGH, c.STATUS, c.EXPERIENCE_YEARS, c.VENDOR_ID, c.CAMPUS_ID, c.APPLICATION_DATE, v.CAMPUS_NAME
      FROM CANDIDATE c
      LEFT JOIN CAMPUS v
      ON v.CAMPUS_ID = c.CAMPUS_ID"""
    
    df2= pd.read_sql(query2, conn)
    df2['YEAR'] = pd.DatetimeIndex(df2['APPLICATION_DATE']).year
    
    query3 = """SELECT 
  EMPLOYEE.EMPLOYEE_ID,
  EMPLOYEE.GENDER,
  EMPLOYEE.POSITION,
  EMPLOYEE.DEPARTMENT_ID,
  VENDORS.VENDOR_NAME,
  CAMPUS.CAMPUS_NAME,
  PERFORMANCE.SCORE_YEAR,
  PERFORMANCE.SCORE
FROM 
  EMPLOYEE
JOIN 
  CANDIDATE ON EMPLOYEE.CANDIDATE_ID = CANDIDATE.CANDIDATE_ID
LEFT JOIN 
  VENDORS ON CANDIDATE.VENDOR_ID = VENDORS.VENDOR_ID
LEFT JOIN 
  CAMPUS ON CANDIDATE.CAMPUS_ID = CAMPUS.CAMPUS_ID
LEFT JOIN 
  PERFORMANCE ON EMPLOYEE.EMPLOYEE_ID = PERFORMANCE.EMPLOYEE_ID;"""
    df3= pd.read_sql(query3, conn)
    
    # =============================================================================
    # count=df['VENDOR_NAME'].value_counts()
    # count
    # =============================================================================
    
    df_departments=pd.read_sql('SELECT * FROM DEPARTMENTS', con=conn)
    #%%
    
    with st.sidebar:
        
        gender= st.multiselect('GENDER:',df['GENDER'].unique(), df['GENDER'].unique())
        
        positions=st.multiselect('Designation:',df['APPLIED_POSITION'].unique(),df['APPLIED_POSITION'].unique())
        
        departments=st.multiselect('Departments:',df_departments['DEPARTMENT_NAME'].unique(),df_departments['DEPARTMENT_NAME'].unique())
        
        hired = st.checkbox('HIRED CANDIDATES ONLY')
        if hired:
            df_subset = df.loc[df['STATUS']=='HIRED']
            df2_subset = df2.loc[df['STATUS']=='HIRED']
        else:
            df_subset = df
            df2_subset = df2
            
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
    
    df_subset=df_subset.loc[(df_subset['DEPARTMENT_ID'].isin(department_id)) & (df_subset['APPLIED_POSITION'].isin(positions)) & (df_subset['GENDER'].isin(gender))]   
        
    
    
    df2_subset=df2_subset.loc[(df2_subset['DEPARTMENT_ID'].isin(department_id)) & (df2_subset['APPLIED_POSITION'].isin(positions)) & (df2_subset['GENDER'].isin(gender))]   
    
    df3_subset=df3.loc[(df3['DEPARTMENT_ID'].isin(department_id)) & (df3['POSITION'].isin(positions)) & (df3['GENDER'].isin(gender))]
        
    
    
    #%%
    with col1:
        
        #VENDOR RECOMENDATION DF HERE
        
        line1_df = df_subset.groupby(['YEAR','VENDOR_NAME','GENDER']).size().reset_index(name='FREQUENCY')
        
        line1 = px.area(line1_df, x= 'YEAR', y= 'FREQUENCY', color='VENDOR_NAME',title="VENDOR GRAPH", color_discrete_sequence=px.colors.qualitative.Pastel, line_group='GENDER')
        
        
        line1.update_layout(
            xaxis_title_text='Year',
            yaxis_title_text='No of Candidates',
            plot_bgcolor="white",
            
        )
        
        st.plotly_chart(line1, use_container_width=True)
        
        area1_df= df3_subset.groupby(['SCORE_YEAR','VENDOR_NAME'])['SCORE'].mean().reset_index(name='PERFORMANCE_SCORE')
        
        area1=px.bar(area1_df, x='SCORE_YEAR', y='PERFORMANCE_SCORE', color='VENDOR_NAME', barmode='group',title="PERFORMANCE OF EMPLOYEES PROVIDED BY VENDORS" )
        
        st.plotly_chart(area1, use_container_width=True)
        
        
    #%%
    with col2:
        
# =============================================================================
#         # Campus Recomendation Here
#         st.write("**SUGGESTED CAMPUSES**")
#         campus_rec_df=scrape_campus()
#         campus_rec_df.head()
#         st.dataframe(campus_rec_df['SUGGESTED CAMPUS'].head(),use_container_width=True)
# =============================================================================
        
        line2_df = df2_subset.groupby(['YEAR','CAMPUS_NAME','GENDER']).size().reset_index(name='FREQUENCY')
        #line2_df
        line2 = px.area(line2_df, x= 'YEAR', y= 'FREQUENCY', color='CAMPUS_NAME',title="CAMPUS GRAPH", color_discrete_sequence=px.colors.qualitative.Pastel, line_group='GENDER')
  
        #line_shape='spline'        
        
        line2.update_layout(
            xaxis_title_text='Year',
            yaxis_title_text='No of Candidates',
            plot_bgcolor="white",   
        )
        
        st.plotly_chart(line2, use_container_width=True)
        
        bar2_df=df3_subset.groupby(['SCORE_YEAR','CAMPUS_NAME'])['SCORE'].mean().reset_index(name='PERFORMANCE_SCORE')
        
        bar1=px.bar(bar2_df, x='SCORE_YEAR', y='PERFORMANCE_SCORE', color='CAMPUS_NAME', barmode='group',title="PERFORMANCE OF EMPLOYEES FROM CAMPUSES" )
        
        st.plotly_chart(bar1, use_container_width=True)
    
    
        
        
        
    with col1:
        st.write("**SUGGESTED VENDORS**")
        vendor_rec_df=scrape_vendor()
        
        st.dataframe(vendor_rec_df['NAME OF VENDOR'].head(),use_container_width=True)
        
        def insert_vendor(vname,vloc):
            try:
                query="INSERT INTO RECOMMENDED_VENDOR (VENDOR_NAME,VENDOR_LOCATION) VALUES (%s, %s)"
                val=(vname,vloc)
                cur.execute(query,val)
                conn.commit()
                st.write('VENDOR RECOMENDATION ADDED')
            except:
                st.write('INVALID INPUT')
        
        st.write('**RECOMMEND A VENDOR**')
        
        vname=st.text_input("ENTER VENDOR NAME")
        if vname:
            vvname=vname
        else:
            vvname=None
        vloc=st.text_input("ENTER VENDOR LOCATION")
        if vloc:
            vvloc=vloc
        else:
            vvloc=None
        
        button=st.button("ADD VENDOR RECOMMENDATION", on_click=insert_vendor,args =(vvname,vvloc))
    
    with col2:
        
        st.write("**SUGGESTED CAMPUSES**")
        campus_rec_df=scrape_campus()
        
        st.dataframe(campus_rec_df['SUGGESTED CAMPUS'].head(),use_container_width=True)
        
        def insert_campus(cname,cloc):
            try:
                query="INSERT INTO RECOMMENDED_CAMPUS (CAMPUS_NAME,CAMPUS_LOCATION) VALUES (%s, %s)"
                val=(cname,cloc)
                cur.execute(query,val)
                conn.commit()
                st.write('CAMPUS RECOMENDATION ADDED')
            except:
                st.write('INVALID INPUT')
        
        st.write('**RECOMMEND A CAMPUS**')
        
        cname=st.text_input("ENTER CAMPUS NAME")
        if cname:
            ccname=cname
        else:
            ccname=None
        cloc=st.text_input("ENTER CAMPUS LOCATION")
        if cloc:
            ccloc=cloc
        else:
            ccloc=None
        
        button=st.button("ADD CAMPUS RECOMMENDATION", on_click=insert_campus,args =(ccname,ccloc))
        
        
        