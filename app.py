from langchain_community.embeddings import HuggingFaceEmbeddings
from anthropic import Anthropic
import streamlit as st
from langchain_chroma import Chroma

client = Anthropic()

@st.cache_resource
def load_vector_store():
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.schema import Document
    
    with open("jpm-10K-small-clean.txt", "r") as f:
        text = f.read()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)
    docs = [Document(page_content=chunk) for chunk in chunks]
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = Chroma.from_documents(docs, embeddings)
    retriever = vector_store.as_retriever()
    return retriever
  
def ask_loanbot(question):
    retriever = load_vector_store()
    retrieved_docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": f"""Act as a legal loan document assistant. Answer the question using only the context provided.
                If the answer is not in the context, say "I don't have that information in the document". Don't make up any answers, strictly stick to the context given to you."

                Context:
                {context}
                
                Question: {question}"""
            }
        ]
    )

    return message.content[0].text, retrieved_docs


st.title("SEC Document Assistant")
input = st.text_input("Type your question")
if st.button("Ask"):
    response, retrieved_docs = ask_loanbot(input)
    st.write(response)
    with st.expander("Retrieved Docs"):
        st.write(retrieved_docs)


