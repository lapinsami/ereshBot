import sys
import discord
from discord.ext import commands, tasks
sys.path.insert(0, '../')
from ereshFunctions import checkStatusMode, getListFromFile


class BGTasks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(minutes=30)
    async def updateStatus(self):
        await self.bot.wait_until_ready()
        game, mode = getListFromFile("status.csv")
        mode = checkStatusMode(mode)
        game = discord.Game(game)
        await self.bot.change_presence(status=mode, activity=game)

    @commands.Cog.listener()
    async def on_ready(self):
        self.updateStatus.start()


def setup(bot):
    bot.add_cog(BGTasks(bot))
