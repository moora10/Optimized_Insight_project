#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 22:10:04 2020

@author: annahmoore
"""


import streamlit as st
import pandas as pd
import numpy as np
from sklearn import datasets, ensemble
from sklearn.ensemble import RandomForestClassifier

st.write("""
         # Amyloid Augury
         **_Personalized_** risk profiling for the earliest pathological marker of Alzheimer's disease
""")

uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
if uploaded_file is not None:
     data = pd.read_csv(uploaded_file)
     #st.write(data)
if uploaded_file is None:
     st.write("Please upload data file")

#import model 
import pickle
filename = 'random_forest_model_optimized.sav'
loaded_model = pickle.load(open(filename, 'rb'))

if st.button('Predict'):
	out = loaded_model.predict(data)
	#save prediction as an array 
	out = np.array(out)

	out_framed = pd.DataFrame(data=out.flatten(), columns=['Prediction'])

	#change from 0 and 1 to high and low risk
	out_framed.replace(0, "high risk", inplace=True)
	out_framed.replace(1, "low risk", inplace=True)

	results_full = pd.concat([out_framed, data], axis=1, sort=False)

	st.write(results_full)
	
	#create download button
	import base64
	def get_table_download_link(df):
	    """Generates a link allowing the data in a given panda dataframe to be downloaded
	    in: dataframe
	    out: href string
	    reference:https://discuss.streamlit.io/t/how-to-set-file-download-function/2141
	    """
	    csv = df.to_csv(index=False)
	    b64 = base64.b64encode(
		csv.encode()
	    ).decode() # some strings <-> bytes conversions necessary here
	    return f'<a href="data:file/csv;base64,{b64}" download="amyloid_risk_predictions.csv">Download csv file</a>'
	
	st.markdown(get_table_download_link(results_full), unsafe_allow_html=True)

