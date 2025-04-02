import os
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import ElasticsearchStore
from langchain_openai import AzureOpenAIEmbeddings  # To use Azure OpenAI embeddings through LangChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from dotenv import load_dotenv

# # Load environment variables
load_dotenv()

# Get configurations from .env
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL")
ELASTICSEARCH_INDEX = os.getenv("ELASTICSEARCH_INDEX")
ELASTICSEARCH_API_KEY = os.getenv("ELASTICSEARCH_API_KEY")

print("🚀 Starting document ingestion...")

# Load HR policies and IT knowledge base files
loader = TextLoader("data/hr_policies.txt")
documents = loader.load()

if not documents:
    print("❌ No documents found. Please check the file path!")
    exit()

print(f"📄 Loaded {len(documents)} document(s). Splitting text into smaller chunks...")

# Split the document into smaller chunks for better retrieval
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
split_docs = text_splitter.split_documents(documents)

print(f"🔹 Split into {len(split_docs)} chunks. Initializing embeddings...")

# Initialize OpenAI embeddings
embeddings = AzureOpenAIEmbeddings(
    model="text-embedding-3-large",
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    openai_api_version=AZURE_OPENAI_API_VERSION
)

# Store embeddings in Elasticsearch
vectorstore = ElasticsearchStore(
    es_url=ELASTICSEARCH_URL,
    index_name=ELASTICSEARCH_INDEX,
    es_api_key=ELASTICSEARCH_API_KEY,
    embedding=embeddings
)

print("🔄 Converting text into vector embeddings and storing in Elasticsearch...")

# Convert text chunks into embeddings and store them
vectorstore.add_documents(split_docs)

print("✅ Documents successfully added to the enterprise knowledge base in Elasticsearch!")
