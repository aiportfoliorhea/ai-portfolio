from langgraph.graph import StateGraph, END
from typing import TypedDict
from anthropic import Anthropic
from retriever import load_vector_store

# 1. Define state
class SecRagState(TypedDict):
    question: str
    rewritten_query: str
    retrieved_docs: list
    answer: str

# 2. Query rewriter node
def rewrite_query(state: SecRagState) -> SecRagState:
    client = Anthropic()
    
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=256,
        messages=[{
            "role": "user",
            "content": f"""Rewrite this question to be a better search query for retrieving relevant chunks from a JPMorgan 10-K SEC filing. 
Return only the rewritten query, nothing else.

Question: {state['question']}"""
        }]
    )
    state["rewritten_query"] = response.content[0].text.strip()
    return state

# 3. Retrieval node
def retrieve(state: SecRagState) -> SecRagState:
    retriever = load_vector_store()
    docs = retriever.invoke(state["rewritten_query"])
    state["retrieved_docs"] = docs
    return state

# 4. Answer node
def generate_answer(state: SecRagState) -> SecRagState:
    context = "\n\n".join([d.page_content for d in state["retrieved_docs"]])
    client = Anthropic()
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        system="Act as a SEC filing assistant. Answer the question using only the context provided. If the answer is not in the context, say 'I don't have that information in the document'",
        messages=[{
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {state['question']}\nAnswer:"
        }]
    )
    state["answer"] = response.content[0].text.strip()
    return state

# 5. Build graph
def build_rag_graph():
    graph = StateGraph(SecRagState)
    graph.add_node("rewrite", rewrite_query)
    graph.add_node("retrieve", retrieve)
    graph.add_node("generate", generate_answer)
    graph.set_entry_point("rewrite")
    graph.add_edge("rewrite", "retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)
    
    return graph.compile()