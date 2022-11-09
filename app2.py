
from fastapi import FastAPI, File, UploadFile
from activity.constant.application import APP_HOST, APP_PORT
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from activity.pipeline.prediction_pipeline import PredictionPipeline

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


@app.post("/predict")
async def predict_route(csv_file: UploadFile = File(...)):
    try:
       
        df = pd.read_csv(csv_file.file)
        prediction_pipeline = PredictionPipeline()
        predictions = prediction_pipeline.predict_from_s3(df)
        if not predictions:
            return Response("Model is not available")
        return { "prediction": predictions}
        
    except Exception as e:
        raise Response(f"Error Occured! {e}")


if __name__ == '__main__':
    app_run(app, host=APP_HOST, port=APP_PORT)
