from anthropic import Anthropic
import streamlit as st
from graph import build_rag_graph
from retriever import load_vector_store

client = Anthropic()
rag_graph = build_rag_graph() 

def ask_loanbot(question):
    result = rag_graph.invoke({"question": question})
    return result["answer"], result["retrieved_docs"], result["rewritten_query"]


st.title("SEC Document Assistant")
input = st.text_input("Type your question")
if st.button("Ask"):
    response, retrieved_docs, rewritten_query = ask_loanbot(input)
    st.write(response)
    with st.expander("Retrieved Docs"):
        st.write(retrieved_docs)
    st.write("Rewritten query:", rewritten_query)
