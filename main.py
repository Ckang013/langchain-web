import streamlit as st

st.title("Chris 的 LLM 網站")
st.write("Written by 2025.03.06")

st.write("### 說明")
st.write("這是一個練習關於LLM大語言模型的應用網站，裡面會練習到OpenAI GPT API，以及 LangChain 框架的應用，但需要請用戶自行提供使用的OPENAI_API_KEY")

st.write("#### OpenAI vs Hugging Face")
st.write("這兩個在 NLP自然語言處理的領域都很強大，但使用方面有所不同")
st.image("./compare.png")

st.write("### 頁面介紹")
st.write("##### LLM 基本應用")
st.write("1. 計算 token 數")
st.write("2. 對 ChatGPT 提問")
st.write("3. 文本摘要")
st.write("4. 文本生成")
st.write("5. 文本分類")

st.write("##### LangChain 應用")
st.write("6. 帶記憶的對話鏈")
st.write("7. 指定輸出格式")
st.write("8. 智能代理工具")
st.write("9. 檢索增強生成- PDF問答")