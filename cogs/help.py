from datetime import datetime
import os
import discord
from discord.ext import commands

thumbnail = os.getenv('EMBED_THUMBNAIL')

help_text = {
    'help': 'Lists all available commands and their description',
    'base64_e': 'Encodes a given message in base64 format',
    'base64_d': 'Decodes a given base_64 encoded message',
    'caeser_e': 'Encodes a given message using the caesar cipher',
    'caesar_d': 'Decodes a given caesar cipher',
    'md5': 'Encodes a given message using the MD5',
    'sha256': 'Encodes a given message using the SHA256',
    '8ball': 'Magic 8ball',
    'senti': 'conducts sentiment analysis on a given message',
    'wiki': 'Returns a wiki article link on the given search term',
    'ping': 'Returns bot latency',
    'ban': 'Bans mentioned user',
    'kick': 'Kicks mentioned user',
    'delete': 'Deletes last n messages in channel (n defaults to 10)',
    'collect': 'Saves a copy of the last n messages in the given channel',
    'summary': 'Provides a summary of saved chatlog. Must only be used after collect',
    'xkcd': 'Displays a random comic',
    'query': 'Answers a question with regards to a specific server',
    'regenerate_embeddings': 'Regenerates the context for querying with the latest saved chat log'
}

command_args = {
    'help': '!help / !help <command name>',
    'base64_e': '!base64_e <text message>',
    'base64_d': '!base64_d <encoded message>',
    'caeser_e': '!caeser_e <text message>',
    'caeser_d': '!caeser_d <encoded message>',
    'md5': '!md5 <message>',
    'sha256': '!sha256 <message>',
    '8ball': '!8ball <question>',
    'senti': '!senti <message>',
    'wiki': '!wiki <search term>',
    'ping': '!ping',
    'ban': '!ban <user mention> / !ban <user mention> <reason>',
    'kick': '!kick <user mention> / !kick <user mention> <reason>',
    'delete': '!delete / !delete <number of messages>',
    'collect': '!collect <number of messages>',
    'summary': '!summary <option for dm (p, priv, private, dm)>',
    'xkcd': '!xkcd',
    'query': '!query <prompt>',
    'regenerate_embeddings': '!regenerate_embeddings'
}


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name ='help')
    async def help(self, ctx, command=None):
        if command:
            # Provide help for a specific command
            command_obj = self.bot.get_command(command)
            if not command_obj:
                await ctx.send(f"Command: '{command}' not found.")
                return
            else:
                command_embed = discord.Embed(timestamp=datetime.utcnow(), title=command,
                                      colour=0xB0B0BF, description=help_text[command])
                command_embed.set_author(name='UltraChat')
                command_embed.set_thumbnail(url=thumbnail)
                command_embed.add_field(name='Command Format', value=command_args[command], inline=True)
                command_embed.set_footer(text="UltraChat by GDSC")
                await ctx.send(embed=command_embed)


        else:
            # Provide a general help message listing available commands
            command_embed = discord.Embed(timestamp=datetime.utcnow(), title='Available Commands',
                                          colour=0xB0B0BF, description="use '!help <command name>' for more info on any particular command")
            command_embed.set_author(name='UltraChat')
            command_embed.set_thumbnail(url=thumbnail)
            command_embed.set_footer(text="UltraChat by GDSC")
            for command in help_text:
                command_embed.add_field(name=command, value=help_text[command], inline=True)

            # Add descriptions for available commands here
            await ctx.send(embed=command_embed)

async def setup(bot):
    await bot.add_cog(Help(bot))