import discord
import os
from discord.ext import commands
from ereshFunctions import getListFromFile


def getPrefix(botti, message):
    prefixes = ['--', 'eresh ']
    return commands.when_mentioned_or(*prefixes)(botti, message)


token_file = open("token.csv", "r")
TOKEN = token_file.readline()
token_file.close()
bot = commands.Bot(command_prefix=getPrefix)


@bot.check
async def commandAllowed(ctx):
    if str(ctx.message.author.id) in getListFromFile("banned_users.csv"):
        return False
    if isinstance(ctx.message.channel, discord.DMChannel):
        return str(ctx.message.author.id) in getListFromFile("pm_users.csv")
    else:
        return True


@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name)
    print(bot.user.id)
    print('-------------------')


for file in os.listdir('./cogs'):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")

bot.run(TOKEN, bot=True, reconnect=True)
