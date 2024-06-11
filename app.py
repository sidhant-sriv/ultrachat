from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from summariser import summarize_document
# STEP 0: LOAD OUR TOKEN FROM SOMEWHERE SAFE
load_dotenv()
TOKEN: Final[str] = os.getenv('TOKEN')

# STEP 1: BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
client: Client = Client(intents=intents)

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
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

# STEP 4: HANDLING MESSAGES
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
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
        with open(file_name, 'w') as f:
            for msg in messages:
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
        latency = round(client.latency * 1000)
        await message.channel.send(f'Pong! Latency is {latency}ms')

    else:
        await send_message(message, user_message)

# STEP 5: MAIN ENTRY POINT
def main() -> None:
    client.run(TOKEN)

if __name__ == '__main__':
    main()