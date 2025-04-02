
# Building a RAG-Based Enterprise Knowledge Assistant  


## Overview

This tutorial demonstrates how to build a **Retrieval-Augmented Generation (RAG) application** that serves as an Enterprise Knowledge Assistant. Employees can query an internal knowledge base (e.g., HR policies, IT reports, support documents) and receive AI-generated responses augmented with relevant document excerpts.

**Use Cases:**
- **HR & Policy Assistant:** Query company policies and HR guidelines.
- **IT Knowledge Base:** Retrieve past incident reports and best practices.
- **Customer Support Docs:** Quickly search manuals and SOPs.

---

## Tech Stack

- **LangChain:** Orchestrates document processing, retrieval, and generation pipelines.
- **Streamlit:** Provides a simple web-based user interface for interacting with the assistant.
- **Azure OpenAI:** Supplies powerful language models for generating AI responses and embeddings.
- **Elasticsearch:** Serves as a vector database for storing and retrieving document embeddings.

---

## Prerequisites

Before you begin, ensure you have:

- **Python:** Version 3.10 or later.
- **Azure OpenAI API:** Credentials to access Azure OpenAI models.
- **Elasticsearch:** Access to an Elasticsearch instance (e.g., via Elastic Cloud).

---

## Setup and Installation

### 1. Create and Activate a Virtual Environment

Create a virtual environment to manage project dependencies:

```bash
python -m venv .venv
```

Activate the virtual environment:

- **Windows:**
  ```bash
  .\.venv\Scripts\activate
  ```
- **macOS/Linux:**
  ```bash
  source .venv/bin/activate
  ```

### 2. Install Dependencies

Install the required Python packages using the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root with your credentials and settings:

```dotenv
AZURE_OPENAI_API_KEY=your-azure-api-key
AZURE_OPENAI_ENDPOINT=your-azure-endpoint
AZURE_OPENAI_DEPLOYMENT=your-deployment-name
AZURE_OPENAI_API_VERSION=your-api-version

ELASTICSEARCH_URL=your-elasticsearch-url
ELASTICSEARCH_INDEX=enterprise_knowledge_base
ELASTICSEARCH_API_KEY=your-elasticsearch-api-key
```

---

## Project Structure

```
rag-app-with-simple-streamlit-ui/
│── ingest.py        # Script to load documents into Elasticsearch
│── app.py           # Streamlit app for the chatbot UI
│── .env             # Environment variables
│── requirements.txt # Project dependencies
│── data/            # Folder containing input documents (e.g., hr_policies.txt)
```

---

## Key Components

### Document Ingestion (`ingest.py`)

- **Purpose:** Loads enterprise documents into Elasticsearch for retrieval.
- **Highlights:**
  - Uses `langchain_community` document loaders to read files (e.g., `hr_policies.txt`).
  - Splits documents into smaller chunks using a text splitter.
  - Converts text chunks into vector embeddings using `AzureOpenAIEmbeddings`.
  - Stores embeddings in Elasticsearch.
- **Run:**  
  ```bash
  python ingest.py
  ```

### Chatbot UI (`app.py`)

- **Purpose:** Provides a Streamlit-based UI that lets users ask questions and receive AI-generated answers.
- **Highlights:**
  - Connects to Elasticsearch via a vector store.
  - Creates a RAG pipeline using `RetrievalQA` and `AzureChatOpenAI`.
  - Displays an interactive web UI for querying the knowledge base.
- **Run:**  
  ```bash
  streamlit run app.py
  ```

---

## Running the Application

1. **Ingest Documents:**
   - Ensure your input document (e.g., `data/hr_policies.txt`) is in place.
   - Run the ingestion script:
     ```bash
     python ingest.py
     ```
   - This will process and index your documents into Elasticsearch.

2. **Launch the Chatbot:**
   - Start the Streamlit app:
     ```bash
     streamlit run app.py
     ```
   - Open your browser at [http://localhost:8501](http://localhost:8501) to interact with the assistant.

---

## Next Steps and Enhancements

- **Expand Document Support:** Integrate loaders for PDFs or other file formats.
- **Metadata Filtering:** Enable queries based on document metadata (e.g., filtering by department).
- **Observability:** Implement logging and monitoring for improved pipeline insights.

---

By following these steps and reviewing the code in each module (`ingest.py` and `app.py`), you'll have a fully functioning RAG-based Enterprise Knowledge Assistant. Happy coding!

---