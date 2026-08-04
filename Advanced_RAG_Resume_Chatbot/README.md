# 🤖 Advanced RAG Resume Chatbot

An AI-powered Resume Assistant built using Retrieval-Augmented Generation (RAG).

This application allows users to upload a resume PDF and ask questions about the candidate's skills, education, experience, and projects.

The system retrieves relevant information from the resume using vector search and generates accurate answers using Google Gemini.

---

## 🚀 Features

- Upload Resume PDF
- Extract resume information
- Convert text into embeddings
- Store embeddings using ChromaDB
- Semantic search using Retriever
- AI-generated answers using Google Gemini
- Interactive Streamlit interface

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Programming Language |
| Streamlit | Web Interface |
| LangChain | RAG Framework |
| Google Gemini | LLM |
| HuggingFace Embeddings | Vector Generation |
| ChromaDB | Vector Database |
| PyPDFLoader | PDF Processing |

---

## 🏗️ Architecture
Resume PDF

 ↓

PDF Loader

 ↓

Text Chunking

 ↓

HuggingFace Embeddings

 ↓

ChromaDB Vector Store

 ↓

Retriever

 ↓

Google Gemini

 ↓

AI Response
📂 Project Structure
Advanced_RAG_Resume_Chatbot/

├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── data/
├── chroma_db/
└── screenshots/
