from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
import os
from dotenv import load_dotenv
from llama_index.llms.groq import Groq
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.cohere import CohereEmbedding
import pymongo
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
import uuid

#Load Tokens
load_dotenv()
GROQ = os.getenv('GROQ')
HF_TOKEN = os.getenv('HF_TOKEN')
cohere_api_key = os.getenv('COHERE_API_KEY')
mongo_uri = os.getenv('mongo_uri')


llm_model = "llama-3.1-8b-instant"


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



def generate_embeddings(documents_path:str, server, channel)->None:
    """
    Generates embeddings for files present in a given folder and stores those vectors in a chroma vector store
    at a given folder
    args:
        documents_path (str): Path to the folders containing contextual data

    """
    print("Generating embeddings...")


    # Initialize embeddings

    embeddings = CohereEmbedding(
        api_key=cohere_api_key,
        model_name="embed-english-light-v3.0",
        input_type="search_query",
    )
    Settings.embed_model = embeddings

    #Document reader
    documents = SimpleDirectoryReader(documents_path).load_data()
    for document in documents:
        document.metadata = {"server": int(server), "channel": str(channel)}

    print(documents[0].metadata)

    mongodb_client = pymongo.MongoClient(mongo_uri)
    store = MongoDBAtlasVectorSearch(mongodb_client, db_name = "UltraChat", collection_name=str(server), id_key=str(uuid.uuid4()))

    store.create_vector_search_index(
        dimensions=384, path="embedding", similarity="cosine"
    )


    storage_context = StorageContext.from_defaults(vector_store=store)

    #TODO: USE cache backed embeddings
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context
    )

    print('Done generating embeddings')


def query(prompt:str, server) -> str:
    """
    Rag query agent that uses context from a vector store to respond to a prompt
    args:
        prompt (str): Prompt to the llm
        embedding_path (str): Path to the chroma vector store to use as context to the prompt
    """

    #Initialising the llm model instance
    llm = Groq(model=llm_model, api_key=GROQ)
    Settings.llm = llm

    #Initialise Embeddings
    embeddings = CohereEmbedding(
        api_key=cohere_api_key,
        model_name="embed-english-light-v3.0",
        input_type="search_query",
    )

    Settings.embed_model = embeddings

    mongodb_client = pymongo.MongoClient(mongo_uri)
    store = MongoDBAtlasVectorSearch(mongodb_client, db_name = "UltraChat", collection_name=str(server))

    storage_context = StorageContext.from_defaults(vector_store=store)

    # TODO: USE cache backed embeddings
    index = VectorStoreIndex.from_vector_store(
        vector_store=store, storage_context=storage_context
    )


    #TODO: create a prompt template
    #Rag query agent and querying
    query_engine = index.as_query_engine()
    response = query_engine.query(prompt)

    return response
