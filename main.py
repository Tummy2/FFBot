import discord
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.all()
# intents.message_content = True
# intents.members = True
# intents.presences = True

client = discord.Client(intents=intents)
guild_status = {}
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  guild = client.get_guild(1280364300837326868)
    
  if guild:
      for member in guild.members:
          guild_status[member.id] = ""
  else:
      print("Guild not found.")
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith('!hello'):
    await message.channel.send('fuck you')

@client.event
async def on_presence_update(before, after):
  new_activity = after.activity.name
  if guild_status[before.id] == "League of Legends":
    guild_status[before.id] = new_activity

    return
  guild_status[before.id] = new_activity

  if(new_activity == "League of Legends"):
    await client.get_channel(1323920088264609843).send(before.mention + " stop playing league u bum")

client.run(os.getenv('TOKEN'))