from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

def qa_agent(openai_api_key, memory, uploaded_file, question):
    model = ChatOpenAI(model="gpt-3.5-turbo", api_key=openai_api_key)
    file_content = uploaded_file.read()
    temp_file_path = "law.pdf"
    with open(temp_file_path, "wb") as temp_tile:
        temp_tile.write(file_content)
    loader = PyPDFLoader(temp_file_path)
    docs = loader.load()

    # 文本切割
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=30,
        separators=["\n", "。", "!", "?", ",", "、", ""]
    )
    texts = text_splitter.split_documents(docs)

    # 向量資料庫
    embeddings_model = OpenAIEmbeddings(api_key=openai_api_key)
    db = FAISS.from_documents(texts, embeddings_model)

    # 檢索器
    retriever = db.as_retriever()

    qa = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=retriever,
        memory=memory
    )
    response = qa.invoke({"chat_history": memory, "question": question})
    return response