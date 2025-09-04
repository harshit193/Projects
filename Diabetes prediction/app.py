import streamlit as st
import pandas as pd
import joblib
import pickle

df = pd.read_csv('./diabetes.csv')
df.drop(columns='Outcome',inplace=True)
required_columns = df.columns

with open('./scaler.pkl','rb') as file:
    scaler = pickle.load(file)


vc_model = joblib.load('./vc_model.jlb')
rfc_model = joblib.load('./rfc_model.jlb')

input_data={}

st.title('Diabetes Prediction')

with st.form('form'):
    pregnances = st.number_input('Enter number of pregnancies')
    glucose = st.number_input('Enter level of Glucose')
    blood_pressure = st.number_input('Enter Blood Pressure')
    skin_thikness = st.number_input('Enter thikness of skin')
    insulin = st.number_input('Enter insulin level in blood')
    bmi = st.number_input('Enter Body mass index')
    diabetes_pedigree_function = st.number_input('Enter the Diabetes percentage*100')/100
    age = st.number_input('Enter Age')
    
    button = st.form_submit_button('Predict')
    
    if button:
        input_data = {
            'Pregnancies':pregnances,
            'Glucose':glucose,
            'BloodPressure':blood_pressure,
            'SkinThickness':skin_thikness,
            'Insulin':insulin,
            'BMI':bmi,
            'DiabetesPedigreeFunction':diabetes_pedigree_function,
            'Age':age
        }
        input_data = pd.DataFrame([input_data])
        
        if all([col in input_data.columns for col in required_columns]):
            input_data_scaled = scaler.transform(input_data)
            predict = vc_model.predict(input_data_scaled)
            if predict:
                st.success('You have diabetes') 
            else:
                st.success("You don't have Diabetes")
        else:
            st.warning(f'Required columns missing. required columns: {required_columns}')


st.dataframe(input_data, hide_index=True)