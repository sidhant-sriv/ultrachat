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
#client: Client = Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)
EXCLUDED_FILES = [] #files that might be in the cogs folder but need not to be loaded

# STEP 2: MESSAGE FUNCTIONALITY
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled probably)')
        return

    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

# STEP 3: HANDLING THE STARTUP FOR OUR BOT
@bot.event
async def on_ready() -> None:
    print(f'{bot.user} is now running!')

# STEP 4: HANDLING MESSAGES
"""@bot.event
async def on_message(message: Message) -> None:
    if message.author == bot.user:
        return

    user_message = message.content

    if user_message.startswith('!collect'):
        try:
            num_messages = int(user_message.split()[1])
        except (IndexError, ValueError):
            num_messages = 10

        messages = []
        async for msg in message.channel.history(limit=num_messages):
            messages.append(msg)

        messages.reverse()

        file_name = f'{message.author.name}.txt'
        with open(file_name, 'w', encoding='utf-8') as f:
            for msg in messages:
                if msg.author != bot.user:
                    f.write(f'{msg.author.name}: {msg.content}\n')

        await message.channel.send(f'Collected the last {num_messages} messages and saved them to {file_name}')

    elif user_message.startswith('!summary'):
        file_name = f'{message.author.name}.txt'
        if os.path.exists(file_name):
            summary = summarize_document(file_name)
            await message.channel.send(f'*Summary*:\n {summary}')
        else:
            await message.channel.send(f'No collected messages found for {message.author.name}. Please use the !collect command first.')

    elif user_message == '!ping':
        latency = round(bot.latency * 1000)
        await message.channel.send(f'Pong! Latency is {latency}ms')

    else:
        await send_message(message, user_message)
"""

@bot.command(name="commands", description="Returns all commands available")
async def commands(ctx):
    helptext = "```"
    for command in bot.commands:
        helptext+=f"{command}\n"
    helptext+="```"
    await ctx.send(helptext)

#Cog Loading
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename not in EXCLUDED_FILES:
            await bot.load_extension(f'cogs.{filename[:-3]}')


# STEP 5: MAIN ENTRY POINT
async def main() -> None:
    async with bot:
        await load()
        await bot.start(TOKEN)






if __name__ == '__main__':
    asyncio.run(main())
