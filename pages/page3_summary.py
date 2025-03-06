from openai import OpenAI
import streamlit as st

st.write("## LLM 文本摘要總結")
st.write("將一段用戶針對店家所留下的google評論，做文本摘要將正面的優點，以及負面的缺點，給總結出來")
st.write("參數temperature 預設為1，數字越低模型的回答越相關越穩定")
st.divider()

## 評論範例參考
st.write("#### 評論參考範例")
st.write("ex. 店內的用餐環境非常寬敞，還有坐墊讓人坐的更舒適，點餐系統很方便，抽油煙的管子就隱藏在炭火爐旁，燒烤的油煙不外露，"
         "燒烤時不會整間店煙霧瀰漫，吃完燒烤後也不會全身上下滿滿的烤肉味，真的設計得很用心，不像有些燒肉店，爐子就放在桌上，必須"
         "要把手抬高才能用烤肉夾來夾肉翻肉，整場烤完腰痠背痛，手都快舉不起來。")

## 實現功能應用
model_list = ["gpt-3.5-turbo", "gpt-4o-mini"]
model_select = st.selectbox("請選擇一個模型", model_list, index=1)
openai_api_key = st.text_input("請輸入金鑰: ", type="password")
summary_text = st.text_area("請輸入要做摘要的google評論: ")
number = st.slider("請設定模型的 temperature 參數", min_value=0.0, max_value=2.0, value=0.5, step=0.1)
submitted = st.button("開始摘要")

def summarize_text(api_key, model, text, temp):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model= model,
        messages=[
            {"role": "system", "content": "你的任務是要將用戶的針對店家或產品的評價做摘要總結，並分成兩個部分，一個是優點或是正面的評價，另一個是缺點或是負面的評價"},
            {"role": "user", "content": f"請幫我摘要總結這段評論: \n{text}"}
        ],
        temperature=temp     # 隨機性設定低一點，回答的創造力越低，回答越嚴謹
    )
    return response.choices[0].message.content

if submitted and not openai_api_key:
    st.info("請輸入OpenAI API Key")
if submitted and not summary_text:
    st.info("請輸入要做摘要總結的文字")
if submitted and openai_api_key and summary_text:
    try:
        with st.spinner("模型正在摘要總結，請稍後..."):
            summary = summarize_text(openai_api_key, model_select, summary_text, number)
        st.write("總結出來的結果如下: ")
        st.write(summary)
    except Exception as e:
        st.error(f"發生錯誤: {e}")