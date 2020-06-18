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
st.header("Cohort mode") 
#create template for download
template = pd.read_csv('columns.csv')
st.write('Cohort mode template available for download below')
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
filename = 'random_forest_model_optimized.sav'
loaded_model = pickle.load(open(filename, 'rb'))

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
        return f'<a href="data:file/csv;base64,{b64}" download="amyloid_risk_predictions.csv">Download results file</a>'

    st.markdown(get_table_download_link(results_full), unsafe_allow_html=True)
    st.subheader("High risk candidates for brain amyloid are recommended to move to PET screening.")

## Add individual exploratory sidebar with some of the most important features
st.sidebar.header("Individual exploratory mode")                
                
st.sidebar.subheader('Demographics')
age = st.sidebar.slider('Age', 54, 90, 78, 1)

st.sidebar.subheader('Genetic Profile')
apoe_count = st.sidebar.selectbox('APOE4 Allele Count', ('0', '1', '2'), 2)
superPGRSATN = st.sidebar.slider('Genetic Risk Score', -1.3, 1.3, 1.2, 0.1)

st.sidebar.subheader('Serum Protein Concentrations')
ChromograninA = st.sidebar.slider('Chromogranin A (ng/mL)', 1.0, 3.4, 2.5, 0.1)
Eotaxin = st.sidebar.slider('Eotaxin.3 (pg/mL)', 1.5, 3.3, 3.0, 0.1)
Tenascin_C = st.sidebar.slider('Tenascin C (ng/mL)', 2.2, 3.4, 2.3)

filename = 'indiv_exploratory.sav'
loaded_model = pickle.load(open(filename, 'rb'))

if st.sidebar.button('Individual Prediction'):

    X_test ={'apoe_count': apoe_count, 'age': age, 'Chromogranin.A.':ChromograninA, 'Eotaxin': Eotaxin, 'superPGRSATN': superPGRSATN, 'Tenascin.C': Tenascin_C}


    X_test = pd.DataFrame.from_dict(X_test, orient='index')
#transpose
    X_test_input = X_test.T

    out = loaded_model.predict(X_test_input)
#print(y_pred)
    if out == 1:
        st.title('High risk for brain amyloid, recommended that this candidate moves to PET screen')
    else: 
        st.title('Low risk for brain amyloid, recommended that this candidate does not move to PET screen')

