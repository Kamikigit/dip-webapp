from fastapi import FastAPI
from fastapi import File, UploadFile
from fastapi.responses import HTMLResponse
import os
import uuid
import model
import shutil
import pandas as pd
import base64
app = FastAPI()
@app.get('/')
def root():
    return {"text": "Hello World."}

@app.post("/upload")
async def uploaded(in_file:UploadFile = File(...)):
    print("reading file")
    filename = f"{str(uuid.uuid1())}.csv"
    path = os.path.join("./storage", filename)
    # ファイルに書き込む
    fout = open(path, 'wb')
    while 1:
        chunk = await in_file.read(100000)
        if not chunk:
            break
        fout.write(chunk)
    fout.close()
    # 推論中
    df = batch_predict(filename)
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return {"csv": b64}

def batch_predict(filename: str):
    ml = model.PredictAPI()
    pred = ml.predict(filename)
    print('finished prediciton')
    return pred
