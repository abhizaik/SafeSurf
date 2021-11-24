import numpy as np
from flask import Flask, request, jsonify, render_template
import  pickle
import features

app = Flask(__name__)
model = pickle.load(open('phishing.pkl','rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    url = [str(x) for x in request.form.values()]
    print(url)

    data = [features.featureExtraction(url[0])]
    print(data)
    data = np.array(data)


    prediction = model.predict(data)

    if prediction[0] ==1:
        prediction = 'PHISHING'
    else:
        prediction = 'LEGIT'

    return render_template('index.html', prediction_text = 'Given domain is {}.'.format(prediction))



if __name__ == '__main__':
    app.run(debug=True)