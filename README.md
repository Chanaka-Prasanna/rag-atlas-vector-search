# Learn Deep Learning with AI — RAG Application

This is a **Retrieval-Augmented Generation (RAG)** based web application designed to help users learn about **Deep Learning** by asking AI-driven questions.

The app uses the **Deep Learning Book** as the knowledge base, processes it into vector embeddings, stores them in **MongoDB Atlas Vector Search**, and generates intelligent answers using **Google Gemini LLMs**.

---

## 📚 Project Overview

- The Deep Learning Book was split into smaller meaningful chunks.
- Each chunk was embedded into a vector representation using **Google Generative AI Embeddings**.
- The embedded data was stored in a **MongoDB Atlas** database using **Atlas Vector Search** indexing.
- A **Streamlit** web app allows users to enter queries.
- The app retrieves the most relevant document chunks using **vector similarity search**.
- A custom **prompt template** is used to format the retrieved context before sending it to the **Gemini  model**.
- The final answer is generated and displayed to the user.

---

## 🛠️ Technologies Used

- **Python** — Main programming language.
- **Streamlit** — For building the interactive frontend application.
- **MongoDB Atlas** — To store and manage vectorized document chunks.
- **Atlas Vector Search** — To retrieve the most relevant information based on similarity.
- **LangChain** — To build the RAG pipeline (retriever, prompt templates, chains).
- **Google Gemini** — As the Large Language Model (LLM) for final answer generation.
- **Google Generative AI Embeddings** — For creating document embeddings.
- **Custom Metadata Tagging** — Metadata extraction from documents using Gemini.

---

## 📂 Project Structure

```plaintext
├── app.py                # Streamlit frontend for user interaction
├── rag.py                # Main RAG pipeline (Retriever + LLM answering)
├── store_vector_data.py  # Script for processing and storing document chunks
├── deeplearningbook.pdf  # Source document for knowledge base
├── key_param.py          # API keys and MongoDB URI configurations
├── search_index.json     # Configurations for create vector search index
```

---

## ⚡ How It Works

1. The `store_vector_data.py` script:
    - Loads the Deep Learning Book.
    - Splits the content into smaller chunks.
    - Extracts metadata (title, keywords, code presence).
    - Creates vector embeddings.
    - Stores everything into MongoDB Atlas with a vector search index.

2. The `app.py` and `rag.py`:
    - Provide a frontend for users to submit their queries.
    - Retrieve the most relevant document chunks based on vector similarity.
    - Format the context into a prompt.
    - Use Gemini model to generate an accurate answer.
    - Display the answer to the user.

---

## 🎯 What I Learned

- How to implement **Retrieval-Augmented Generation (RAG)** applications.
- How to configure and use **MongoDB Atlas Vector Search**.
- How to store embeddings and perform **vector similarity search**.
- How to build flexible RAG pipelines using **LangChain**.
- How to use **Google Gemini models** for context-aware answer generation.
- How to integrate frontend and backend seamlessly with **Python** and **Streamlit**.

---
