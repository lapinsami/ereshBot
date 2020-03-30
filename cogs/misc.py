from discord.ext import commands
from discord import File


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


def setup(bot):
    bot.add_cog(Misc(bot))
