from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from anthropic import Anthropic
import streamlit as st
from langchain_chroma import Chroma

client = Anthropic()

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


