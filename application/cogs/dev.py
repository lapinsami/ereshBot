from discord.ext import commands

class Dev(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping",
                      description="pong")
    async def ping(self, ctx):
        await ctx.send("pong")


async def setup(bot):
    await bot.add_cog(Dev(bot))
