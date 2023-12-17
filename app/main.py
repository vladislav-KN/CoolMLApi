import asyncio
import time
from io import StringIO
from fastapi import FastAPI, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import numpy as np
import pandas as pd
import pathlib
import requests

from sklearn.model_selection import train_test_split

from app.base_classes.base_predict_models import Response, Message,Status
from app.config.ConfigFileLoader import ConfigFileLoader
from app.model.model_education import ModelEducator
from app.model.model_predictor import ModelPredictor


config = ConfigFileLoader.load_from_file()
app = FastAPI()

while not pathlib.Path(config.file_path).exists():
    print(f"Файл {config.file_path} не найден. Ожидание...")
    time.sleep(5)
prediction = ModelPredictor(config.file_path)
educator = ModelEducator(config.file_path)


@app.post("/predict/", response_model=Response, responses={400: {"model": Message}})
async def predict_data_from_csv(file: UploadFile):
    if file.filename.endswith(".csv"):
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode('utf-8')))

        if not('Id' in df.columns and len(df.columns) == 14):
            raise HTTPException(status_code=400, detail="Incorrect data")
        predict_df = df.drop('Id', axis=1)
        result = {'data':[]}
        for index, data in zip(df['Id'].values, prediction.predict_proba(predict_df)):
            result['data'].append( {'id': str(index), 'predict':  data})

        # Отправляем JSON-ответ

        return JSONResponse(content=result, status_code=200)
    else:
        # Если файл не CSV, возвращаем ошибку
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")




async def train_and_send_metrics(df:pd.DataFrame):
    # Замените 'целевая_переменная' на название вашей целевой переменной.
    X = df.drop('res', axis=1).drop('Id', axis=1).replace([np.inf, -np.inf], np.nan).dropna()
    y = df['res']
    # Разделите данные на обучающий и временный набор (80% данных) и оставшиеся 20% данных
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.2)
    # Затем разделите временный набор на тестовый и валидационный наборы (по 50% от временного набора)
    X_test, X_validation, y_test, y_validation = train_test_split(X_temp, y_temp, test_size=0.5)
    # Обучение модели
    await educator.retrain(X_train,y_train)
    result = educator.compute_metrics(X_test,y_test)
    csv_data = df.to_csv(index=False)
    metrics_url = (f"{config.api_url}?Accuracy={result['Accuracy']}"
                   f"&Recall={result['Recall']}&F1Score={result['F1 Score']}"
                   f"&MeanSquaredError={result['Mean Squared Error']}"
                   f"&R2={result['R2 Score']}&AucRoc={result['AUC-ROC']}"
                   f"&LogLoss={result['Log Loss']}")

    # Отправка асинхронного HTTP-запроса
    response = requests.post(metrics_url, data=csv_data)
    print("Metrics Status Code:", response.status_code)
    print("Metrics Response Content:", response.text)

@app.post("/educate_model/", response_model=Status,responses={400: {"model": Message}})
async def create_upload_file(file: UploadFile, background_tasks: BackgroundTasks):
    if file.filename.endswith(".csv"):
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode('utf-8')))
        if not('Id' in df.columns and len(df.columns) == 14):
            raise HTTPException(status_code=400, detail="Incorrect data")
        # Start the asynchronous function in the background without waiting for the result
        background_tasks.add_task(train_and_send_metrics,df)
        # Отправляем JSON-ответ
        return JSONResponse(content={"status": "OK"})
    else:
        # Если файл не CSV, возвращаем ошибку
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")