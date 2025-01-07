import discord
import openai
from dotenv import load_dotenv
import os

load_dotenv()

# -------------------- TOKENS --------------------

DISCORD_TOKEN=os.getenv('DISCORD_TOKEN')
OPENAI_TOKEN=os.getenv('OPENAI_TOKEN')

if not DISCORD_TOKEN:
    raise ValueError("Discord API key not found. Set it as an environment variable.")
if not OPENAI_TOKEN:
    raise ValueError("OpenAI API key not found. Set it as an environment variable.")

# -------------------- Discord Setup --------------------

intents = discord.Intents.all()
client = discord.Client(intents=intents)
guild_status = {}   # guild_status = {guildA: {memberA: activity, memberB: activity}, guildB: {}, guildC: {}}

# -------------------- OpenAI Setup --------------------

openai.api_key = OPENAI_TOKEN

# -------------------- HELPER FUNCTIONS -------------------

def find_notification_channel(guild):  # Find the channel to send messages in (usually general) 
  for channel in guild.text_channels:
      if channel.name == "ffbot":   # Find the channel for ffbot
          return channel.id
  return guild.text_channels[0].id if guild.text_channels else None   # Find the first available channel

async def generate_message():
    response =  await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a toxic league of legends streamer, you are super sarcastic and love to trash talk in anyway that you can, but you give credit when credit is due. You often swear, and use a lot of modern slang"},
            {"role": "user", "content": "I am playing league of legends again, what do you have to say to me."},
        ],
        temperature=1.2,
        max_tokens=150
    )
    return response['choices'][0]['message']['content']

# -------------------- DISCORD FUNCTIONS -------------------

@client.event
async def on_ready():   # Bot already in server and is booting up
    print(f'We have logged in as {client.user}')
    for guild in client.guilds:   # Loop through every server the bot is apart of and initialize
        guild_status[guild.id] = {}
        for member in guild.members:
            guild_status[guild.id][member.id] = ""
    print("Guilds and members initialized!")

@client.event
async def on_guild_join(guild):   # Bot is joining server for the first time
    guild_status[guild.id] = {}
    for member in guild.members:    # Create a new dictionary which is the new guild the bot just joined and initialize
        guild_status[guild.id][member.id] = ""
    print(f"Joined new guild: {guild.name}")

# @client.event
# async def on_message(message):
#   if message.author == client.user:
#     return
#   if message.content.startswith('!hello'):
#     await message.channel.send('fuck you')

@client.event
async def on_presence_update(before, after):
    guild = before.guild 
    if not guild or guild.id not in guild_status:   # Make sure the member is in a real guild
        return

    new_activity = after.activity.name if after.activity else ""    # Get the new activity if it exists

    member_status = guild_status[guild.id]    # member_status is the guild with the member we are looking for

    if member_status.get(before.id) == "League of Legends":   # If they were already playing LOL we don't care
        member_status[before.id] = new_activity
        return

    member_status[before.id] = new_activity   # Update what they are doing

    if new_activity == "League of Legends":   # If they did start playing LOL
        notification_channel_id = find_notification_channel(guild)
        if notification_channel_id:
            channel = client.get_channel(notification_channel_id)
            if channel:
                message = await generate_message()
                await channel.send(f"{before.mention} {message}")

client.run(DISCORD_TOKEN)