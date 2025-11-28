# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 11:10:28 2023

@author: khush
"""

import streamlit as st

from password import check_password

st.set_page_config(
    page_title="BuildTogether",
    page_icon="🤝",
    layout="wide"
)


#%%
if check_password():

    st.markdown('''<body style="display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin: 0;">
  <div style="background-color: red;
  padding: 20px;">
    <h1 style="color: white;
  text-align: center;">WELCOME TO BuildTogether</h1>
  </div>
</body>''',
unsafe_allow_html=True)
    
    st.sidebar.write("****SELECT A PAGE****")







