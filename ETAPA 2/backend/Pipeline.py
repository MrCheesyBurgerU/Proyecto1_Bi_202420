from Pipes import Cleaning, Vectorizer, Model
from sklearn.pipeline import Pipeline
from joblib import dump
import pandas as pd


def createPipeline(data):

    pipeline = Pipeline([
        ('cleaner', Cleaning(isTraining=True)),
        ('vectorizer', Vectorizer(isTraining=True)),
        ('model', Model())
    ])

    pipeline.fit(data)  
    dump(pipeline, './assets/model.joblib', compress=True)

if __name__ == "__main__":
    print("[Pipeline] Pipeline Started")
    df = pd.read_excel("./data/ODScat_345.xlsx")
    createPipeline(df)
    print("[Pipeline] Pipeline Finished")
