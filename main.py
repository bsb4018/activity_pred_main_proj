from activity.configuration.mongo_db_connection import MongoDBClient
from activity.exception import ActivityException
from activity.logger import logging
from activity.pipeline import train_pipeline
from activity.pipeline.train_pipeline import TrainPipeline
from activity.utils.main_utils import read_yaml_file
from activity.constant.training_pipeline import SAVED_MODEL_DIR
from fastapi import FastAPI, File, UploadFile
from activity.constant.application import APP_HOST, APP_PORT
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.responses import Response
from activity.ml.model.estimator import ModelResolver,TargetValueMapping
from activity.utils.main_utils import load_object
from fastapi.middleware.cors import CORSMiddleware
import os
import pandas as pd


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train_route():
    try:

        train_pipeline = TrainPipeline()
        if train_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")
        train_pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")



@app.post("/predict")
async def predict_route(csv_file: UploadFile = File(...)):
    try:

        df = pd.read_csv(csv_file.file)
        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
        if not model_resolver.is_model_exists():
            return Response("Model is not available")
        
        best_model_path = model_resolver.get_best_model_path()
        model = load_object(file_path=best_model_path)
        y_pred = model.predict(df)
        df['predicted_column'] = y_pred
        df['predicted_column'].replace(TargetValueMapping().reverse_mapping(),inplace=True)
        prediction_result = df['predicted_column'].tolist()
        
        return { "prediction": prediction_result}
        
    except Exception as e:
        raise Response(f"Error Occured! {e}")


if __name__ == '__main__':
    app_run(app, host=APP_HOST, port=APP_PORT)
