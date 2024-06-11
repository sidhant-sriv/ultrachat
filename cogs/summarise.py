import discord
from discord.ext import commands
import os
from summariser import summarize_document

class MessageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='collect')
    async def collect(self, ctx, num_messages: int = 10):
        messages = []
        async for msg in ctx.channel.history(limit=num_messages):
            messages.append(msg)

        messages.reverse()

        # Ensure the directory exists
        directory = 'message_history'
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Save messages to file in the directory
        file_name = os.path.join(directory, f'{ctx.author.name}_{ctx.channel.id}.txt')
        with open(file_name, 'w') as f:
            for msg in messages:
                f.write(f'{msg.author.name}: {msg.content}\n')

        await ctx.send(f'Collected the last {num_messages} messages and saved them to {file_name}')

    @commands.command(name='summary')
    async def summary(self, ctx, query: str=""):
        # Path to the file in the directory
        file_name = os.path.join('message_history', f'{ctx.author.name}_{ctx.channel.id}.txt')
        if os.path.exists(file_name):
            summary = summarize_document(file_name, query)
            await ctx.send(f'*Summary*:\n {summary}')
        else:
            await ctx.send(f'No collected messages found for {ctx.author.name}. Please use the !collect command first.')

async def setup(bot):
    await bot.add_cog(MessageCog(bot))
