import streamlit as st
import requests

st.title("推論web app")

upfile = st.file_uploader("ファイルを選択して下さい", type="csv")
start = st.button("スタート")

if start:
    if upfile is not None:
        files = {"in_file": upfile.getvalue()}
        res = requests.post(f"http://backend:8080/upload", files=files)
        # st.write("推論を開始します")
        #ダウンロード
        b64 = res.json()["csv"]
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="result.csv">download</a>'
        st.markdown(f"推論結果をダウンロードする {href}", unsafe_allow_html=True)
