# Phishing Domain Detection

![cover_image](https://github.com/akpmpr/phishing-domain-detection/blob/main/misc/phishing-image.jpg?raw=true)

## Objective
Phishing is a type of social engineering attack often used to steal user data, including login credentials and credit card numbers. It occurs when an attacker, masquerading as a trusted entity, dupes a victim into opening a URL send via an email, instant message, or text message. The objective of this project is to train machine learning models on the dataset created to predict phishing websites. Both phishing and legit URLs of websites are gathered to form a dataset and from them required URL features are extracted. The performance level of each model is measures and compared.

## Data Collection
The set of phishing URLs are collected from opensource service called PhishTank. This service provide a set of phishing URLs in multiple formats like csv, json etc. that gets updated hourly. The legitimate URLs are obatined from the open datasets of the University of New Brunswick. This dataset has a collection of benign, spam, phishing, malware & defacement URLs. Out of all these types, the benign url dataset is considered for this project. The above mentioned datasets are uploaded to the [data](https://github.com/akpmpr/phishing-domain-detection/tree/main/data) folder of this repository.

## Feature Extraction
The below mentioned category of features are extracted from the URL data:

- Address Bar based Features (In this category 9 features are extracted.)
- Domain based Features (In this category 4 features are extracted.)

So, all together 13 features are extracted from the two datasets and are and trained with different machine learning models.
The features are referenced from the phishing websites page given in the [machine learning repository](https://archive.ics.uci.edu/ml/datasets/Phishing+Websites) of University of California, Irvine.

## Models & Training
Before starting the ML model training, the data is split into 80:20 (train : test). From the dataset, it is clear that this is a supervised machine learning task. There are two major types of supervised machine learning problems, called classification and regression. This dataset comes under classification problem, as the input URL is classified as phishing (1) or legitimate (0). The machine learning models considered to train the dataset in this project are:

- XGBClassifier
- Decision Tree
- Random Forest
- LogisticRegression
- KNeighborsClassifier

All these models are trained on the train dataset and evaluation of the model is done with the test dataset.

## Result
From the obtained results of the above models, XGBoost Classifier has highest model performance of 95.6%. So the model is saved to the file [XGBClassifier.pickle.dat](https://github.com/akpmpr/phishing-domain-detection/blob/main/XGBClassifier.pickle.dat).

## Next Steps
This project can be further extended by creating an application on Flask and hosting it in a cloud platform like AWS, Azure or GCP, which will take the URL and predict it's nature i.e. legitimate or phishing. As of now, I am working towards the creation of the Flask application for this project. The further developments will be updated at the earliest.
