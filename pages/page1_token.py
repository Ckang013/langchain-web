import streamlit as st
import tiktoken

st.write("## 計算 token 數")
st.write("#### token 是什麼?")
st.write("電腦看不懂文字，所以會將這些文字轉換成由數字組成的數列，這些被稱為 token，並不是每一個文字"
         "都只有一組 token，有些字轉換後會用多個 token 來表示，在轉換時也會需要指定模型，這裡使用的是 gpt-3.5-turbo，但計算不需要額外的成本費用")
st.divider()

text = st.text_area("請輸入要計算和轉換的文字")
if text:
    st.write(f"你想轉換的文字是: {text}")

encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
tokens = encoding.encode(text)
st.write(f"轉換後的 token 為: {tokens}")
st.write(f"token 長度為 : {len(tokens)}")