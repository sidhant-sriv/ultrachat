from discord.ext import commands
import discord
from datetime import datetime
import os
from dotenv import load_dotenv
import query


load_dotenv()
thumbnail = os.getenv('EMBED_THUMBNAIL')

class Querying(commands.Cog):
    """Discord Cog to handle all querying related commands"""
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="query")
    async def question(self, ctx, *, prompt:str):
        """
        Command: query (!query in chat) followed by the prompt
        Function: After using the collect command, a central vector store will be generated for the specific discord server,
        this command will use that vector store as context and respond to the given prompt
        args:
            ctx (discord.ext.commands.Context): Discord context
            prompt (str): Prompt from the user
        """

        #general vector store directory
        vector_store_directory = f'vectors/common'

        #accesses the private vector store for specific private channels in given discord server
        if str(ctx.channel.type) == "private":
            vector_store_directory = f'vectors/private'

        #vector store path
        embedding_path = vector_store_directory

        #queries if context (vector store) exists
        try:
            response = query.query(prompt, ctx.server.id, embedding_path)

            #Generating discord embed as response to the query
            query_embed = discord.Embed(timestamp=datetime.utcnow(), title='Prompt: '+prompt,
                                              colour=0xB0B0BF, description=response)
            query_embed.set_author(name='UltraChat')
            query_embed.set_thumbnail(url=thumbnail)
            query_embed.set_footer(text="UltraChat by GDSC")

            await ctx.channel.send(embed=query_embed)
        except Exception:
            #handles case if no context is found
            await ctx.channel.send('No context found, use the collect command first')



async def setup(bot):
    await bot.add_cog(Querying(bot))