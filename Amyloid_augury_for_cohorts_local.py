#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 22:10:04 2020

@author: annahmoore
"""


import streamlit as st
import pandas as pd
import numpy as np
import base64
import pickle

st.write("""
         # Amyloid Augury
         **_Personalized_** risk profiling for the earliest pathological marker of Alzheimer's disease
""")
import base64

#create template for download
template = pd.read_csv("/Users/annahmoore/Desktop/columns.csv")
st.write('Template available for download below')
def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(
        csv.encode()
    ).decode()  # some strings <-> bytes conversions necessary here
    return f'<a href="data:file/csv;base64,{b64}" download="template.csv">Download template</a>'
st.markdown(get_table_download_link(template), unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
if uploaded_file is not None:
     data = pd.read_csv(uploaded_file)
     #st.write(data)
if uploaded_file is None:
     st.write("Please upload data file")

#import model 
filename = 'random_forest_model_final.sav'
loaded_model = pickle.load(open("/Users/annahmoore/Desktop/random_forest_model_final.sav", 'rb'))

if st.button('Predict'):
    out = loaded_model.predict(data)
    out = np.array(out)

    out_framed = pd.DataFrame(data=out.flatten(), columns=['Prediction'])

    #change from 0 and 1 to high and low risk
    out_framed.replace(0, "low risk", inplace=True)
    out_framed.replace(1, "high risk", inplace=True)

    results_full = pd.concat([out_framed, data], axis=1, sort=False)

    st.write(results_full)

    import base64
    def get_table_download_link(df):
        """Generates a link allowing the data in a given panda dataframe to be downloaded
        in:  dataframe
        out: href string
        """
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(
            csv.encode()
        ).decode()  # some strings <-> bytes conversions necessary here
        return f'<a href="data:file/csv;base64,{b64}" download="myfilename.csv">Download results file</a>'

    st.markdown(get_table_download_link(results_full), unsafe_allow_html=True)

#### Allow some exploration of individual trial candidates 
    candidate_selection = st.sidebar.selectbox(
    "Select a trial candidate for exploration",
    ('Candidate 1', 'Candidate 2', 'Candidate 3', 'Candidate 4')
)
    if candidate_selection == 'Candidate 1':
            st.write(results_full.iloc[0, 0:51])
            if results_full.iloc[0,0] == "high risk":
                st.header("High risk for brain amyloid, recommended that this candidate moves to PET screen")
            else:
                st.header("Low risk for brain amyloid, recommended that this candidate does not move to PET screen")
    if candidate_selection == 'Candidate 2':
            st.write(results_full.iloc[1, 0:51])
            if results_full.iloc[1,0] == "high risk":
                st.header("High risk for brain amyloid, recommended that this candidate moves to PET screen")
            else:
                st.header("Low risk for brain amyloid, recommended that this candidate does not move to PET screen")

    #if candidate_selection == 'Candidate 3':
     #       st.write(results_full.iloc[2, 0:51])
    #if results_full.iloc[2,0] == 'high risk':
     #       st.header("High risk for brain amyloid, recommended that this candidate moves to PET screen")
    #if results_full.iloc[2,0] == 'low risk':
     #       st.header("Low risk for brain amyloid, recommended that this candidate does not move to PET screen")

    #if candidate_selection == 'Candidate 4':
    #        st.write(results_full.iloc[3, 0:51])
    #if results_full.iloc[3,0] == 'high risk':
     #       st.header("High risk for brain amyloid, recommended that this candidate moves to PET screen")
    #if results_full.iloc[3,0] == 'low risk':
     #       st.header("Low risk for brain amyloid, recommended that this candidate does not move to PET screen")


#####old
#out = loaded_model.predict(data)

#save prediction as an array 
#out = np.array(out)

#out_framed = pd.DataFrame(data=out.flatten(), columns=['Prediction'])

#out_framed.replace(0, "high risk", inplace=True)
#out_framed.replace(1, "low risk", inplace=True)
#out_framed.replace(to_replace =[0],  
                          #  value ='high risk')
#append the array onto the dataframe as a new column
#data['prediction'] = out
#results_full = pd.concat([out_framed, data], axis=1, sort=False)

#st.write(results_full)

#import base64
#def get_table_download_link(df):
 #   """Generates a link allowing the data in a given panda dataframe to be downloaded
  #  in:  dataframe
   # out: href string
   # """
   # csv = df.to_csv(index=False)
   # b64 = base64.b64encode(
   #     csv.encode()
   # ).decode()  # some strings <-> bytes conversions necessary here
   # return f'<a href="data:file/csv;base64,{b64}" download="myfilename.csv">Download csv file</a>'

#st.markdown(get_table_download_link(results_full), unsafe_allow_html=True)

