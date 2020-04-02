import sys
from discord.ext import commands
from discord import File

sys.path.insert(0, '../')
from ereshFunctions import status, permissions


class Misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='rin',
                      description='The truth about Rin',
                      brief='The truth',
                      aliases=['eresh'])
    async def rin(self, ctx):
        await ctx.send("Ereshkigal > Ishtar > f/sn Rin > Loli Rin > f/ha Rin")

    @commands.command(name='dab',
                      description='Ereshkigal dabs',
                      brief='Eresh dabs')
    async def dab(self, ctx):
        await ctx.send(file=File('eresh-dab.png'))

    @commands.command(name='info',
                      description='Information about the bot and its status',
                      brief='Get the bot status and info')
    async def info(self, ctx):
        message = ""
        multiline_message = list()
        multiline_message.append(f">>> Ereshkigal https://github.com/Vogelchevalier/ereshBot")
        multiline_message.append(f"Nickname: {status['nickname']}")
        multiline_message.append(f"Status: {status['playingStatus']} ({status['onlineStatus']})")
        multiline_message.append(f"Available cogs: {status['availableCogs']}")
        multiline_message.append(f"Disabled cogs: {status['disabledCogs']}")

        for line in multiline_message:
            message += f"{line}\n"

        await ctx.send(message)


def setup(bot):
    bot.add_cog(Misc(bot))
