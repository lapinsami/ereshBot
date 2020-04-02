import sys
import discord
from discord.ext import commands, tasks
sys.path.insert(0, '../')
from ereshFunctions import status


class BGTasks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(minutes=30)
    async def updateStatus(self):
        await self.bot.wait_until_ready()
        await self.bot.change_presence(status=status["onlineStatus"], activity=discord.Game(status["playingStatus"]))
        for server in self.bot.guilds:
            await server.get_member(self.bot.user.id).edit(nick=status["nickname"])

    @commands.Cog.listener()
    async def on_ready(self):
        self.updateStatus.start()

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        # 1st: if the ID of the updated member is the bot's ID
        # 2nd: if an updated nickname exists
        # 3rd: if the updated nick differs from the configured nick
        # = if the bot's nickname was updated but the config was not
        if before.id == self.bot.user.id and after.nick and after.nick != status["nickname"]:
            await after.edit(nick=status["nickname"])


def setup(bot):
    bot.add_cog(BGTasks(bot))
