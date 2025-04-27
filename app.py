# Install first if you haven't:
# pip install streamlit chromadb langchain ollama pypdf

import streamlit as st
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import tempfile

# Helper function to load and split PDFs
def load_and_split_pdfs(uploaded_files):
    documents = []
    for file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file.read())
            loader = PyPDFLoader(tmp.name)
            documents.extend(loader.load())
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return text_splitter.split_documents(documents)

# Cache vector store to avoid recomputing every reload
@st.cache_resource
def create_vector_store(texts):
    embedding_model = OllamaEmbeddings(model="nomic-embed-text")
    return Chroma.from_documents(texts, embedding_model)

# UI Start
st.set_page_config(page_title="RAG Chatbot", layout="wide")
st.title("🔍 Multi-PDF RAG Chatbot (Ollama + Streamlit)")

# Upload PDFs
uploaded_files = st.sidebar.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    with st.spinner("Processing documents..."):
        texts = load_and_split_pdfs(uploaded_files)
        vector_store = create_vector_store(texts)
        retriever = vector_store.as_retriever()
        ollama_llm = Ollama(model="llama3")
        rag_chain = RetrievalQA.from_chain_type(llm=ollama_llm, retriever=retriever)

    # Chat Interface
    if "history" not in st.session_state:
        st.session_state.history = []

    user_question = st.chat_input("Ask something about your PDFs")

    if user_question:
        with st.spinner("Generating answer..."):
            answer = rag_chain.run(user_question)
            st.session_state.history.append((user_question, answer))

    # Display chat history
    for idx, (q, a) in enumerate(st.session_state.history):
        with st.chat_message("user", avatar="👤"):
            st.markdown(q)
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(a)

    # Sidebar chat history
    st.sidebar.markdown("### Chat History")
    for idx, (q, a) in enumerate(st.session_state.history):
        st.sidebar.markdown(f"**Q:** {q}")
else:
    st.info("👆 Upload one or more PDFs to get started!")

st.caption("Powered by Ollama (Local LLM)")
