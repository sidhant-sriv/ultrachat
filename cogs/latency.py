import discord as discord
from discord.ext import commands

class Latency(commands.Cog):
    """Latency commands"""
    def __init__(self, bot):
        self.bot = bot
    @commands.command(aliases= ['ping', 'latency'])
    async def latency(self,ctx):
        """Returns latency"""
        await ctx.send(f'The latency is {round(self.client.latency *1000)} ms')

async def setup(bot):
    await bot.add_cog(Latency(bot))
