from fastapi import FastAPI
from fastapi.responses import JSONResponse
import subprocess
import pandas as pd
import os

app = FastAPI()

# 1. Endpoint scraping
@app.get("/run-scraping")
def run_scraping():
    try:
        result = subprocess.run(["python", "app/scraping.py"], capture_output=True, text=True)
        return {"status": "success", "message": result.stdout}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

# 2. Endpoint hasil scraping
@app.get("/data")
def read_data():
    try:
        df = pd.read_csv("data/dataset.csv")
        return df.to_dict(orient="records")
    except FileNotFoundError:
        return JSONResponse(status_code=404, content={"status": "error", "message": "File tidak ditemukan"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

# 3. Endpoint topic modeling
@app.get("/run-topic-modeling")
def run_topic_modeling():
    try:
        result = subprocess.run(["python", "app/modelling.py"], capture_output=True, text=True)
        return {"status": "success", "message": result.stdout}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
