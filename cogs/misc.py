from discord.ext import commands


class Misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='rin',
                      description="The truth about Rin",
                      brief="- The truth",
                      aliases=['eresh'])
    async def rin(self, ctx):
        await ctx.send("Ereshkigal > Ishtar > f/sn Rin > Loli Rin > f/ha Rin")


def setup(bot):
    bot.add_cog(Misc(bot))
