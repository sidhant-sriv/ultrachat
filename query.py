from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from llama_index.embeddings.langchain import LangchainEmbedding
import os
from dotenv import load_dotenv
from llama_index.llms.groq import Groq
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import TitleExtractor
from llama_index.core.ingestion import IngestionPipeline
import asyncio

load_dotenv()
GROQ = os.getenv('GROQ')
HF_TOKEN = os.getenv('HF_TOKEN')
def create_folders_and_file(folder_path, filename):
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
  except OSError as e:
    print(f"Error creating file: {e}")



def generate_embeddings(documents_path:str, save_path:str)->None:
    print("Generating embeddings...")

    load_dotenv()
    HF_TOKEN = os.getenv('HF_TOKEN')

    # Initialize embeddings
    embeddings = HuggingFaceInferenceAPIEmbeddings(
        api_key=HF_TOKEN, model_name="BAAI/bge-large-en-v1.5"
    )
    embed_model = LangchainEmbedding(embeddings)
    Settings.embed_model = embeddings

#    Settings.embed_model = HuggingFaceEmbedding(
#    model_name = 'nomic-ai/nomic-embed-text-v1'
#    )

    documents = SimpleDirectoryReader(documents_path).load_data()
    db = chromadb.PersistentClient(path=save_path)
    # create collection
    chroma_collection = db.get_or_create_collection("quickstart")

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # create your index
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context
    )

    print('Done generating embeddings')


def query(prompt:str, embedding_path:str) -> str:
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
    db = chromadb.PersistentClient(path=embedding_path)

    # get collection
    chroma_collection = db.get_or_create_collection("quickstart")

    # assign chroma as the vector_store to the context
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # load your index from stored vectors
    index = VectorStoreIndex.from_vector_store(
        vector_store, storage_context=storage_context
    )
    query_engine = index.as_query_engine()
    response = query_engine.query(prompt)
    return response
