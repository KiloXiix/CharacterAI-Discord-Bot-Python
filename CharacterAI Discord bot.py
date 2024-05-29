import asyncio
import discord
from characterai import aiocai

# Replace these with your actual values
char_id = 'Input your characterai character id here'
CHATOKEN = 'input your characterai login token here '
TOKEN = "Input your discord bot token here"

intents = discord.Intents.default()
intents.message_content = True

class MyBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chat = None
        self.char = char_id
        self.client = aiocai.Client(CHATOKEN)
        self.chat_history = []

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        me = await self.client.get_me()
        async with await self.client.connect() as chat:
            self.chat = chat
            new, answer = await self.chat.new_chat(self.char, me.id)
            self.chat_id = new.chat_id
            print(f'{answer.name}: {answer.text}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.lower() == "nl1027":
            await message.channel.send("Shutting down...")
            await self.save_chat_history()
            await self.close()
            return

        async with await self.client.connect() as chat:
            chat_response = await chat.send_message(self.char, self.chat_id, message.content)
            self.chat_history.append(
                f"{message.author.name}: {message.content}\n{self.user.name}: {chat_response.text}\n"
            )
            await self.save_chat_history()
            await message.channel.send(chat_response.text)

    async def save_chat_history(self):
        with open("chat_history.txt", "a") as f:
            for entry in self.chat_history:
                f.write(entry)

async def main():
    client = MyBot(intents=intents)
    await client.start(TOKEN)

asyncio.run(main())
