from discord.ext import commands
import discord
from datetime import datetime
import os
from dotenv import load_dotenv
import query

load_dotenv()
thumbnail = os.getenv('EMBED_THUMBNAIL')

class Querying(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="regenerate_embeddings")
    async def regenerate_embeddings(self, ctx):
        await ctx.send("Regenerating the embeddings...")
        folder_path = f'chats/{ctx.author.name}/{ctx.message.guild.name}'
        embeddings_path = os.path.join(folder_path, 'embeddings')
        if os.path.exists(embeddings_path):
            os.remove(embeddings_path)

        query.generate_embeddings(folder_path, embeddings_path)
        await ctx.send("Embeddings regenerated successfully")

    @commands.command(name="query")
    async def question(self, ctx, *, prompt):
        file_directory = f'chats/{ctx.author.name}/{ctx.message.guild.name}'
        embedding_path = file_directory + '/embeddings'
        response = query.query(prompt, embedding_path=embedding_path)

        query_embed = discord.Embed(timestamp=datetime.utcnow(), title='Prompt: '+prompt,
                                          colour=0xB0B0BF, description=response)
        query_embed.set_author(name='UltraChat')
        query_embed.set_thumbnail(url=thumbnail)
        query_embed.set_footer(text="UltraChat by GDSC")

        await ctx.channel.send(embed=query_embed)

async def setup(bot):
    await bot.add_cog(Querying(bot))