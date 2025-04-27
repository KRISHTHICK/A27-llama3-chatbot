# Install first if you haven't:
# pip install streamlit chromadb langchain ollama

import streamlit as st
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import os

# 1. Load documents (you can replace 'sample.txt' with any local file)
loader = TextLoader("sample.txt")
documents = loader.load()

# 2. Split documents into chunks
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

# 3. Create embeddings using Ollama
embedding_model = OllamaEmbeddings(model="nomic-embed-text")  # Run this model locally in Ollama

# 4. Store embeddings in ChromaDB
vector_store = Chroma.from_documents(texts, embedding_model)

# 5. Create RAG chain
ollama_llm = Ollama(model="llama3")  # Local model like Llama3
rag_chain = RetrievalQA.from_chain_type(
    llm=ollama_llm,
    retriever=vector_store.as_retriever()
)

# 6. Streamlit UI
st.title("🔍 Simple RAG Chatbot (Ollama + Streamlit)")

user_question = st.text_input("Ask a question based on document:")

if st.button("Get Answer") and user_question:
    answer = rag_chain.run(user_question)
    st.success(answer)

st.caption("Powered by Ollama (Local LLM)")
