import streamlit as st

from langchain.memory import ConversationBufferMemory
from utils import qa_agent

st.title("AI智能PDF問答工具")
st.write("結合LangChain的 記憶Memory、檢索增強生成RAG")

with st.sidebar:
    openai_api_key = st.text_input("請輸入OpenAI API金鑰: ", type="password")

# 當對話裡沒有 memory時，去初始化 memory
if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(
        return_messages=True,
        memory_key="chat_history",
        output_key="answer"
    )

uploaded_file = st.file_uploader("上傳妳的PDF文件: ", type="pdf")
question = st.text_input("對PDF的內容進行提問", disabled=not uploaded_file) # 當沒有上傳PDF，就無法輸入

if uploaded_file and question and not openai_api_key:
    st.info("請輸入妳的OpenAI API金鑰")
if uploaded_file and question and openai_api_key:
    with st.spinner("AI正在思考中，請稍後..."):
        response = qa_agent(openai_api_key, st.session_state["memory"], uploaded_file, question)

    st.write("### 答案")
    st.write(response["answer"])
    st.session_state["chat_history"] = response["chat_history"]

## 顯示歷史訊息
if "chat_history" in st.session_state:
    with st.expander("歷史訊息"):
        for i in range(0, len(st.session_state["chat_history"]), 2):
            human_message = st.session_state["chat_history"][i]
            ai_message = st.session_state["chat_history"][i+1]
            st.write(human_message.content)
            st.write(ai_message.content)
            if i < len(st.session_state["chat_history"]) - 2:
                st.divider()