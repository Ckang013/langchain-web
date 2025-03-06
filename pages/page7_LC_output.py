import streamlit as st

from langchain_openai import ChatOpenAI
from langchain.output_parsers import CommaSeparatedListOutputParser, PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import Field
from pydantic import BaseModel

st.write("## LangChain 指定輸出格式")
st.write("這是用 LangChain框架 的 output_parser 去對輸出格式做調整，可以支援JSON、Markdown、YAML、XML、數列、表格")
st.divider()

## 實現功能應用
st.write("#### 色號產生器- 輸出 list格式")
st.write("輸入一個關鍵字，會產生對應的3個色號，ex. Facebook、Apple、Benz、Taipei")
openai_api_key = st.text_input("請輸入API金鑰: ", type="password")
query = st.text_input("請輸入要產生色號的關鍵字: ")
color_btn = st.button("產生色號")

prompt = ChatPromptTemplate.from_messages([
    ("system", "{parser_instructions}"),     # 指定輸出格式
    ("human", "列出3個{subject}色系的十六進制顏色碼")
])
output_parser = CommaSeparatedListOutputParser()
parser_instructions = output_parser.get_format_instructions()
final_prompt = prompt.invoke({"subject": query, "parser_instructions": parser_instructions})

if color_btn and not openai_api_key:
    st.warning("請輸入金鑰")
if color_btn and not query:
    st.warning("請輸入關鍵字")
if color_btn and openai_api_key and query:
    model = ChatOpenAI(model="gpt-4o-mini", api_key=openai_api_key)
    with st.spinner("產生中..."):
        response = model.invoke(final_prompt)
    st.write("生成色號如下")
    st.write(output_parser.invoke(response))

## 實現功能應用
st.divider()
st.write("#### 暢銷書的資訊- 輸出 JSON格式")
st.write("讓模型去找出近期的暢銷書並提供書的名稱、作者、類型")
book_btn = st.button("查詢近期熱門的兩款書")

class BookInfo(BaseModel):
    book_name:str = Field(description="書籍的名稱", example="哈利波特")
    author_name:str = Field(description="書籍的作者", example="JK羅琳")
    genres:str = Field(description="書籍的類型", example="奇幻小說")

output_parser_2 = PydanticOutputParser(pydantic_object=BookInfo)

prompt_2 = ChatPromptTemplate.from_messages([
    ("system", "{parser_instructions_2}"),
    ("human", "請給我近期熱門的兩款書，並提供書名、作者、書籍類型")
])
final_prompt_2 = prompt_2.invoke({"parser_instructions_2": output_parser_2.get_format_instructions()})

if book_btn and openai_api_key:
    model = ChatOpenAI(model="gpt-4o-mini", api_key=openai_api_key)
    with st.spinner("查詢中..."):
        response = model.invoke(final_prompt_2)
    st.write("生成的書如下: ")
    st.write(output_parser.invoke(response))