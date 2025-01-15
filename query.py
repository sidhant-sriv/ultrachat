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
from langchain import hub
from llama_index.core.prompts import LangchainPromptTemplate

langchain_prompt = hub.pull('rlm/rag-prompt')
#Load Tokens
load_dotenv()
GROQ = os.getenv('GROQ')
HF_TOKEN = os.getenv('HF_TOKEN')
cohere_api_key = os.getenv('COHERE_API_KEY')


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



def generate_embeddings(documents_path:str, server:str, embedding_path)->None:
    """
    Generates embeddings for files present in a given folder and stores those vectors in a chroma vector store
    at a given folder
    args:
        documents_path (str): Path to the folders containing contextual data
        save_path (str): Path to the folder where the embeddings will be stored (in a folder named embeddings)
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
    db = chromadb.PersistentClient(path=embedding_path)

    # create collection
    chroma_collection = db.get_or_create_collection(server)

    #TODO: Switch from Chroma to Weaviate or SupaBase
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # create your index
    #TODO: USE cache backed embeddings
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context
    )

    print('Done generating embeddings')


def query(prompt:str, server, embedding_path) -> str:
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

    # initialize client
    db = chromadb.PersistentClient(path=embedding_path)

    # get collection
    chroma_collection = db.get_or_create_collection(server)

    # assign chroma as the vector_store to the context
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # load your index from stored vectors
    index = VectorStoreIndex.from_vector_store(
        vector_store, storage_context=storage_context
    )

    #TODO: create a prompt template
    #Rag query agent and querying
    query_engine = index.as_query_engine()
    lc_prompt_tmpl = LangchainPromptTemplate(
        template=langchain_prompt,
        template_var_mappings={"query_str": "question", "context_str": "context"},
    )

    query_engine.update_prompts(
        {"response_synthesizer:text_qa_template": lc_prompt_tmpl}
    )
    response = query_engine.query(prompt)
    return response
