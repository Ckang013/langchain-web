from openai import OpenAI
import streamlit as st

st.write("## LLM 文本分類")
st.write("文本分類對於公司第一線人員，也就是客服人員來說是個很棒的工具，當今天用戶在官網平台上輸入針對產品想問的問題，可以直接先做文本分類，將用戶的問題歸類到"
         "特定類別，等後續再由能夠回覆這類問題的內部人員來做回應，假設是被分類到較專業的問題類別，就由研發的工程師做回覆，如果是分類到較簡易的問題類別，就可以"
         "直接由客服人員做回覆")
st.divider()

st.write("#### 應用範例")
st.write("這裡的練習假設是針對汽車品牌的客戶提問，問題的類別有「產品規格」「功能比較」「操作說明」「價格查詢」「故障問題」「其他」")
st.write("ex: ")
st.write("這台車和其他公司相同價位區間的車的差別。\n"
         "這台車的原定價格是多少，優惠期間的價格又是多少。\n"
         "我要如何啟用車子的夜間輔助駕駛功能。\n"
         "這台車動力十足，開起來很舒服，讚。")

## 實現功能應用
model_list = ["gpt-3.5-turbo", "gpt-4o-mini"]
model_select = st.selectbox("請選擇一個模型", model_list, index=1)
openai_api_key = st.text_input("請輸入金鑰: ", type="password")
questions = st.text_area("請輸入要做分類的客戶問題 (每個問題之間用 句號「。」做區隔): ")
submitted = st.button("開始分類")

category_list = ["產品規格", "功能比較", "操作說明", "價格查詢", "故障問題", "其他"]
prompt_template = """
你的任務是將客戶提出的問題進行分類，確認這些問題是這些類別中的哪一個: {categories}
客戶的問題是 {question}
"""

def classify_questions(api_key, model, prompt):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

if submitted and not openai_api_key:
    st.info("請輸入api key")
if submitted and not questions:
    st.info("請輸入要分類的問題")
if submitted and openai_api_key and questions:
    q_list = questions.split("。")
    st.write("分類的結果如下: ")
    for q in q_list:
        with st.spinner("分類中..."):
            format_prompt = prompt_template.format(categories=",".join(category_list), question=q)
            class_ = classify_questions(openai_api_key, model_select, format_prompt)
            st.write(class_)