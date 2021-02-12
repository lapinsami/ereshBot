import discord
from discord.ext import commands
from application import BotState, Auth
from discord.ext.commands import CommandNotFound


def getPrefix(botti, message):
    prefixes = ['--', 'eresh ']
    return commands.when_mentioned_or(*prefixes)(botti, message)


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=getPrefix, intents=intents)


@bot.check
async def commandAllowed(ctx):

    # Check if user banned
    if ctx.message.author.id in BotState.PERMS.keys():
        if BotState.PERMS[ctx.message.author.id]["banned"]:
            print("banned")
            return False

    # Check if inside a PM
    # and if the user has permission to use commands in PMs
    # or if command is allowed in PMs for everyone
    if isinstance(ctx.message.channel, discord.DMChannel):
        if ctx.message.author.id == 76579685995118592:
            return True
        elif ctx.message.author.id in BotState.PERMS.keys():
            return BotState.PERMS[ctx.message.author.id]["pm_user"] or BotState.PERMS[ctx.message.author.id]["admin"]
        else:
            return False
    else:
        return True


@bot.event
async def on_ready():
    print(f'\n# Logged in as {bot.user.name} ({BotState.STATUS["nickname"]}), id {bot.user.id}')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error


for extension in BotState.STATUS["availableCogs"]:
    if extension not in BotState.STATUS["disabledCogs"]:
        bot.load_extension(f'application.{extension}')
        print(f"# {extension} loaded")

bot.run(Auth.DISCORD, bot=True, reconnect=True)
