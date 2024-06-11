from llama_index.llms.groq import Groq
from llama_index.core import Settings, SimpleDirectoryReader, get_response_synthesizer, DocumentSummaryIndex
from llama_index.core.node_parser import SentenceSplitter
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from llama_index.embeddings.langchain import LangchainEmbedding
from dotenv import load_dotenv
import os
import nest_asyncio

def summarize_document(file_name='message_history.txt', query="What is the summary of this chat log? Answer casually and also tell me the users involved"):
    # Apply nest_asyncio
    nest_asyncio.apply()

    # Load environment variables
    load_dotenv()
    GROQ = os.getenv('GROQ')
    HF_TOKEN = os.getenv('HF_TOKEN')

    if not GROQ:
        raise ValueError("Missing GROQ API key in environment variables.")

    # Initialize the LLM
    model = 'llama3-8b-8192'
    llm = Groq(model=model, api_key=GROQ)
    Settings.llm = llm

    # Initialize embeddings
    embeddings = HuggingFaceInferenceAPIEmbeddings(
        api_key=HF_TOKEN, model_name="BAAI/bge-large-en-v1.5"
    )
    embed_model = LangchainEmbedding(embeddings)
    Settings.embed_model = embeddings

    # Load the document
    reader = SimpleDirectoryReader(input_files=[file_name])
    docs = reader.load_data()
    docs[0].doc_id = file_name

    # Initialize response synthesizer and splitter
    response_synthesizer = get_response_synthesizer(response_mode="tree_summarize", use_async=True)
    splitter = SentenceSplitter(chunk_size=1024)

    # Create the document summary index
    doc_summary_index = DocumentSummaryIndex.from_documents(
        docs,
        llm=llm,
        transformations=[splitter],
        response_synthesizer=response_synthesizer,
    )

    # Create the query engine
    query_engine = doc_summary_index.as_query_engine(response_mode="tree_summarize", use_async=True)

    # Return the query result
    return query_engine.query(query)

