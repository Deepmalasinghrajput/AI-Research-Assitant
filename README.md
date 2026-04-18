# AI Research Assistant 

## Overview
This project is an AI-powered research assistant designed to perform end-to-end research by combining Retrieval-Augmented Generation (RAG) with a multi-agent architecture.  

The system integrates multiple specialized agents to handle information retrieval, content extraction, report generation, and evaluation, resulting in more structured and reliable outputs compared to single-model approaches.

---

## Key Features

- Real-time web search using external APIs  
- Content extraction and preprocessing from web sources  
- Contextual retrieval using ChromaDB (RAG)  
- Structured research report generation  
- Automated evaluation of generated content  
- Interactive chat-based user interface  

---

## System Architecture

The workflow is divided into distinct stages:

1. **Search Agent** – Retrieves relevant information from the web  
2. **Reader Agent** – Extracts meaningful content from sources  
3. **RAG Layer** – Enhances context using vector database retrieval  
4. **Writer Agent** – Generates a structured research report  
5. **Critic Agent** – Evaluates the quality and completeness of the output  

---

## Tech Stack

- Python  
- Flask  
- LangChain  
- Mistral AI  
- ChromaDB  
- HTML, CSS, JavaScript  

---

## Project Structure

├── agents.py # Agent definitions
├── tools.py # Web search and scraping tools
├── pipeline.py # Multi-agent workflow
├── rag_store.py # RAG (ChromaDB) logic
├── ingest.py # Data ingestion for vector DB
├── app.py # Flask application

├── templates/
│ └── index.html

├── static/
│ ├── style.css
│ └── script.js

---
Create a .env file and add:
TAVILY_API_KEY=your_api_key
MISTRAL_API_KEY=your_api_key
#Start application
python app.py

