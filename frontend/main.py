import streamlit as st
import requests

st.title("推論web app")

upfile = st.file_uploader("ファイルを選択して下さい")
start = st.button("スタート")

if start:
    if upfile is not None:
        files = {"file": upfile.getvalue()}
        res = requests.post(f"http://backend:8080/{style}", files=files)
        file_path = res.json()

        st.write("推論中です・・・")

    
