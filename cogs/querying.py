from discord.ext import commands
import discord
from datetime import datetime
import os
from dotenv import load_dotenv
import query
import asyncio
from pinecone.grpc import PineconeGRPC as Pinecone
import pinecone



load_dotenv()
thumbnail = os.getenv('EMBED_THUMBNAIL')
pc = Pinecone(api_key=os.getenv('PINECONE_API'))

class Querying(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="query")
    async def question(self, ctx, *, prompt):
        api_key = os.environ["PINECONE_API_KEY"]
        pinecone.init(api_key=api_key, environment='us-east-1')

        if str(ctx.author.id) in pinecone.list_indexes():
            response = query.query(prompt, (ctx.guild.name.lower()).replace(' ', '-'))

            query_embed = discord.Embed(timestamp=datetime.utcnow(), title='Prompt: '+prompt,
                                              colour=0xB0B0BF, description=response)
            query_embed.set_author(name='UltraChat')
            query_embed.set_thumbnail(url=thumbnail)
            query_embed.set_footer(text="UltraChat by GDSC")

            await ctx.channel.send(embed=query_embed)
        else:
            await ctx.channel.send('No context found, use the collect command first')



async def setup(bot):
    await bot.add_cog(Querying(bot))