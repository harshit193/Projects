import streamlit as st
import numpy as np
import pandas as pd
import joblib
import pickle


df = pd.read_csv('./Used_Bikes.csv')
df.drop(columns='price',inplace=True)
required_columns = df.columns

bike_names = df['bike_name'].unique()
cities = df['city'].unique()
brands = df['brand'].unique()


scaler = joblib.load('./scaler.jlb')
en_bike_name = joblib.load('./Encoder_bike_name.jlb')
en_brand = joblib.load('./Encoder_brand.jlb')
en_city = joblib.load('./Encoder_city.jlb')
en_owner = {'First Owner':0,'Second Owner':1,'Third Owner':2,'Fourth Owner Or More':3}



vr_model = joblib.load('./voting_regressor.jlb')
rfr_model = joblib.load('./Random_forest.jlb')



st.title('Used Bike Price Prediction web-app')

st.subheader('Fill the values for predicting the bike price')

bike_name = st.selectbox(label='Select Bike',options=bike_names,index=None)
brand = st.selectbox('Select Brand',brands,index=None)
city = st.selectbox('Select City',cities,index=None)
kms_driven = st.number_input('Enter Kms Driven')
owner = st.selectbox('Select Owner',['First Owner','Second Owner','Third Owner','Fourth Owner Or More'],index=None)
age = st.number_input('Enter Bike age')
power = st.number_input('Enter Power in cc')

button = st.button('predict')



if bike_name:
    bike_name = en_bike_name.transform([bike_name])
if brand:
    brand = en_brand.transform([brand])
if city:
    city = en_city.transform([city])
if owner:
    owner = en_owner[owner]

input_data = {
    'bike_name':bike_name,
    'city':city,
    'kms_driven':kms_driven,
    'owner':owner,
    'age':age,
    'power':power,
    'brand':brand
}

input_data = pd.DataFrame([input_data])

if button:
    if not all([col in input_data.columns for col in required_columns]):
        st.warning(f'Required columns missing. Required columns: {required_columns}')
    else:
        scaled_input_data = scaler.transform(input_data)
        predict = rfr_model.predict(scaled_input_data)
        st.success(f'Predicted price is: {predict[0]:.2f}')

st.dataframe(input_data)