from discord.ext import commands
import discord
from riotwatcher import LolWatcher, ApiError
from application import checkStatusMode, writeToYAML, getMessage, BotState, Auth


def isAdmin(ctx):
    if ctx.author.id in BotState.PERMS.keys():
        admin = BotState.PERMS[ctx.author.id]["admin"]
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

        BotState.STATUS["nickname"] = nickname
        await ctx.send(getMessage("nickChanged", nickname))
        await ctx.guild.get_member(self.bot.user.id).edit(nick=nickname)
        writeToYAML("application/status.yml", BotState.STATUS)

    # Sets the status
    @commands.command(name='status',
                      description='Sets the status',
                      brief='Set status')
    @commands.check(isAdmin)
    async def status(self, ctx, game, mode):
        playing = discord.Game(game)
        online = checkStatusMode(mode)

        BotState.STATUS["playingStatus"] = str(playing)
        BotState.STATUS["onlineStatus"] = str(online)
        await ctx.send(getMessage("statusChanged", str(playing), str(online)))
        await self.bot.change_presence(status=online, activity=playing)
        writeToYAML("application/status.yml", BotState.STATUS)

    # Logs out the bot
    @commands.command(name='logout',
                      description="Shuts down the bot",
                      brief="Shutdown",
                      aliases=['close', 'shutdown'])
    @commands.is_owner()
    async def logout(self, ctx):
        await ctx.send(getMessage("logout"))
        await ctx.bot.logout()

    # Toggle PMs
    @commands.command(name='allowpm',
                      description="Toggles between allowing and not allowing commands in PMs for user",
                      brief="Allow commands in PMs",
                      aliases=['pm'])
    @commands.check(isAdmin)
    async def togglePm(self, ctx, userid):

        # if no permissions set for the userid, set them to default
        if userid not in BotState.PERMS.keys():
            BotState.PERMS[str(userid)] = BotState.DEF_PERMS.copy()

        # if the user has pm permissions, disable them
        # and if they don't, enable them
        if BotState.PERMS[userid]["pm_user"]:
            BotState.PERMS[userid]["pm_user"] = False
            await ctx.send(getMessage("disablePm", userid))
        else:
            BotState.PERMS[userid]["pm_user"] = True
            await ctx.send(getMessage("enablePm", userid))

        writeToYAML("application/permissions.yml", BotState.PERMS)

    # Ban user
    @commands.command(name='ban',
                      description="Bans user from using the bot",
                      brief="Ban user")
    @commands.check(isAdmin)
    async def banUser(self, ctx, userid):

        # if no permissions set for the userid, set them to default
        if userid not in BotState.PERMS.keys():
            BotState.PERMS[str(userid)] = BotState.DEF_PERMS.copy()

        # if user already banned, do nothing
        # if user not banned, ban them (if not admin)
        if BotState.PERMS[userid]["banned"]:
            await ctx.send(getMessage("alreadyBanned", userid))
        elif not BotState.PERMS[userid]["admin"]:
            BotState.PERMS[userid]["banned"] = True
            await ctx.send(getMessage("banned", userid))
        else:
            await ctx.send(getMessage("isAdmin", userid))

        writeToYAML("application/permissions.yml", BotState.PERMS)

    # Unban user
    @commands.command(name='unban',
                      description="Unbans user from using the bot",
                      brief="Unban user")
    @commands.check(isAdmin)
    async def unbanUser(self, ctx, userid):

        # if no permissions set for the userid, set them to default
        if userid not in BotState.PERMS.keys():
            BotState.PERMS[str(userid)] = BotState.DEF_PERMS.copy()

        # if user banned, unban them
        # if user not banned, do nothing
        if BotState.PERMS[userid]["banned"]:
            BotState.PERMS[userid]["banned"] = False
            await ctx.send(getMessage("unBanned", userid))
        else:
            await ctx.send(getMessage("isNotBanned", userid))

        writeToYAML("application/permissions.yml", BotState.PERMS)

    # Enable cog
    @commands.command(name='enable',
                      description="Enables a cog",
                      brief="Enable cog",
                      aliases=['load'])
    @commands.check(isAdmin)
    async def enable(self, ctx, ext):

        # if "all" as the argument, load all cogs
        if ext == "all":
            for extension in BotState.STATUS["disabledCogs"]:
                if extension != "cogs.admin":
                    self.bot.load_extension(f'application.{extension}')

            BotState.STATUS["disabledCogs"] = list()

            await ctx.send(getMessage("enableAll"))

        # load the cog given as the argument
        elif f"cogs.{ext}" in BotState.STATUS["availableCogs"]:
            self.bot.load_extension(f"application.cogs.{ext}")
            BotState.STATUS["disabledCogs"].remove(f"cogs.{ext}")
            await ctx.send(getMessage("enableCog", ext))

        else:
            await ctx.send(getMessage("cogNotFound", ext))

        # write status to file
        writeToYAML("application/status.yml", BotState.STATUS)

    # Disable cog
    @commands.command(name='disable',
                      description="Disables a cog",
                      brief="Disable cog",
                      aliases=['unload'])
    @commands.check(isAdmin)
    async def disable(self, ctx, ext):

        # if "all" as the argument, unload all cogs
        if ext == "all":
            for extension in BotState.STATUS["availableCogs"]:
                if extension != "cogs.admin" and extension not in BotState.STATUS["disabledCogs"]:
                    self.bot.unload_extension(f'application.{extension}')
                    BotState.STATUS["disabledCogs"].append(extension)

            await ctx.send(getMessage("disableAll"))

        # unload the cog given as the argument
        elif f"cogs.{ext}" in BotState.STATUS["availableCogs"]:
            if ext != "admin" and ext not in BotState.STATUS["disabledCogs"]:
                self.bot.unload_extension(f"application.cogs.{ext}")
                BotState.STATUS["disabledCogs"].append(f"cogs.{ext}")
                await ctx.send(getMessage("disableCog", ext))

        else:
            await ctx.send(getMessage("cogNotFound", ext))

        # write status to file
        writeToYAML("application/status.yml", BotState.STATUS)

    # Reload cog
    @commands.command(name='reload',
                      description="Reloads a cog",
                      brief="Reload cog",
                      aliases=['re'])
    @commands.check(isAdmin)
    async def reload(self, ctx, ext):

        # if "all" as the argument, reload all enabled cogs
        if ext == "all":
            for extension in BotState.STATUS["availableCogs"]:
                if extension not in BotState.STATUS["disabledCogs"]:
                    self.bot.reload_extension(f'application.{extension}')

            await ctx.send(getMessage("reloadAll"))

        # reload the cog given as the argument
        elif f"cogs.{ext}" not in BotState.STATUS["disabledCogs"]:
            self.bot.reload_extension(f"application.cogs.{ext}")
            await ctx.send(getMessage("reloadCog", ext))

        # write status to file
        writeToYAML("application/status.yml", BotState.STATUS)

    # Make user an admin
    @commands.command(name='admin',
                      description="Give admin permissions to the user",
                      brief="Make user an admin")
    @commands.is_owner()
    async def admin(self, ctx, userid):

        # if no permissions set for the userid, set them to default
        if userid not in BotState.PERMS.keys():
            BotState.PERMS[str(userid)] = BotState.DEF_PERMS.copy()

        # if the user has admin permissions, disable them
        if BotState.PERMS[userid]["admin"]:
            BotState.PERMS[userid]["admin"] = False
            await ctx.send(getMessage("disableAdmin", userid))

        # and if they don't, enable them
        else:
            BotState.PERMS[userid]["admin"] = True
            await ctx.send(getMessage("enableAdmin", userid))

        writeToYAML("application/permissions.yml", BotState.PERMS)

    @admin.error
    async def adminError(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send(getMessage("notOwner"))


def setup(bot):
    bot.add_cog(Admin(bot))
