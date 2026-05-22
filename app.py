import chromadb
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from anthropic import Anthropic
import streamlit as st
from langchain_chroma import Chroma

@st.cache_resource

def load_vector_store():
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    # connect to chroma
    vector_store = Chroma(
        collection_name="loanbot",
        embedding_function=embeddings,
        persist_directory="./chroma_db"
    )
    # return the retriever
    retriever = vector_store.as_retriever()
    return retriever
  
