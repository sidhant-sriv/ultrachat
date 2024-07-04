from typing import Final
from dotenv import load_dotenv
from discord import Intents, Client, Message
from discord.ext import commands

import os
import asyncio

# STEP 0: LOAD OUR TOKEN FROM SOMEWHERE SAFE
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# STEP 1: BOT SETUP
intents: Intents = Intents.all()
intents.message_content = True  # NOQA
bot = commands.Bot(command_prefix='!', intents=intents)
EXCLUDED_FILES = ['music.py', 'summarise.py'] #files that might be in the cogs folder but need not to be loaded
EXCLUDED_COMMANDS = ['help']

#Removing default commands
for i in EXCLUDED_COMMANDS:
    bot.remove_command(i)


# STEP 2: HANDLING THE STARTUP FOR OUR BOT
@bot.event
async def on_ready() -> None:
    print(f'{bot.user} is now running!')


@bot.command(name="commands", description="Returns all commands available")
async def commands(ctx):
    helptext = "```"
    for command in bot.commands:
        helptext+=f"{command}\n"
    helptext+="```"
    await ctx.send(helptext)

#STEP 3: Cog Loading
async def load():
    '''loads cogs present in .\cogs'''
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename not in EXCLUDED_FILES:
            await bot.load_extension(f'cogs.{filename[:-3]}')


# STEP 4: MAIN ENTRY POINT
async def main() -> None:
    async with bot:
        await load()
        await bot.start(TOKEN)






if __name__ == '__main__':
    asyncio.run(main())
