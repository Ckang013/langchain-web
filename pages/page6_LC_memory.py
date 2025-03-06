import streamlit as st

from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from  langchain.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder

st.write("## LangChain 記憶對話問答")
st.write("這是用 LangChain框架 的 ConversationChain 建立出來的具有記憶功能的對話鍊，提問一個問題，並針對AI回應的內容中再去做延伸詢問，或是再問之前告訴AI的問題")
st.divider()

## 實現功能應用
model_list = ["gpt-3.5-turbo", "gpt-4o-mini"]
model_select = st.selectbox("請選擇一個模型", model_list, index=1)
openai_api_key = st.text_input("請輸入API金鑰: ", type="password")
query = st.text_input("請輸入要詢問的問題: ")
temp = st.slider("請輸入 temperature 參數: ", value=1.0, min_value=0.0, max_value=2.0, step=0.1)
button = st.button("提問")

# 對話問答迴圈
if button and not openai_api_key:
    st.warning("請輸入api key")
if button and not query:
    st.warning("請輸入要詢問的問題")
if openai_api_key and query:
    # 初始化模型
    model = ChatOpenAI(api_key=openai_api_key, model=model_select, temperature=temp)

    # 記憶歷史對話，初始化 st.session_state
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationBufferMemory()

    # 建立 LangChain 對話鍊
    qa_chain = ConversationChain(llm=model, memory=st.session_state.memory)

    if button:
        st.write(f"你的提問是: {query}")
        with st.spinner("AI思考中..."):
            response = qa_chain.run(query)
            st.write(f"AI的回答是: {response}")

        # 顯示對話歷史
        st.subheader("對話歷史")
        st.write(st.session_state.memory.buffer)