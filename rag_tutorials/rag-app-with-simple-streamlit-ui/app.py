import os
import streamlit as st
from langchain_openai import AzureOpenAIEmbeddings 
from langchain_community.vectorstores import ElasticsearchStore
from langchain_openai import AzureChatOpenAI
from langchain.chains import RetrievalQA 
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configurations from .env
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL")
ELASTICSEARCH_INDEX = os.getenv("ELASTICSEARCH_INDEX")
ELASTICSEARCH_API_KEY = os.getenv("ELASTICSEARCH_API_KEY")

# Initialize OpenAI embeddings
embeddings = AzureOpenAIEmbeddings(
    model="text-embedding-3-large",
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    openai_api_version=AZURE_OPENAI_API_VERSION
)

# Connect to Elasticsearch vector store
vectorstore = ElasticsearchStore(
    es_url=ELASTICSEARCH_URL,
    index_name=ELASTICSEARCH_INDEX,
    es_api_key=ELASTICSEARCH_API_KEY,
    embedding=embeddings
)

# Create Retrieval-Augmented Generation (RAG) pipeline
retriever = vectorstore.as_retriever()
llm = AzureChatOpenAI(
    # azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    # api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_deployment=os.getenv("AZURE_DEPLOYMENT_NAME")
)


qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff"
)

# Streamlit UI
st.title("🧠 Enterprise Knowledge Assistant")
st.write("Ask questions about HR policies, IT knowledge, or support documentation.")

query = st.text_input("🔍 Enter your query:")

if query:
    response = qa_chain.run(query)
    st.write("**AI Response:**", response)
