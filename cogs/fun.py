import discord
import os
import imgurpython
import requests
from discord.ext import commands
import random
import praw
from textblob import TextBlob
from dotenv import load_dotenv, find_dotenv
load_dotenv('.env')
CLIENT_ID = os.environ['REDDIT_CLIENT_ID']
CLIENT_SECRET = os.environ['REDDIT_CLIENT_SECRET']
USER_AGENT = os.environ['REDDIT_USER_AGENT']
IMGUR_ID = os.environ['IMGUR_CLIENT_ID']
IMGUR_SECRET = os.environ['IMGUR_CLIENT_SECRET']

class Fun(commands.Cog):
    """Stuff that's fun"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='8ball')
    async def _8ball(self, ctx, *, question):
        """Magic 8ball"""
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful."]
        res = discord.Embed(title=f'Question : **{question}**',description=f'Answer: **{random.choice(responses)}**', color=0xB0B0BF)
        await ctx.send(embed=res)


    @commands.command(name="senti")
    async def sentiment(self, ctx, *, sentence):
        """Returns sentiment of a sentence"""
        if sentence:
            words = TextBlob(sentence)
            res = discord.Embed(title=f'{sentence}', description= f'Calculated sentiment {words.sentiment.polarity}', color=0xB0B0BF)
            res.set_footer(text="If value>0 then positive, <0 then negative and =0 then neutral sentiment")
            await ctx.send(embed=res)
    @commands.command(name = 'imgur')
    async def imgur(self, ctx, *, query):
        """Returns an image from imgur"""
        if query:
            client = imgurpython.ImgurClient(IMGUR_ID,IMGUR_SECRET)
            items = client.gallery_search(query)[:]
            post = random.choice(items)
            res = discord.Embed(title=post.title)
            res.set_image(url=post.link)
            await ctx.send(post.link)

async def setup(bot):
    await bot.add_cog(Fun(bot))
