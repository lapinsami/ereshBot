import os
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from application import COGS

TOKEN = os.environ['DISCORD_TOKEN']

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="--", intents=intents)


@bot.check
async def command_allowed(ctx):
    return True


@bot.event
async def on_ready():
    print(f'\n# Logged in as {bot.user.name}, id {bot.user.id}')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

async def load_extensions():
    for ext in COGS:
        await bot.load_extension(f'application.{ext}')
        print(f"# {ext} loaded")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN, reconnect=True)

asyncio.run(main())
