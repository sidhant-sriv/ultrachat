from urllib import request
from discord.ext import commands
from discord import Embed, Colour
import discord
from datetime import datetime
from llama_index.llms.groq import Groq
from llama_index.core import get_response_synthesizer, DocumentSummaryIndex
from llama_index.core.node_parser import SentenceSplitter
import aiohttp
import nest_asyncio
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from llama_index.embeddings.langchain import LangchainEmbedding
import os
from dotenv import load_dotenv
from llama_index.llms.groq import Groq
import query
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext


query_prompt = "Summarize the following Discord chat log in bullet point format, focusing on the key decisions made and the reasoning behind them. Keep the summary concise and informative."
thumbnail = os.getenv("EMBED_THUMBNAIL")
def summarize_document(file_name='message_history.txt', query=query_prompt):
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
        """Collects a given number of messages in channel and saves it"""
        try:
            num_messages = int(num)
        except (IndexError, ValueError):
            num_messages = 10

        messages = []
        async for msg in ctx.channel.history(limit=num_messages):
            messages.append(msg)

        messages.reverse()

        file_directory = f'chats/{ctx.author.name}/{ctx.message.guild.name}'
        file_name = f'{ctx.message.channel.name}.txt'
        full_path = os.path.join(file_directory, file_name)

        if not os.path.exists(full_path):
            query.create_folders_and_file(file_directory, file_name)

        with open(full_path, 'w', encoding='utf-8') as f:
            for msg in messages:
                if msg.author != self.bot.user:
                    f.write(f'{msg.author.name}: {msg.content}\n')

        await ctx.channel.send(f'Collected the last {num_messages} messages and saved them to {file_name}')
        save_path = os.path.join(file_directory, 'embeddings')
        await query.generate_embeddings(save_path=save_path, documents_path=file_directory)
        await ctx.channel.send('Embeddings generated, ready for querying')
    
    async def is_authenticated(self, user_id):
        """Check if the user is authenticated."""
        url = "https://ultra-chat-backend.onrender.com/is_authenticated"
        headers = {'ID': str(user_id)}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                return response.status == 200

    async def send_login_prompt(self, ctx):
        """Send a login prompt to the user."""
        login_embed = Embed(
            title="Authentication Required",
            description="Please login to access this feature.",
            colour=Colour.red()
        )
        login_embed.set_footer(text="Click the button below to login.")

        login_url = "https://discord.com/oauth2/authorize?client_id=1256967412943949904&redirect_uri=https://ultra-chat-backend.onrender.com/callback&response_type=code&scope=identify%20email"
        login_embed_url = f"{login_url}"
        login_embed.add_field(name="Login", value=f"[Login Here]({login_embed_url})")

        await ctx.channel.send(embed=login_embed)
        print(f"Login prompt sent to {ctx.author.name}")  

    @commands.command(name="summary")
    async def summary(self, ctx, priv=None):
        """provides a summary of a given chat log saved by the collect command"""
        file_directory = f'chats/{ctx.author.name}/{ctx.message.guild.name}'
        file_name = f'{ctx.message.channel.name}.txt'
        full_path = os.path.join(file_directory, file_name)

        authenticated = await self.is_authenticated(ctx.author.id)
        if not authenticated:
            await self.send_login_prompt(ctx)
            return
        if os.path.exists(file_directory):
            summary = summarize_document(full_path)

            summary_embed = discord.Embed(timestamp=datetime.utcnow(), title='Summary',
                                          colour=0xB0B0BF, description=summary)
            summary_embed.set_author(name='UltraChat')
            summary_embed.set_thumbnail(url=thumbnail)
            summary_embed.set_footer(text="UltraChat by GDSC")

            if priv in ['p', 'priv', 'private', 'dm']:
                await ctx.author.send(embed=summary_embed)
            else:
                await ctx.channel.send(embed=summary_embed)
#            print(f'Summary: {summary}')

        else:
            await ctx.channel.send(
                f'No collected messages found for {ctx.author.name}. Please use the !collect command first.')

        url = "https://ultra-chat-backend.onrender.com/is_authenticated"
        headers = {'ID': str(ctx.author.id)}  
    
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response_json = await response.json()
            # Logging response
                print(f"Response status code: {response.status}")
                print(f"Response data: {response_json}")




async def setup(bot):
    await bot.add_cog(Summary(bot))