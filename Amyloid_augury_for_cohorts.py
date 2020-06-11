#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 22:10:04 2020

@author: annahmoore
"""


import streamlit as st
import pandas as pd
import numpy as np

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

out = loaded_model.predict(data)

#save prediction as an array 
out = np.array(out)

out_framed = pd.DataFrame(data=out.flatten(), columns=['Prediction'])

out_framed.replace(0, "high risk", inplace=True)
out_framed.replace(1, "low risk", inplace=True)
#out_framed.replace(to_replace =[0],  
                          #  value ='high risk')
#append the array onto the dataframe as a new column
#data['prediction'] = out
results_full = pd.concat([out_framed, data], axis=1, sort=False)

st.write(results_full)

