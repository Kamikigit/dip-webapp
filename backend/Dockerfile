FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
# コンテナ内で必要なパッケージをインストール
# RUN pip install -r requirements.txt
RUN apt update && apt install libgomp1 \
 && pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

COPY . .
EXPOSE 8080
# FastAPIを8080ポートで待機
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]