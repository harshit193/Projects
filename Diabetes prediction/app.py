from flask import Flask, render_template, request, jsonify
import joblib
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

vc_model = joblib.load(r'E:\Windows 10\Python Files\Projects\Diabetes prediction\vc_model.joblib')
with open(r'E:\Windows 10\Python Files\Projects\Diabetes prediction\scaler.pkl','rb') as file:
    scaler = pickle.load(file)

app = Flask(__name__)

@app.route('/')
def home():
    return 'Diabetes prediction model is running'

@app.route(rule='/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        input_data = pd.DataFrame([data])
        
        if not data:
            return jsonify({'error':'input data not provided'}), 400
        
        required_columns = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
        
        if not all(col in input_data.columns for col in required_columns):
            return jsonify({'error':'Required columns missing. Required columns: '}), 400
        
        scaled_data = scaler.transform(input_data)
        
        prediction = vc_model.predict(scaled_data)
        
        response = {
            'prediction': 'diabetes' if prediction[0] == 1 else 'no diabetes'
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error':str(e)}), 500

if __name__=='__main__':
    app.run(debug=True)