import os
from dotenv import load_dotenv
from llama_index.llms.groq import Groq
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import StorageContext
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.cohere import CohereEmbedding
from langchain import hub
from llama_index.core import PromptTemplate




#langchain_prompt = hub.pull('rlm/rag-prompt')
#Load Tokens
load_dotenv()
GROQ = os.getenv('GROQ')
HF_TOKEN = os.getenv('HF_TOKEN')
cohere_api_key = os.getenv('COHERE_API_KEY')
pinecone_api = os.getenv('PINECONE_API')

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




def generate_embeddings(documents_path:str, server:str, embedding_path:str, channel:str)->None:
    """
    Generates embeddings for files present in a given folder and stores those vectors in a chroma vector store
    at a given folder
    args:
        documents_path (str): Path to the folders containing contextual data

    """
    print("Generating embeddings...")

    load_dotenv()
    # Initialize embeddings
    embeddings = CohereEmbedding(
        api_key=cohere_api_key,
        model_name="embed-english-light-v3.0",
        input_type="search_query",
    )

    Settings.embed_model = embeddings

    #    Settings.embed_model = HuggingFaceEmbedding(
    #    model_name = 'nomic-ai/nomic-embed-text-v1'
    #    )

    documents = SimpleDirectoryReader(documents_path).load_data()
    for document in documents:
        document.metadata = {"server": server[1:0], "channel": channel}

    db = chromadb.PersistentClient(path=embedding_path)
    # create collection
    chroma_collection = db.get_or_create_collection(server)

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # create your index
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context
    )


    #TODO: USE cache backed embeddings
    print('Done generating embeddings')




def query(prompt:str, server:str, embedding_path:str, channel:str) -> str:
    model = "llama-3.1-8b-instant"
    llm = Groq(model=model, api_key=GROQ)
    Settings.llm = llm

    # Initialize embeddings
    embeddings = CohereEmbedding(
        api_key=cohere_api_key,
        model_name="embed-english-light-v3.0",
        input_type="search_query",

    )

    Settings.embed_model = embeddings


    # get collection
    chroma_collection = db.get_or_create_collection(server)

    storage_context = StorageContext.from_defaults(vector_store=vector_store)


    qa_prompt_tmpl = (
        "The following is a Discord chat log.\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "Given the context of the Discord chat log and not prior knowledge, "
        "answer the query.\n"
        "Query: {query_str}\n"
        "Answer: "
    )
    qa_prompt = PromptTemplate(qa_prompt_tmpl)

    # load your index from stored vectors
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store, storage_context=storage_context
    )

    filter = MetadataFilters(
        filters=[
            MetadataFilter(
                key="server",
                value=str(server),
                operator=FilterOperator.EQ,
            )
        ],
        condition=FilterCondition.AND,
    )
    query_engine = index.as_query_engine(summary_template = qa_prompt)


    response = query_engine.query(f"query made from {channel}"+prompt)
    return response
