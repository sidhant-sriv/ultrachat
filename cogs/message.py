#This is a feature file
import discord
from discord.ext import commands
class message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def user_info(self,ctx):
        await ctx.send(f"{ctx.author.name}#{ctx.author.discriminator}  {ctx.author.id}")
async def setup(bot):
    await bot.add_cog(message(bot))
