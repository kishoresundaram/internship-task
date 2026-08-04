import os
import streamlit as st

from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# --------------------------------------------------
# Streamlit UI
# --------------------------------------------------

st.set_page_config(
    page_title="Advanced RAG Resume Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Advanced RAG Resume Chatbot")

st.write("Upload a Resume PDF and ask questions about it.")

# --------------------------------------------------
# Load API Key
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    st.success("✅ API Key Loaded Successfully")
else:
    st.error("❌ GOOGLE_API_KEY not found in .env")
    st.stop()

# --------------------------------------------------
# Upload Resume
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

if uploaded_file is not None:

    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # ----------------------------------------------
    # Load PDF
    # ----------------------------------------------

    loader = PyPDFLoader("temp_resume.pdf")

    documents = loader.load()

    st.success(f"PDF Loaded Successfully ({len(documents)} Pages)")

    # ----------------------------------------------
    # Split Text
    # ----------------------------------------------

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    st.success(f"{len(chunks)} Chunks Created")

    # ----------------------------------------------
    # Embeddings
    # ----------------------------------------------

    with st.spinner("Loading Embedding Model..."):

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    st.success("Embeddings Loaded")
        # ----------------------------------------------
    # Create ChromaDB
    # ----------------------------------------------

    with st.spinner("Creating ChromaDB..."):

        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory="chroma_db"
        )

    st.success("✅ ChromaDB Created Successfully")

    # ----------------------------------------------
    # Retriever
    # ----------------------------------------------

    retriever = vector_db.as_retriever(
        search_kwargs={"k": 3}
    )

    st.success("✅ Retriever Created Successfully")

    # ----------------------------------------------
    # Gemini LLM
    # ----------------------------------------------

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-lite",
        temperature=0.3,
        google_api_key=api_key
    )

    st.success("✅ Gemini Connected Successfully")

    # ----------------------------------------------
    # Prompt
    # ----------------------------------------------

    prompt = ChatPromptTemplate.from_template(
        """
You are an AI Resume Assistant.

Answer the user's question ONLY using the provided resume context.

If the answer is not found in the resume, reply exactly:

"I don't have that information in the uploaded resume."

Resume Context:
{context}

Question:
{question}

Answer:
"""
    )

    st.success("✅ Prompt Created Successfully")

    # ----------------------------------------------
    # RAG Chain
    # ----------------------------------------------

    rag_chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
    )

    st.success("✅ RAG Chain Created Successfully")
        # ----------------------------------------------
    # Ask Question
    # ----------------------------------------------

    st.divider()

    st.subheader("💬 Ask Questions About the Resume")

    question = st.text_input(
        "Enter your question",
        placeholder="Example: What are the candidate's technical skills?"
    )

    if st.button("Ask AI"):

        if question.strip() == "":
            st.warning("Please enter a question.")
        else:

            with st.spinner("Thinking..."):

                try:

                    response = rag_chain.invoke(question)

                    st.success("Answer Generated Successfully")

                    st.subheader("🤖 AI Answer")

                    st.write(response.content)

                    # Show Retrieved Chunks (Optional)
                    with st.expander("View Retrieved Chunks"):

                        docs = retriever.invoke(question)

                        for i, doc in enumerate(docs):

                            st.markdown(f"### Chunk {i+1}")

                            st.write(doc.page_content)

                            st.divider()

                except Exception as e:

                    st.error("An error occurred while generating the answer.")

                    st.code(str(e))

else:

    st.info("👆 Please upload a Resume PDF to begin.")