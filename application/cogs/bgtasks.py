import discord
import random as rand
from discord.ext import commands, tasks
from application import BotState


class BGTasks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(minutes=30)
    async def updateStatus(self):
        await self.bot.wait_until_ready()
        await self.bot.change_presence(status=BotState.STATUS["onlineStatus"], activity=discord.Game(BotState.STATUS["playingStatus"]))
        for server in self.bot.guilds:
            await server.get_member(self.bot.user.id).edit(nick=BotState.STATUS["nickname"])

    @tasks.loop(seconds=5)
    async def customMessage(self):
        await self.bot.wait_until_ready()

        with open("application/message.csv", "r") as f:
            line = f.readline().split(",")

        if len(line) != 6:
            line = ["Channel:", "459711929808715776", "Message:", "message here", "Sent:", "True"]

        sent = line[5] == "True"

        if not sent:
            print(f'Sending "{line[3]}" to channel {line[1]}')
            await self.bot.get_channel(int(line[1])).send(line[3])

        with open("application/message.csv", "w") as f:
            f.write(f'{line[0]},{line[1]},{line[2]},{line[3]},{line[4]},True')

    @commands.Cog.listener()
    async def on_ready(self):
        self.updateStatus.start()
        self.customMessage.start()

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        # 1st: if the ID of the updated member is the bot's ID
        # 2nd: if an updated nickname exists
        # 3rd: if the updated nick differs from the configured nick
        # = if the bot's nickname was updated but the config was not
        if before.id == self.bot.user.id and after.nick and after.nick != BotState.STATUS["nickname"]:
            await after.edit(nick=BotState.STATUS["nickname"])

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author == self.bot.user:
            return

        elif message.author.id == 143323493944131584:
            if rand.randrange(1, 100) <= 1:
                l_thumb = '<:peukku2:719541677370638387>'
                r_thumb = '<:peukku:712075345905451090>'
                face = '<:jimiW:681903944275984426>'
                feet = '<:jalat:712079373360168980>'
                spaces = '             '
                await message.channel.send(f"{l_thumb}{face}{r_thumb}\n{spaces}{feet}")


def setup(bot):
    bot.add_cog(BGTasks(bot))
