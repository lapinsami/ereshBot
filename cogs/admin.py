import sys
from discord.ext import commands
import discord
sys.path.insert(0, '../')
from ereshFunctions import checkStatusMode, writeListToFile, getListFromFile


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Sets the status
    @commands.command(name='status',
                      description="Sets the status",
                      brief="- Set status",
                      aliases=['np', 'hougu'])
    @commands.is_owner()
    async def status(self, ctx, game, mode):
        game = discord.Game(game)
        mode = checkStatusMode(mode)

        await self.bot.change_presence(status=mode, activity=game)
        writeListToFile([game, mode], "status.csv", "overwrite")
        await ctx.send(f"Playing {game} ({mode})")

    # Logs out the bot
    @commands.command(name='logout',
                      description="Shuts down the bot",
                      brief="- Shutdown",
                      aliases=['close', 'shutdown'])
    @commands.is_owner()
    async def logout(self, ctx):
        await ctx.send("Shutting down...")
        await ctx.bot.logout()

    # Toggle PMs
    @commands.command(name='allowpm',
                      description="Toggles between allowing and not allowing commands in PMs for user",
                      brief="- Allow commands in PMs",
                      aliases=['pm'])
    @commands.is_owner()
    async def togglePm(self, ctx, userid):
        allowed_users = getListFromFile("pm_users.csv")

        if userid in allowed_users:
            allowed_users.remove(userid)
            await ctx.send(f"Commands in PMs disabled for userid {userid}")
        else:
            allowed_users.append(userid)
            await ctx.send(f"Commands in PMs enabled for userid {userid}")

        writeListToFile(allowed_users, "pm_users.csv", "overwrite")

    # Ban user
    @commands.command(name='ban',
                      description="Bans user from using the bot",
                      brief="- Ban user")
    @commands.is_owner()
    async def banUser(self, ctx, userid):
        banned_users = getListFromFile("banned_users.csv")

        if userid in banned_users:
            await ctx.send(f"Userid {userid} is already banned")
        else:
            banned_users.append(userid)
            await ctx.send(f"Userid {userid} banned")

        writeListToFile(banned_users, "banned_users.csv", "overwrite")

    # Unban user
    @commands.command(name='unban',
                      description="Unbans user from using the bot",
                      brief="- Unban user")
    @commands.is_owner()
    async def unbanUser(self, ctx, userid):
        banned_users = getListFromFile("banned_users.csv")

        if userid in banned_users:
            banned_users.remove(userid)
            await ctx.send(f"Userid {userid} unbanned")
        else:
            await ctx.send(f"Userid {userid} is not banned")

        writeListToFile(banned_users, "banned_users.csv", "overwrite")

    # Enable cog
    @commands.command(name='enable',
                      description="Enables a cog",
                      brief="- Enable cog",
                      aliases=['load'])
    @commands.is_owner()
    async def enable(self, ctx, ext):
        self.bot.load_extension(f"cogs.{ext}")
        await ctx.send(f"{ext} enabled")

    # Disable cog
    @commands.command(name='disable',
                      description="Disables a cog",
                      brief="- Disable cog",
                      aliases=['unload'])
    @commands.is_owner()
    async def disable(self, ctx, ext):
        if ext != 'admin':
            self.bot.unload_extension(f"cogs.{ext}")
            await ctx.send(f"{ext} disabled")

    # Reload cog
    @commands.command(name='reload',
                      description="Reloads a cog",
                      brief="- Reload cog",
                      aliases=['re'])
    @commands.is_owner()
    async def reload(self, ctx, ext):
        self.bot.reload_extension(f"cogs.{ext}")
        await ctx.send(f"{ext} reloaded")

    # Reload all cogs
    @commands.command(name='refresh',
                      description="Reloads everything",
                      brief="- Reload all",
                      aliases=['res'])
    @commands.is_owner()
    async def refresh(self, ctx):
        self.bot.reload_extension(f"cogs.math")
        self.bot.reload_extension(f"cogs.dnd")
        self.bot.reload_extension(f"cogs.bgtasks")
        await ctx.send(f"Everything reloaded")
        self.bot.reload_extension(f"cogs.admin")

    @status.error
    @banUser.error
    @unbanUser.error
    @togglePm.error
    @logout.error
    @enable.error
    @disable.error
    @reload.error
    @refresh.error
    async def adminError(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send('Nice try.')


def setup(bot):
    bot.add_cog(Admin(bot))
