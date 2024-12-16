
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from llama_index.embeddings.langchain import LangchainEmbedding
import os
from dotenv import load_dotenv
from llama_index.llms.groq import Groq
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.core import Settings
from pinecone import Pinecone, ServerlessSpec
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.pinecone import PineconeVectorStore
from IPython.display import Markdown, display


load_dotenv()
GROQ = os.getenv('GROQ')
HF_TOKEN = os.getenv('HF_TOKEN')
PINECONE_TOKEN = os.environ['PINECONE_API']

pc = Pinecone(api_key=PINECONE_TOKEN)

def create_folders_and_file(folder_path, filename) ->str:
  """
  Creates folders and subfolders if they don't exist and writes content to a file in the deepest folder.

  Args:
      folder_path (str): Path to the top-level folder.
      filename (str): Name of the file to create in the deepest folder.
      content (str, optional): Content to write to the file. Defaults to "This is some text".
  """
  # Ensure path is a string
  if not isinstance(folder_path, str):
    raise TypeError("folder_path must be a string")

  # Create folders using os.makedirs with exist_ok=True to handle existing directories
  try:
    os.makedirs(folder_path, exist_ok=True)
  except OSError as e:
    print(f"Error creating directories: {e}")
    return

  # Create the file with full path
  full_path = os.path.join(folder_path, filename)
  try:
    with open(full_path, 'w') as f:
        pass
    print(f"Successfully created file: {full_path}")
    return full_path
  except OSError as e:
    print(f"Error creating file: {e}")



def generate_embeddings(documents_path:str, index_name:str)->None:
    print("Generating embeddings...")

    index_name = str(index_name)
    pc.create_index(
        name=index_name,
        dimension=1024,
        metric="euclidean",
        spec=ServerlessSpec(cloud="aws", region='us-east-1'),
    )

    load_dotenv()
    HF_TOKEN = os.getenv('HF_TOKEN')

    # Initialize embeddings
    embeddings = HuggingFaceInferenceAPIEmbeddings(
        api_key=HF_TOKEN, model_name="BAAI/bge-large-en-v1.5"
    )
    embed_model = LangchainEmbedding(embeddings)
    Settings.embed_model = embeddings



    documents = SimpleDirectoryReader(documents_path).load_data()
    pinecone_index = pc.Index(index_name)

    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context
    )



    print('Done generating embeddings')


def query(prompt:str, index_name) -> str:
    index_name = str(index_name)
    pc.create_index(
        name=index_name,
        dimension=1024,
        metric="euclidean",
        spec=ServerlessSpec(cloud="aws", region='us-east-1'),
    )

    model = 'llama3-8b-8192'
    llm = Groq(model=model, api_key=GROQ)
    Settings.llm = llm

    # Initialize embeddings
    embeddings = HuggingFaceInferenceAPIEmbeddings(
        api_key=HF_TOKEN, model_name="BAAI/bge-large-en-v1.5"
    )
    embed_model = LangchainEmbedding(embeddings)
    Settings.embed_model = embeddings

    # initialize client
    pinecone_index = pc.Index(index_name)

    vector_store = PineconeVectorStore(
        pinecone_index=pinecone_index,
    )


    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # load your index from stored vectors
    index = VectorStoreIndex.from_vector_store(
        vector_store, storage_context=storage_context
    )
    query_engine = index.as_query_engine()
    response = query_engine.query(prompt)
    return response
