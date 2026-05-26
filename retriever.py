from langchain_community.embeddings import HuggingFaceEmbeddings
import streamlit as st
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

@st.cache_resource
def load_vector_store():
    with open("jpm-10K-small-clean.txt", "r") as f:
        text = f.read()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)
    docs = [Document(page_content=chunk) for chunk in chunks]
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = Chroma.from_documents(docs, embeddings)
    retriever = vector_store.as_retriever()
    return retriever