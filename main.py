import discord
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
# intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  print(message.author.id)

  if message.author == client.user:
    return
  if message.content.startswith('!hello'):
    await message.channel.send('fuck you')
# @client.event
# async def on_activity(message):
  

client.run(os.getenv('TOKEN'))