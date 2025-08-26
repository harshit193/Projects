from flask import Flask, render_template, request
import joblib
import pickle


app = Flask(__name__)

#Loading the model
model = joblib.load('filename.joblib')
#another method
model = pickle.laod('filename.pkl','rb')

@app.route('/')
def home():
    return render_template('index.html', **locals())

@app.route('/predict', methods=['POST','GET'])
def predict():
    variable_name1 = request.form['variable_name1'] #we need to type cast the data into int or float before using them
    variable_name2 = request.form['variable_name2'] #we need to type cast the data into int or float before using them
    result = model.predict([variable_name1,variable_name2])
    return render_template('index.html', **locals())


if __name__=='__main__':
    app.run(debug=True)