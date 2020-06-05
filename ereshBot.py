import discord
from discord.ext import commands
from application import BotState, Auth


def getPrefix(botti, message):
    prefixes = ['--', 'eresh ']
    return commands.when_mentioned_or(*prefixes)(botti, message)


bot = commands.Bot(command_prefix=getPrefix)


@bot.check
async def commandAllowed(ctx):
    if str(ctx.message.author.id) in BotState.PERMS.keys():
        if BotState.PERMS[str(ctx.message.author.id)]["banned"]:
            return False
    if isinstance(ctx.message.channel, discord.DMChannel):
        if str(ctx.message.author.id) in BotState.PERMS.keys():
            return BotState.PERMS[str(ctx.message.author.id)]["pm_user"]
        else:
            return False
    else:
        return True


@bot.event
async def on_ready():
    print(f'\n# Logged in as {bot.user.name} ({BotState.STATUS["nickname"]}), id {bot.user.id}')

for extension in BotState.STATUS["availableCogs"]:
    if extension not in BotState.STATUS["disabledCogs"]:
        bot.load_extension(f'application.{extension}')
        print(f"# {extension} loaded")

bot.run(Auth.DISCORD, bot=True, reconnect=True)

