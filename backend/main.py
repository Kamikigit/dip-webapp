from fastapi import FastAPI, Request, BackgroundTasks
from fastapi import File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import uuid
# import model
import shutil
app = FastAPI()

@app.get('/')
def root():
    return {"text": "Hello World."}

# ファイルを保存する
@app.post("/{style}")
def uploaded(style: str, in_file:UploadFile = File(...)):
    number = uuid.uuid1()
    filename = str(number) + '.csv'
    # path = os.path.join("../uploaded", filename)
    # async with open(path, 'wb') as out_file:
    #     out_file.copyfileobj(in_file.file, out_file)
    form = await request.form()
    uploadfile = form['content']

    ファイルに書き込む
    fout = open(path, 'wb')
    while 1:
        chunk = await uploadfile.read(100000)
        if not chunk:
            break
        fout.write(chunk)
    fout.close()
    return {"filename": contents}
    # return {"number": number}


# バックグラウンドで推論中
def batch_predict(filename: str):
    ml = model.PredictAPI()
    pred = ml.predict(filename)
    print('finished prediciton')

# @app.get('/{style}')
# async def batch_prediction(request: Request, style: str, background_tasks: BackgroundTasks):
#     # if io.check_outputs(filename):
#     #     raise HTTPException(status_code=404, detail="the result of prediction already exists")
#     print("predicting....")
#     filename = os.path.join("../uploaded", filename)
#     background_tasks.add_task(batch_predict, filename)
#     return templates.TemplateResponse("predicting.html", {"request": request})

# # ダウンロードする
# @app.get('/download')
# async def download(filename: str):
#     downloadfile = os.path.join("./downloads", filename)

#     return templates.TemplateResponse("download.html", {"request": request})
