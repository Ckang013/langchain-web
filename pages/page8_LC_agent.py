import re
import streamlit as st

from langchain import hub
from langchain.agents import create_structured_chat_agent, AgentExecutor, initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_experimental.tools import PythonREPLTool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

st.write("## LangChain Agent調用工具")
st.write("Agent叫做智能代理，可以串接各種工具來使用，ex.企業內部資料庫、企業內部文檔、Python編譯器、Wikipedia、API"
         "並針對用戶提問的不同，選擇應該調用哪一種工具來做查詢及回答")

st.write("##### 工具1: Python數學計算、工具2: example.csv文件、工具3: 維基百科")
st.write("可以輸入的指令如下:")
st.write("ex. 計算25的平方加13")
st.write("ex. 蔡英文的生日是哪一天")
st.write("ex. 幫我查example.csv裡面的價格平均值")
st.image("./example.png")
st.divider()

openai_api_key = st.text_input("請輸入API金鑰: ", type="password")
text_query = st.text_input("輸入問題: ")
btn = st.button("提問")

## 工具一 計算數字，初始化
python_tool = PythonREPLTool()

## 工具三 Wikipedia，初始化
wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)
prompt = hub.pull("hwchase17/structured-chat-agent")    # ReAct 的 Prompt

if btn and openai_api_key and text_query:
    ## 工具二 CSV執行器
    csv_agent_executor = create_csv_agent(
        llm=ChatOpenAI(model="gpt-4o-mini", api_key=openai_api_key),
        path="./example.csv",
        verbose=True,
        agent_executor_kwargs={"handle_parsing_errors": True},      # 避免解析錯誤
        allow_dangerous_code=True   # 允許執行 Python代碼
    )

    tools = [
        python_tool,
        Tool(
            name="CSV分析工具",
            description="當需要回答有關example.csv文件的問題時，使用這個工具",
            func=csv_agent_executor.invoke
        ),
        Tool(
            name="維基百科查詢",
            func=wiki.run,
            description="當需要查詢維基百科上的資訊時，使用這個工具"
        )
    ]

    model = ChatOpenAI(model="gpt-4o-mini", api_key=openai_api_key)
    agent = initialize_agent(
        tools=tools,
        llm=model,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,    # 設定 Agent 的運作方式
        verbose=True
    )


    with st.spinner("計算中..."):
        response = agent.invoke({"input": text_query})
    st.write("結果如下")
    st.write(f"{response['output']}")