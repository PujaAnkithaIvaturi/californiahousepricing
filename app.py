import pickle
from flask import Flask, request, app, jsonify, url_for, render_template
import numpy as np
import pandas as pd

#Starts the app just like main function
app=Flask(__name__)
#Loading the model
regmodel=pickle.load(open('regmodel.pkl','rb'))
scalar=pickle.load(open('scaling.pkl','rb'))
@app.route('/')
def home():
    return render_template('home.html')

#creating a predict API, wherein using postman or other tools, to send a request to the app and get a output
#Through predict_api on hitting it, the input we give should be given in json format that is stored in data key.

#This function transforms the input given in the form, predicts the output
@app.route('/predict_api', methods=['POST'])
def predict_api():
    data=request.json['data']
    print(data)
    print(np.array(list(data.values())).reshape(1,-1))
    new_data=scalar.transform(np.array(list(data.values())).reshape(1,-1))
    output=regmodel.predict(new_data)
    print(output[0])
    return jsonify(output[0])


#Creating and taking in the values inputted from the HTML Form
@app.route('/predict',methods=['POST'])
def predict():
    #taking the input value (could be integer) from the form and converting them into float
    data=[float(x) for x in request.form.values()]
    final_input=scalar.transform(np.array(data).reshape(1,-1))
    print(final_input)
    output=regmodel.predict(final_input)[0]
    return render_template("home.html",prediction_text="The House Price Prediction with the given data in California is {}.".format(output))

if __name__=="__main__":
    app.run(debug=True)

#In our Linear regression model, the first thing we did after splitting the data, we did standardization.
