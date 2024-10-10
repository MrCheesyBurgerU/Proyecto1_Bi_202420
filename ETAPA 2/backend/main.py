from fastapi import FastAPI, File, Response, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from DataModel import DataModel
from joblib import load, dump

import pandas as pd
import json
import os


app = FastAPI()
pipeline = load('./assets/model.joblib')

origins = ['http://localhost/8000',
           'http://localhost:5173',
           'http://localhost:3000',
           'http://127.0.0.1:8000']

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)


@app.post('/predict_input')
def makePredictionInput(dataModel : DataModel):
    print("[Predict Input] Procces Started")
    data = dataModel.model_dump()
    df = pd.DataFrame([data], columns = dataModel.columns())
    pipeline.named_steps['cleaner'].isTraining = False
    pipeline.named_steps['vectorizer'].isTraining = False
    pred_df = pipeline.predict(df)
    score = max(pred_df.loc[0, 'prob_class_0'], pred_df.loc[0, 'prob_class_1'], pred_df.loc[0, 'prob_class_2'])
    print("[Predict Input] Procces Finished")
    return {'prediction': int(pred_df.loc[0,'label']), 'score': score}


@app.post('/predict_file')
async def makePredictionCsv(file: UploadFile = File(...)):

    print("[Predict File] Procces Started")

    _, file_extension = os.path.splitext(file.filename)

    if file_extension not in ['.csv', '.xlsx']:
        return JSONResponse(status_code=400, content={"message": "Invalid file type. Please upload a CSV or XLSX file."})

    try:
        if file_extension == '.csv':
            dataframe = pd.read_csv(file.file)
        elif file_extension == '.xlsx':
            dataframe = pd.read_excel(file.file)
        
        pipeline.named_steps['cleaner'].isTraining = False
        pipeline.named_steps['vectorizer'].isTraining = False
        pred_df = pipeline.predict(dataframe)
        labels = pred_df['label']
        scores = [float(max(pred_df.loc[i, 'prob_class_0'], pred_df.loc[i, 'prob_class_1'], pred_df.loc[i, 'prob_class_2'])) for i in range(pred_df.shape[0])]
        final_df = pd.DataFrame({'Textos_espanol': dataframe['Textos_espanol'],'sdg': labels,'score': scores})
        output_dir = os.path.join(os.getcwd(), 'data')
        output_filename = 'predictions_' + file.filename
        output_path = os.path.join(output_dir, output_filename)
        if file_extension == '.csv':
            final_df.to_csv(output_path, index=False, sep=',', encoding='utf-8-sig')
            print("[Predict File] Procces Finished")
            return FileResponse(output_path, media_type='text/csv', filename=output_filename)

        elif file_extension == '.xlsx':
            final_df.to_excel(output_path, index=False)
            print("[Predict File] Procces Finished")
            return FileResponse(output_path, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=output_filename)

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "An error occurred while processing the file.", "error":str(e)})


@app.post('/retrain')
async def retrainModel(file: UploadFile = File(...)):

    print("[Retrain] Procces Started")

    _, file_extension = os.path.splitext(file.filename)

    if file_extension not in ['.csv', '.xlsx']:
        return JSONResponse(status_code=400, content={"message": "Invalid file type. Please upload a CSV or XLSX file."})

    try:
        if file_extension == '.csv':
            new_dataframe = pd.read_csv(file.file)
        elif file_extension == '.xlsx':
            new_dataframe = pd.read_excel(file.file)
        
        original_data_path = './data/ODScat_345.xlsx'  
        if os.path.exists(original_data_path):
            original_dataframe = pd.read_excel(original_data_path)
        else:
            return JSONResponse(status_code=404, content={"message": "Original data file not found."})

        combined_dataframe = pd.concat([original_dataframe, new_dataframe], ignore_index=True)
        pipeline.named_steps['cleaner'].isTraining = True
        pipeline.named_steps['vectorizer'].isTraining = True
        pipeline.fit(combined_dataframe)
        dump(pipeline, './assets/model.joblib', compress=True)

        print("[Retrain] Procces Finished")

        return JSONResponse(status_code=200, content={"message": "Model retrained successfully!"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "An error occurred while processing the file.", "error":str(e)})


@app.get('/report')
def getReport():

    print("[Report] Procces Started")

    answer = {
              'f1': pipeline['model'].f1, 
              'precision': pipeline['model'].precision, 
              'recall': pipeline['model'].recall}
    
    print("[Report] Procces Finished")
    return Response(content=json.dumps(answer), media_type='application/json', headers={'Access-Control-Allow-Origin': '*'})


@app.get("/words_relevance/{id}")
def getWordsRelevance(id: int):

    print("[Words Relevance] Procces Started")

    variables = {3: pipeline['vectorizer'].impact3,
                 4: pipeline['vectorizer'].impact4,
                 5: pipeline['vectorizer'].impact5}
    
    vect_array = variables[id]
    vect_array.rename(columns={'term': 'text'}, inplace=True)
    vect_array.rename(columns={'weight': 'value'}, inplace=True)
    vect_array = vect_array.to_json(orient='records')

    print("[Words Relevance] Procces Finished")

    return Response(content=vect_array, media_type='application/json', headers={'Access-Control-Allow-Origin': '*'})





