from discord.ext import commands
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




class Summary(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="collect")
    async def collect(self, ctx, num):
        try:
            num_messages = int(num)
        except (IndexError, ValueError):
            num_messages = 10

        messages = []
        async for msg in ctx.channel.history(limit=num_messages):
            messages.append(msg)

        messages.reverse()

        file_name = f'{ctx.author.name}.txt'
        with open(file_name, 'w', encoding='utf-8') as f:
            for msg in messages:
                if msg.author != self.bot.user:
                    f.write(f'{msg.author.name}: {msg.content}\n')

        await ctx.channel.send(f'Collected the last {num_messages} messages and saved them to {file_name}')
    @commands.command(name="summary")
    async def summary(self, ctx):
        file_name = f'{ctx.author.name}.txt'
        if os.path.exists(file_name):
            summary = summarize_document(file_name)
            await ctx.channel.send(f'*Summary*:\n {summary}')
        else:
            await ctx.channel.send(
                f'No collected messages found for {ctx.author.name}. Please use the !collect command first.')

async def setup(bot):
    await bot.add_cog(Summary(bot))