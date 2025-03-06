from idlelib.rpc import response_queue

import streamlit as st
from openai import OpenAI
import pandas as pd

## 頁面介紹
st.write("## 對 ChatGPT 發起詢問")
st.write("這個應用就是把 GPT 的模型引入進來直接在這裡使用，與官網提供的詢問結果會是一樣的，"
         "唯一不一樣的地方就是在這裡發問需要連結自己的金鑰，支付額外的token使用成本^^")
st.divider()

## 模型介紹
st.write("#### 模型介紹")
st.write("這裡簡單列出幾個模型和相關的資訊，還有其他很多的執行不同任務的模型，可以參考OpenAI官網")
df = pd.DataFrame({
    "模型": ["GPT-3.5 Turbo", "GPT-4.5 Preview", "GPT-4o Mini", "o3-mini"],
    "收費(每百萬個token 輸入)": ["$ 0.5", "$ 75", "$ 0.15", "$ 1.1"],
    "收費(每百萬個token 輸出)": ["$ 1.5", "$ 75", "$ 1.20", "$ 4.5"],
    "描述": ["版本較舊、較便宜的聊天模型", "最新最強的模型，高情感、高智能、高創造力", "經濟實惠的小型智能模型，適合快速、輕量級任務",
             "快速靈活的推理模型，適合處理複雜、多步驟的任務"]
})
st.table(df)

## 實現功能應用
model_list = ["gpt-3.5-turbo", "gpt-4o-mini", "o3-mini"]
model_select = st.selectbox("請選擇一個模型", model_list, index=0)
openai_api_key = st.text_input("請輸入金鑰: ", type="password")
query_question = st.text_input("請輸入要詢問GPT的問題: ")
submitted = st.button("送出提問")

client = OpenAI(api_key=openai_api_key)

if submitted and not openai_api_key:
    st.info("請輸入API KEY !")
if submitted and not query_question:
    st.info("請輸入要詢問的問題 !")

if submitted and openai_api_key and query_question:
    st.write(f"你提出的問題是: {query_question}")
    with st.spinner("模型正在思考中，請稍後..."):
        response = client.chat.completions.create(
            model= model_select,
            messages=[
                {"role": "user", "content": query_question}
            ]
        )

    st.write(f"GPT的回答: {response.choices[0].message.content}")