from discord.ext import commands
from discord import Embed, Colour
import discord
from datetime import datetime
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
from llama_index.embeddings.cohere import CohereEmbedding
from database import *
from llama_index.core import PromptTemplate
import time




thumbnail = os.getenv("EMBED_THUMBNAIL")

#TODO: cycle through API Keys
#TODO: Convert function to async
def summarize_document(file_name='message_history.txt'):
    # Apply nest_asyncio
    nest_asyncio.apply()

    # Load environment variables
    load_dotenv()
    GROQ = os.getenv('GROQ')
    cohere_api_key = os.getenv('COHERE_API_KEY')

    if not GROQ:
        raise ValueError("Missing GROQ API key in environment variables.")

    qa_prompt_tmpl = (
        "Context information is below.\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "Given the context information and not prior knowledge, "
        "answer the query.\n"
        "Query: {query_str}\n"
        "Answer: "
    )
    qa_prompt = PromptTemplate(qa_prompt_tmpl)

    # Initialize the LLM
    model = 'llama-3.1-8b-instant'
    llm = Groq(model=model, api_key=GROQ)
    Settings.llm = llm

    # Initialize embeddings
    embeddings = CohereEmbedding(
        api_key=cohere_api_key,
        model_name="embed-english-light-v3.0",
        input_type="search_query",
    )

    Settings.embed_model = embeddings

    # Load the document
    reader = SimpleDirectoryReader(input_files=[file_name])
    docs = reader.load_data()
    docs[0].doc_id = file_name

    # Initialize response synthesizer and splitter
    #TODO: check for a better method to generate summary
    response_synthesizer = get_response_synthesizer(response_mode="tree_summarize", use_async=True)
    splitter = SentenceSplitter(chunk_size=512, chunk_overlap=10)

    # Create the document summary index
    doc_summary_index = DocumentSummaryIndex.from_documents(
        docs,
        llm=llm,
        transformations=[splitter],
        response_synthesizer=response_synthesizer,
        show_progress=True
    )

    # Create the query engine
    query_engine = doc_summary_index.as_query_engine(response_mode="tree_summarize", use_async=True, verbose=True, summary_template = qa_prompt)


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
        chat_path = os.path.join(file_directory, file_name)

        if not os.path.exists(chat_path):
            query.create_folders_and_file(file_directory, file_name)

        with open(chat_path, 'w', encoding='utf-8') as f:
            for msg in messages:
                if msg.author != self.bot.user:
                    f.write(f'{msg.author.name}(id:{msg.id}): {msg.content}\n')

        await ctx.channel.send(f'Collected the last {num_messages} messages and saved them to {file_name}')

        vector_store_directory = f'vectors/{ctx.guild.id}/common'
        if str(ctx.channel.type) == "private":
            vector_store_directory = f'vectors/{ctx.guild.id}/private/{ctx.channel.id}'

        file_name = f'all_text.txt'
        all_chat_path = os.path.join(vector_store_directory, file_name)
        save_path = os.path.join(vector_store_directory, 'embeddings')
        temp_path = os.path.join(vector_store_directory, 'TEMP')
        temp_file = os.path.join(temp_path, 'temp.txt')

        if not os.path.exists(all_chat_path):
            query.create_folders_and_file(vector_store_directory, file_name)

        if not os.path.exists(temp_file):
            query.create_folders_and_file(temp_path, 'TEMP.txt')

        with open(all_chat_path, 'a+', encoding='utf-8') as all_chat:
            with open(chat_path, 'r', encoding='utf-8') as chat:
                with open(temp_file, 'a+', encoding='utf-8') as temp:
                    messages = chat.readlines()
                    all_messages = all_chat.readlines()
                    for message in messages:
                        if message not in all_messages:
                            all_chat.write('\n'+message)
                            temp.write('\n'+message)

                query.generate_embeddings(save_path=save_path, documents_path=temp_path)

                with open(temp_file, 'w', encoding='utf-8') as f:
                    pass



    
    async def is_authenticated(self, user_id):
        """Check if the user is authenticated."""
        url = "https://ultra-chat-backend.onrender.com/is_authenticated"
        headers = {'ID': str(user_id)}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                return response.status == 200

    @commands.command(name="login")
    async def send_login_prompt(self, ctx):
        """Send a login prompt to the user."""
        login_embed = Embed(
            title="UltraChat Login",
            description="Please login to store summaries for later",
            colour=Colour.red()
        )
        login_embed.set_footer(text="Click the link above to login.")

        login_url = os.getenv("LOGIN_URL")
        login_embed_url = f"{login_url}"
        login_embed.add_field(name="Login", value=f"[Login Here]({login_embed_url})")

        await ctx.channel.send(embed=login_embed)
        print(f"Login prompt sent to {ctx.author.name}")  

    @commands.command(name="summary")
    async def summary(self, ctx, priv=None):
        start_end = time.time()
        """provides a summary of a given chat log saved by the collect command"""
        file_directory = f'chats/{ctx.author.name}/{ctx.message.guild.name}'
        file_name = f'{ctx.message.channel.name}.txt'
        full_path = os.path.join(file_directory, file_name)



        if os.path.exists(file_directory):
            summary = summarize_document(full_path)

            summary_embed = discord.Embed(timestamp=datetime.utcnow(), title='Summary',
                                          colour=0xB0B0BF, description=summary)
            summary_embed.set_author(name='UltraChat')
            summary_embed.set_thumbnail(url=thumbnail)
            summary_embed.set_footer(text="UltraChat by GDSC")

            data = {
                "content": str(summary),
                "server_id": str(ctx.message.guild.id),
                "is_private": True if str(ctx.message.type) == 'private' else False,
                "user_id": str(ctx.author.id)
            }
            response = create_summary(data)

            end_time = time.time()
            if str(response.status_code) == '201':
                summary_embed.add_field(name=f"Summary saved (in {(end_time-start_end):.2f} sec)", value=f"your summary has been saved successfully")


            else:
                login_url = "https://discord.com/api/oauth2/authorize?client_id=1256967412943949904\u0026redirect_uri=https://ultra-achat-go-backend.onrender.com/callback\u0026response_type=code\u0026scope=identify%20email"
                login_embed_url = f"{login_url}"
                summary.add_field(name="Login to save summaries", value=f"[Login Here]({login_embed_url})")


            if priv in ['p', 'priv', 'private', 'dm']:
                await ctx.author.send(embed=summary_embed)
            else:
                await ctx.channel.send(embed=summary_embed)





        else:
            await ctx.channel.send(
                f'No collected messages found for {ctx.author.name}. Please use the !collect command first.')








async def setup(bot):
    await bot.add_cog(Summary(bot))