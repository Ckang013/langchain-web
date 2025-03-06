from openai import OpenAI
import streamlit as st

st.write("## LLM 文本生成")
st.write("生成一段模型創造出來的故事或小說內容")
st.write("參數temperature 數字越大，模型的創造力越高，回答的內容更天馬行空")
st.write("參數max_token 可以限制模型回答的字數，不然回答的token太長，花費的費用也越多")
st.divider()

## 實現功能應用
model_list = ["gpt-3.5-turbo", "gpt-4o-mini"]
model_select = st.selectbox("請選擇一個模型", model_list, index=1)
openai_api_key = st.text_input("請輸入金鑰: ", type="password")
story = st.text_area("請提供想生成的故事內容: ")
number = st.slider("請設定模型的 temperature 參數", min_value=0.0, max_value=2.0, value=1.5, step=0.1)
story_length = st.number_input("請輸入模型回傳的最大token數: ", value=200, min_value=100, max_value=500, step=100)
submitted = st.button("開始生成故事")

def generate_text(api_key, model, text, temp, length):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model= model,
        messages=[
            {"role": "user", "content": f"根據這段文字生成一個故事: \n{text}"}
        ],
        temperature= temp,
        max_tokens= length
    )
    return response.choices[0].message.content

if submitted and not openai_api_key:
    st.info("請輸入OpenAI API Key")
if submitted and not story:
    st.info("請輸入要做摘要總結的文字")
if submitted and openai_api_key and story:
    try:
        with st.spinner("AI生成中..."):
            generate = generate_text(openai_api_key, model_select, story, number, story_length)
        st.write("生成的故事如下: ")
        st.write(generate)
    except Exception as e:
        st.error(f"有錯誤: {e}")