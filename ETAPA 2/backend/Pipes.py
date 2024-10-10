
from sklearn.metrics import classification_report, f1_score, precision_score, recall_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from langdetect import DetectorFactory, detect
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from typing import Union

import pandas as pd
import numpy as np
import string


class Cleaning:

    def __init__(self, isTraining = False):
        self.translateTable = str.maketrans(' ', ' ', string.punctuation)
        self.stopwords = set(stopwords.words('spanish'))
        self.lemmatizer = WordNetLemmatizer()
        self.isTraining = isTraining
        DetectorFactory.seed = 42
        self.df = None
    
    def detect_language(self, text):
        try:
            return detect(text)
        except:
            return None

    def fix_codification(self, text:str):
        utf8_to_ansi = {"Ã": "Á","Ã¡": "á","Ã‰": "É","Ã©": "é","Ã": "Í","Ã­": "í","Ã“": "Ó",
                        "Ã³": "ó","Ãš": "Ú","Ãº": "ú","Ã‘": "Ñ","Ã±": "ñ","Â¿": "¿"}
        for utf8, ansi in utf8_to_ansi.items():
            text = text.replace(utf8, ansi)
        return text
    
    def to_lowercase(self, text:str):
        return text.lower()
    
    def replace_accents(self, text:str):
        accents = {'á': 'a','é': 'e','í': 'i','ó': 'o','ú': 'u'}
        for accented, unaccented in accents.items():
            text = text.replace(accented, unaccented)
        return text
    
    def remove_characters(self, text:str):
        return text.translate(self.translateTable)
    
    def remove_stopwords(self, text:str):
        return [word.strip() for word in text.split(' ') if word not in self.stopwords and len(word) > 2]

    def remove_no_alphabetics(self, words:list[str]):
        return [word for word in words if word.isalpha()]
    
    def lemmatize(self, words:list[str]):
        lemas = []
        for word in words:
            if len(word) > 4:
                lemas.append(self.lemmatizer.lemmatize(word, pos = 'v'))
            else:
                lemas.append(word)
        return lemas

    def remove_routes(self, words:list[str]):
        return [word for word in words if (('http' not in word) and ('https' not in word) and  ('www' not in word))]
    
    def preprocessing(self, text:str):
        text = self.fix_codification(text)
        text = self.to_lowercase(text)
        text = self.replace_accents(text)
        text = self.remove_characters(text)
        words = self.remove_stopwords(text)
        words = self.remove_no_alphabetics(words)
        words = self.lemmatize(words)
        words = self.remove_routes(words)
        return ' '.join(words)
    
    def fit(self, data, target=None):
        self.df = data
        if self.isTraining:
            self.df['Language'] = self.df['Textos_espanol'].apply(self.detect_language)
        self.df['Textos_espanol'] = data['Textos_espanol'].apply(self.preprocessing)
        if self.isTraining:
            self.df = self.df[self.df['Language']=='es']
            self.df = self.df.drop(['Language'], axis = 1)
        print('[CleaningTrain] Fitting Finished!!')
        return self
    
    def transform(self, data):
        del self.df
        self.df = data
        self.df['Textos_espanol'] = data['Textos_espanol'].apply(self.preprocessing)
        if self.isTraining:
            self.df = self.df[self.df['Language']=='es']
            self.df = self.df.drop(['Language'], axis = 1)
        print('[CleaningTrain] Transformation Finished!!')
        return self.df
    
    def predict(self, data):
        return self


class Vectorizer:

    def __init__(self, isTraining = False):
        self.vectorizer = TfidfVectorizer()
        self.isTraining = isTraining
        self.vector = None
        self.data = None

    def getVectorWeights(self, data):
        vectorizer = TfidfVectorizer()
        vector = vectorizer.fit_transform(data['Textos_espanol'])
        vectorizer.get_feature_names_out()
        vect_score = np.asarray(vector.mean(axis=0)).ravel().tolist()
        vect_array = pd.DataFrame({'term': vectorizer.get_feature_names_out(), 'weight': vect_score})
        vect_array.sort_values(by='weight',ascending=False,inplace=True)
        return vect_array

    def setImpact(self, df):
        df3 = df[df['sdg'] == 3]
        df4 = df[df['sdg'] == 4]
        df5 = df[df['sdg'] == 5]

        self.impact3 = self.getVectorWeights(df3)
        self.impact4 = self.getVectorWeights(df4)
        self.impact5 = self.getVectorWeights(df5)
    
    def fit(self, data , target = None):
        self.setImpact(data)
        X =  self.vectorizer.fit_transform(data['Textos_espanol'])
        self.data = pd.DataFrame(X.todense())
        self.data['sdg'] = data['sdg']
        print('[Vectorizer] Fitting Finished!!')
        return self

    def transform(self, data):
        self.vector = self.vectorizer.transform(data['Textos_espanol'])
        transformed_data = pd.DataFrame(self.vector.todense(), columns=self.vectorizer.get_feature_names_out())
        if self.isTraining:
            transformed_data['sdg'] = data['sdg'].values
        print('[Vectorizer] Transformation Finished!!')
        return transformed_data
        
    def predict(self, data):
        return self 
    

class Model():

    def __init__(self):
        self.model = RandomForestClassifier(random_state=42, max_depth=30, min_samples_split=15, n_estimators=300)
        self.precision = None
        self.recall = None
        self.report = None
        self.f1 = None
    
    def fit(self, data, target=None):
        Y = data['sdg']
        X = data.drop(['sdg'], axis = 1)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
        self.model.fit(X_train, Y_train)
        Y_test_predict = self.model.predict(X_test)
        self.report = classification_report(Y_test, Y_test_predict)
        self.f1 = f1_score(Y_test, Y_test_predict, average='weighted')
        self.recall = recall_score(Y_test, Y_test_predict, average='weighted')
        self.precision = precision_score(Y_test, Y_test_predict, average='weighted')
        print('[Model] Model Trained!!')
        return self
    
    def transform(self, data):
        return data
    
    def predict(self, data):
        labels = self.model.predict(data)
        probabilities = self.model.predict_proba(data)
        prediction = pd.DataFrame(labels, columns=['label'])
        for i in range(probabilities.shape[1]):
            prediction[f'prob_class_{i}'] = probabilities[:, i]
        print('[Model] Predictions Done!!')
        return prediction


        





    



        
        







    

    


        

