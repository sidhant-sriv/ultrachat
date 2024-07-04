import discord as discord
from discord.ext import commands
from googlesearch import search
import wikipedia


class Info(commands.Cog):
    """Info giving commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='google', description="Gives the first google result")
    async def google(self, ctx, *, query):
        print('damn')
        """Google search"""
        for j in search(query, tld="co.in", num=2, stop=2, pause=1):
            await ctx.send(j)

    @commands.command(name = 'wiki', description="Wikipedia")
    async def wiki(self, ctx, *, query):
        """Wikipedia search"""
        try:
            t = str(wikipedia.search(query)[0].encode("utf-8"))
            res = discord.Embed(title=str(t).title()[
                                2:-1], description=wikipedia.summary(t, sentences=4))
            res.set_thumbnail(url=wikipedia.page(t).images[0])
            # res.set_image(url=wikipedia.page(t).images[1])
            await ctx.send(embed=res)
        except Exception:
            await ctx.send(f"Here is a page with all the links that contain {query} <https://en.wikipedia.org/wiki/"+query.title()+">")


async def setup(bot):
    await bot.add_cog(Info(bot))
