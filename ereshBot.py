import discord
from discord.ext import commands
from ereshFunctions import status, permissions
from cli import mainMenu


def getPrefix(botti, message):
    prefixes = ['--', 'eresh ']
    return commands.when_mentioned_or(*prefixes)(botti, message)


token_file = open("token.csv", "r")
TOKEN = token_file.readline()
token_file.close()
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
    await mainMenu(bot)


for extension in status["availableCogs"]:
    if extension not in status["disabledCogs"]:
        bot.load_extension(extension)
        print(f"# {extension} loaded")

bot.run(TOKEN, bot=True, reconnect=True)
