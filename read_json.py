import pymysql, os, json
import streamlit as st

# read JSON file which is in the next parent folder
#file = r'C:\Users\khush\OneDrive\Documents\KakushIn_Dashboard\test.json'

def add_json_data(file,temp):
    try:
        rfile=r'{}'.format(file)
        json_data=open(rfile).read()
        json_obj = json.loads(json_data)

        # connect to MySQL
        con = pymysql.connect(
            host='localhost',
            user='root', 
            password = "Khushi2002",
            db='ALWAYS_FIRST',
            )
        cursor = con.cursor()
        
        
        # parse json data to SQL insert
        for i, item in enumerate(json_obj):
            candidateName = item.get("CANDIDATE_FNAME", None)
            candidateLname = item.get("CANDIDATE_LNAME", None)
            gender = item.get("GENDER", None)
            dep_id = item.get("DEPARTMENT_ID", None)
            app_pos = item.get("APPLIED_POSITION", None)
            app_thru = item.get("APPLIED_THROUGH", None)
            status = item.get("STATUS", None)
            exp = item.get("EXPERIENCE_YEARS", None)
            vendor_id = item.get("VENDOR_ID", None)
            campus_id = item.get("CAMPUS_ID", None)
            app_date = item.get("APPLICATION_DATE", None)
            
            
            cursor.execute("INSERT INTO candidate (CANDIDATE_FNAME, CANDIDATE_LNAME, GENDER, DEPARTMENT_ID, APPLIED_POSITION, APPLIED_THROUGH, STATUS, EXPERIENCE_YEARS,VENDOR_ID, CAMPUS_ID, APPLICATION_DATE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (candidateName, candidateLname, gender, dep_id, app_pos, app_thru, status, exp, vendor_id, campus_id, app_date))
            con.commit()
        st.write("CANDIDATES ADDED")
        con.close()
    except:
        st.write("INVALID INPUT")