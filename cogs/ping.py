import discord
from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is online.' + "Logged in as " + str(self.client.user) + " with ID " + str(self.client.user.id) + "!")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

    

async def setup(client):
    await client.add_cog(Ping(client))