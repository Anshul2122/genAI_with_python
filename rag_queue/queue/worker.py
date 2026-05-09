from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
import getpass
import os
from openai import OpenAI



if not os.environ.get("GEMINI_API_KEY"):
  os.environ["GEMINI_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
  
#vector embeddings
embedding_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model, url="http://localhost:6333",
    collection_name="dbms_notes"
)

# take user query and convert it into vector
# user_query = input("Enter your query: ")


print("server is up and running... and connected to vector database and google gemini api")


def process_query(query:str):
    print(f"search chunk: {query}")
    search_results = vector_db.similarity_search(query=query)
    
    context = "\n\n\n".join([f"Page content:{result.page_content}\nPage number: {result.metadata['page_label']}\nFile location:{result.metadata['source']}"
                        for result in search_results])
    
    SYSTEM_PROMPT = """You are a helpful AI assistant who answers questions based on the provided context
                   Use the following retrieved documents to answer the question with page_contents and page number . 
                   If you don't know the answer, say you don't know.
                   Context: {context}"""
                   

    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT.format(context=context)},
            {"role": "user", "content": query}
        ]
    )
    print(f"🤖{response.choices[0].message.content}")
    return response.choices[0].message.content

    