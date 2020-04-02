import sys
import os
from discord.ext import commands
import discord

sys.path.insert(0, '../')
from ereshFunctions import checkStatusMode, writeToYAML, status, permissions, default_permissions


def isAdmin(ctx):
    if str(ctx.author.id) in permissions.keys():
        admin = permissions[str(ctx.author.id)]["admin"]
    else:
        admin = False

    owner = ctx.author.id == 76579685995118592

    return admin or owner


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Sets the nickname
    @commands.command(name='nick',
                      description='Sets the bot nickname',
                      brief='Set bot nick',
                      aliases=['nickname'])
    @commands.check(isAdmin)
    async def nick(self, ctx, nickname):

        status["nickname"] = nickname
        await ctx.send(f"Thus, shalt thou call me {nickname}")
        await ctx.guild.get_member(self.bot.user.id).edit(nick=nickname)
        writeToYAML("status.yml", status)

    # Sets the status
    @commands.command(name='status',
                      description='Sets the status',
                      brief='Set status',
                      aliases=['np', 'hougu'])
    @commands.check(isAdmin)
    async def status(self, ctx, game, mode):
        playing = discord.Game(game)
        online = checkStatusMode(mode)

        status["playingStatus"] = str(playing)
        status["onlineStatus"] = str(online)
        await ctx.send(f"Playing {str(playing)} ({str(online)})")
        await self.bot.change_presence(status=online, activity=playing)
        writeToYAML("status.yml", status)

    # Logs out the bot
    @commands.command(name='logout',
                      description="Shuts down the bot",
                      brief="Shutdown",
                      aliases=['close', 'shutdown'])
    @commands.is_owner()
    async def logout(self, ctx):
        await ctx.send("Shutting down...")
        await ctx.bot.logout()

    # Toggle PMs
    @commands.command(name='allowpm',
                      description="Toggles between allowing and not allowing commands in PMs for user",
                      brief="Allow commands in PMs",
                      aliases=['pm'])
    @commands.check(isAdmin)
    async def togglePm(self, ctx, userid):

        # if no permissions set for the userid, set them to default
        if userid not in permissions.keys():
            permissions[str(userid)] = default_permissions["useridhere"]

        # if the user has pm permissions, disable them
        # and if they don't, enable them
        if permissions[userid]["pm_user"]:
            permissions[userid]["pm_user"] = False
            await ctx.send(f"Commands in PMs disabled for userid {userid}")
        else:
            permissions[userid]["pm_user"] = True
            await ctx.send(f"Commands in PMs enabled for userid {userid}")

        writeToYAML("permissions.yml", permissions)

    # Ban user
    @commands.command(name='ban',
                      description="Bans user from using the bot",
                      brief="Ban user")
    @commands.check(isAdmin)
    async def banUser(self, ctx, userid):

        # if no permissions set for the userid, set them to default
        if userid not in permissions.keys():
            permissions[str(userid)] = default_permissions["useridhere"]

        # if user already banned, do nothing
        # if user not banned, ban them (if not admin)
        if permissions[userid]["banned"]:
            await ctx.send(f"Userid {userid} is already banned")
        elif not isAdmin(userid):
            permissions[userid]["banned"] = True
            await ctx.send(f"Userid {userid} banned")
        else:
            await ctx.send(f"Userid {userid} is an admin")

        writeToYAML("permissions.yml", permissions)

    # Unban user
    @commands.command(name='unban',
                      description="Unbans user from using the bot",
                      brief="Unban user")
    @commands.check(isAdmin)
    async def unbanUser(self, ctx, userid):

        # if no permissions set for the userid, set them to default
        if userid not in permissions.keys():
            permissions[str(userid)] = default_permissions["useridhere"]

        # if user banned, unban them
        # if user not banned, do nothing
        if permissions[userid]["banned"]:
            permissions[userid]["banned"] = False
        else:
            await ctx.send(f"Userid {userid} is not banned")

        writeToYAML("permissions.yml", permissions)

    # Enable cog
    @commands.command(name='enable',
                      description="Enables a cog",
                      brief="Enable cog",
                      aliases=['load'])
    @commands.check(isAdmin)
    async def enable(self, ctx, ext):

        # if "all" as the argument, load all cogs
        if ext == "all":
            for extension in status["disabledCogs"]:
                if extension != "cogs.admin":
                    self.bot.load_extension(extension)

            status["disabledCogs"] = list()

            await ctx.send(f"Everything enabled")

        # load the cog given as the argument
        elif f"cogs.{ext}" in status["availableCogs"]:
            self.bot.load_extension(f"cogs.{ext}")
            status["disabledCogs"].remove(f"cogs.{ext}")
            await ctx.send(f"{ext} enabled")

        else:
            await ctx.send(f"No cog named {ext}")

        # write status to file
        writeToYAML("status.yml", status)

    # Disable cog
    @commands.command(name='disable',
                      description="Disables a cog",
                      brief="Disable cog",
                      aliases=['unload'])
    @commands.check(isAdmin)
    async def disable(self, ctx, ext):

        # if "all" as the argument, unload all cogs
        if ext == "all":
            for extension in status["availableCogs"]:
                if extension != "cogs.admin":
                    self.bot.unload_extension(extension)
                    status["disabledCogs"].append(extension)

            await ctx.send(f"Everything disabled")

        # unload the cog given as the argument
        elif f"cogs.{ext}" in status["availableCogs"]:
            if ext != "admin":
                self.bot.unload_extension(f"cogs.{ext}")
                status["disabledCogs"].append(f"cogs.{ext}")
                await ctx.send(f"{ext} disabled")

        else:
            await ctx.send(f"No cog named {ext}")

        # write status to file
        writeToYAML("status.yml", status)

    # Reload cog
    @commands.command(name='reload',
                      description="Reloads a cog",
                      brief="Reload cog",
                      aliases=['re'])
    @commands.check(isAdmin)
    async def reload(self, ctx, ext):

        # if "all" as the argument, reload all enabled cogs
        if ext == "all":
            for extension in status["availableCogs"]:
                if extension not in status["disabledCogs"]:
                    self.bot.reload_extension(extension)

            await ctx.send(f"Reloaded all enabled cogs. Disabled cogs unaffected. Use --load all to load them.")

        # reload the cog given as the argument
        elif f"cogs.{ext}" not in status["disabledCogs"]:
            self.bot.reload_extension(f"cogs.{ext}")
            await ctx.send(f"{ext} reloaded")

        # write status to file
        writeToYAML("status.yml", status)

    # Make user an admin
    @commands.command(name='admin',
                      description="Give admin permissions to the user",
                      brief="Make user an admin")
    @commands.is_owner()
    async def admin(self, ctx, userid):

        # if no permissions set for the userid, set them to default
        if userid not in permissions.keys():
            permissions[userid] = permissions["useridhere"]

        # if the user has admin permissions, disable them
        if permissions[userid]["admin"]:
            permissions[userid]["admin"] = False
            await ctx.send(f"Admin permissions disabled for userid {userid}")

        # and if they don't, enable them
        else:
            permissions[userid]["admin"] = True
            await ctx.send(f"Admin permissions enabled for userid {userid}")

        writeToYAML("permissions.yml", permissions)

    @admin.error
    async def adminError(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send('Nice try.')


def setup(bot):
    bot.add_cog(Admin(bot))
