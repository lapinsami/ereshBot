import discord
from discord.ext import commands
from application import status, permissions


def getPrefix(botti, message):
    prefixes = ['--', 'eresh ']
    return commands.when_mentioned_or(*prefixes)(botti, message)


with open("application/api_keys/discord_api_key.csv", "r") as f:
    TOKEN = f.readline()

bot = commands.Bot(command_prefix=getPrefix)


@bot.check
async def commandAllowed(ctx):
    if str(ctx.message.author.id) in permissions.keys():
        if permissions[str(ctx.message.author.id)]["banned"]:
            return False
    if isinstance(ctx.message.channel, discord.DMChannel):
        if str(ctx.message.author.id) in permissions.keys():
            return permissions[str(ctx.message.author.id)]["pm_user"]
        else:
            return False
    else:
        return True


@bot.event
async def on_ready():
    print(f'\n# Logged in as {bot.user.name} ({status["nickname"]}), id {bot.user.id}')

for extension in status["availableCogs"]:
    if extension not in status["disabledCogs"]:
        bot.load_extension(f'application.{extension}')
        print(f"# {extension} loaded")

bot.run(TOKEN, bot=True, reconnect=True)

