from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings

import getpass
import os

load_dotenv()

if not os.environ.get("AIzaSyB9ZsClLJ-8Ysi9JyEhIXCXYwJj-405TR4"):
  os.environ["AIzaSyB9ZsClLJ-8Ysi9JyEhIXCXYwJj-405TR4"] = getpass.getpass("Enter API key for Google Gemini: ")

file_path = Path(__file__).parent / "DBMS_NOTES.pdf"

#load this file in python program
loader = PyPDFLoader(str(file_path))
docs = loader.load()
# print(docs[1].page_content)

#split the document into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunk = text_splitter.split_documents(documents=docs)
# print(chunk[1].page_content)


# vector embeddings
# embedding_model = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=1024)
embedding_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

vector_store = QdrantVectorStore.from_documents(documents=chunk, embedding=embedding_model, url="http://localhost:6333", collection_name="dbms_notes")
print("Indexing of documents completed")

