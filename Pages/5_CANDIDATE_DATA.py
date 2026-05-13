# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 16:18:56 2023

@author: khush
"""

#%%
import sys
import pymysql
import streamlit as st
import pandas as pd
import numpy as np


sys.path.append('..')

from KakushIn_Dashboard.password import check_password

from KakushIn_Dashboard.read_json import add_json_data

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
    
    df = pd.read_sql('SELECT * FROM CANDIDATE', con=conn)
    #%%
    c1 = st.container()
    
    #%%
    df['YEAR'] = pd.DatetimeIndex(df['APPLICATION_DATE']).year
    #col1.dataframe(df.tail(), width = 800)
    #%%
    
    df_departments=pd.read_sql('SELECT * FROM DEPARTMENTS', con=conn)
    df_vendors=pd.read_sql('SELECT * FROM VENDORS', con=conn)
    df_campus=pd.read_sql('SELECT * FROM CAMPUS', con=conn)
    
    #%%
    
    with st.sidebar:
        cid=st.text_input("ENTER CANDIDATE ID")
        fname=st.text_input("ENTER FIRST NAME")
        lname=st.text_input("ENTER LAST NAME")
        gender=st.radio("GENDER:",('M','F'),horizontal=True)
        departments=st.multiselect('DEPARTMENTS:',df_departments['DEPARTMENT_NAME'].unique(),df_departments['DEPARTMENT_NAME'].unique())
        positions=st.multiselect('DESIGNATION:',df['APPLIED_POSITION'].unique(),df['APPLIED_POSITION'].unique())
        through=st.multiselect('APPLIED THROUGH:',df['APPLIED_THROUGH'].unique(),df['APPLIED_THROUGH'].unique())
        status=st.multiselect('HIRING STAGE:',df['STATUS'].unique(),df['STATUS'].unique())
        exp=st.text_input("ENTER EXPERIENCE YEARS")
        vendors=st.multiselect('VENDORS:',df_vendors['VENDOR_NAME'].unique())
        campus=st.multiselect('CAMPUS:',df_campus['CAMPUS_NAME'].unique())
        star_year, end_year =st.select_slider('APPLICATION YEAR:', options=sorted(df["YEAR"].unique()),value=(min(df["YEAR"].unique()),max(df["YEAR"].unique()) ))
        date=st.date_input("APPLICATION DATE")
        
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
    
    
    #%%
    if cid:
        cid=int(cid)
        df_subset=df.loc[(df['CANDIDATE_ID']==cid)]
    
    else:
        
        #%%
        df_subset=df.loc[(df['YEAR'] >= star_year) & (df['YEAR'] <= end_year) & (df['STATUS'].isin(status)) & (df['DEPARTMENT_ID'].isin(department_id)) & (df['APPLIED_POSITION'].isin(positions)) & (df['GENDER']==gender) & (df['APPLIED_THROUGH'].isin(through))]
        
        
        
        #%%
        
        if fname:
            df_subset=df_subset.loc[df_subset['CANDIDATE_FNAME']==fname]
        #%%
        
        if lname:
            df_subset=df_subset.loc[df_subset['CANDIDATE_LNAME']==lname]
            
        #%%
        
        if exp:
            exp=int(exp)
            df_subset=df_subset.loc[df_subset['EXPERIENCE_YEARS']>=exp]
        
        #%%
        
        if vendors:
            vens=""
            for vendor in vendors:
                if vendor == vendors[-1]:
                    vens=vens+"'"+vendor+"'"
                else:
                    vens= vens+"'"+vendor+"'"+','
            sql= "SELECT VENDOR_ID FROM VENDORS WHERE VENDOR_NAME IN ("+vens+")"
            cur.execute(sql)
            vendor_id=[i[0] for i in cur.fetchall()]
            
            df_subset=df_subset.loc[df_subset['VENDOR_ID'].isin(vendor_id)]
            
            if len(vendor_id)==1:
                vendor_id=vendor_id[0]
            
            
        else:
            vendor_id=None
            df_subset=df_subset[df_subset['VENDOR_ID'].isna()]
        # =============================================================================
        # st.write(vendor_id)  
        # st.write(department_id) 
        # st.write(status)    
        # =============================================================================
        #%%
        
        if campus:
            cams=""
            for c in campus:
                if c == campus[-1]:
                    cams=cams+"'"+c+"'"
                else:
                    cams= cams+"'"+c+"'"+','
            sql= "SELECT CAMPUS_ID FROM CAMPUS WHERE CAMPUS_NAME IN ("+cams+")"
            cur.execute(sql)
            campus_id=[i[0] for i in cur.fetchall()]
            
            df_subset=df_subset.loc[df_subset['CAMPUS_ID'].isin(campus_id)]
            
            if len(campus_id)==1:
                campus_id=campus_id[0]
            
        else:
            campus_id=None
            df_subset=df_subset[df_subset['CAMPUS_ID'].isna()]
        
            
       
        #%%
        
        if len(department_id)==1:
            department_id=department_id[0]
        if len(positions)==1:
            positions=positions[0]
        if len(through)==1:
            through=through[0]
        if len(status)==1:
            status=status[0]
        
        #%%
    def add_candidate(fname,lname,gender,department_id,positions,through,status,exp,vendor_id,campus_id,date):
            try:
                sql= "INSERT INTO candidate (CANDIDATE_FNAME, CANDIDATE_LNAME, GENDER, DEPARTMENT_ID, APPLIED_POSITION, APPLIED_THROUGH, STATUS, EXPERIENCE_YEARS,VENDOR_ID, CAMPUS_ID, APPLICATION_DATE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val=(fname,lname,gender,department_id,positions,through,status,exp,vendor_id,campus_id,date)
                cur.execute(sql,val)
                conn.commit()
                st.write('CANDIDATE ADDED')
            except:
                st.write('INVALID INPUT')

           
        #%%
    container1=st.container()  
    with container1:  
        st.write('**ENTER CANDIDATE DETAILS TO ADD CANDIDATE**')
        button=st.button("ADD CANDIDATE", on_click=add_candidate,args =(fname,lname,gender,department_id,positions,through,status,exp,vendor_id,campus_id,date))
# =============================================================================
#     try:
#         button=st.button("ADD CANDIDATE", on_click=add_candidate,args =(fname,lname,gender,department_id,positions,through,status,exp,vendor_id,campus_id,date))
#     except:
#         
#         pass
# =============================================================================
    
    container2 = st.container()
    container3 = st.container()
    
    with container2:
        st.write("ADD CANDIDATE DATA FROM JSON FILE")
        file= st.text_input("ENTER PATH OF JSON FILE")
       
        temp = None
        button2=st.button("ADD CANDIDATE DATA", on_click = add_json_data, args = (file,temp))

        
    st.write("\n\n\n\n")
             
    df_subset
        
    
