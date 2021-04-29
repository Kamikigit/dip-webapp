from fastapi import FastAPI
from fastapi import File, UploadFile
from fastapi.responses import HTMLResponse
import os
import uuid
import model
import shutil
import pandas as pd
import base64
import io
app = FastAPI()
@app.get('/')
def root():
    return {"text": "Hello World."}

@app.post("/upload")
async def uploaded(in_file:bytes = File(...)):

    df = pd.read_csv(io.BytesIO(in_file), encoding='utf-8')
    # 推論中
    df = predict(df)
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return {"csv": b64}

def predict(df):
    pred = model.serving(df)
    print('finished prediciton')
    return pred
