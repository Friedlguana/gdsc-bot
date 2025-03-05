import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

# Load Tokens
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True
intents.voice_states = True


bot = commands.Bot(command_prefix="!", intents=intents)

async def load_cogs():
    for cog in ['ai_responder', 'reminders', 'polls', 'welcome', 'music']:
        await bot.load_extension(f'cogs.{cog}')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

asyncio.run(main())
