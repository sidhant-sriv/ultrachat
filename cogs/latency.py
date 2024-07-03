import discord as discord
from discord.ext import commands

class Latency(commands.Cog):
    """Latency commands"""
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name='ping')
    async def latency(self,ctx):
        """Returns latency"""
        await ctx.send(f'The latency is {round(self.bot.latency *1000)} ms')

async def setup(bot):
    await bot.add_cog(Latency(bot))
