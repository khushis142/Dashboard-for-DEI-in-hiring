# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 15:11:00 2023

@author: khush
"""
#%%

import pymysql
import streamlit as st
import pandas as pd
import numpy as np

#%%

# database connection
conn = pymysql.connect(
    host='localhost',
    user='root', 
    password = "Khushi2002",
    db='ALWAYS_FIRST_IT_ENABLED_SOLUTIONS',
    )

#%%

cur = conn.cursor()

#%%

cur.execute("select @@version")
output = cur.fetchall()
print(output)

cur.execute("select * from candidate")
output = cur.fetchall()
      
for i in output:
    print(i)

#%%

sql = "INSERT INTO candidate (CANDIDATE_FNAME, CANDIDATE_LNAME, GENDER, DEPARTMENT_ID, APPLIED_POSITION, APPLIED_THROUGH, STATUS, EXPERIENCE_YEARS,VENDOR_ID, CAMPUS_ID, APPLICATION_DATE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
val = ('Ram', 'Dubey','M',3,'ANALYST','VENDOR','STAGE 1',4,2,None,'2021-07-08')

cur.execute(sql, val)

conn.commit()
 
print(cur.rowcount, "details inserted")

#%%

sql = "INSERT INTO candidate (CANDIDATE_FNAME, CANDIDATE_LNAME, GENDER, DEPARTMENT_ID, APPLIED_POSITION, APPLIED_THROUGH, STATUS, EXPERIENCE_YEARS,VENDOR_ID, CAMPUS_ID, APPLICATION_DATE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

val=[('Sham','Singh','M',2,'ASSOCIATE','WEBSITE','STAGE 2',6,None,None,'2018-09-04'),
     ('Rashmi','Thakur','F',1,'ED','REFERENCE','STAGE 1',8,None,None,'2020-01-01')]

cur.executemany(sql, val)

conn.commit()
 
print(cur.rowcount, "details inserted")



#%%

sql = "UPDATE CANDIDATE SET CANDIDATE_FNAME = 'Ramesh' WHERE CANDIDATE_FNAME ='Ram'"
cur.execute(sql)
conn.commit()
    
#%%

sql = "DELETE FROM CANDIDATE WHERE CANDIDATE_FNAME = %s"
val=('Ram')

cur.execute(sql, val)

conn.commit()

#%%
      
# To close the connection
conn.close()
