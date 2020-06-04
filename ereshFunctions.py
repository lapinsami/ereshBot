import os
import subprocess
import discord
import yaml


def getFromYAML(file):
    with open(file, "r") as f:
        contents = yaml.full_load(f)
    return contents


def writeToYAML(file, contents):
    with open(file, 'w') as f:
        yaml.dump(contents, f)
    return


def commandLine(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    for line in process.stdout:
        print(line)
    process.wait()
    print(process.returncode)


def buildEmbed(title, message_title, message, footer, footer_icon):
    embed = discord.Embed(title=title,
                          colour=discord.Colour.from_rgb(239, 183, 131))
    embed.set_footer(icon_url=footer_icon, text=footer)
    embed.set_author(name=status['nickname'], icon_url='https://cdn.discordapp.com/avatars/459704067359244289/a120d9f0a972e15d9ac41a01ac28bcdb.png')
    embed.add_field(name=message_title, value=message, inline=False)

    return embed


def getMessage(msg_name, msg_arg0=None, msg_arg1=None):

    messages = {
        "logout": "Shutting down...",
        "disableCog": f"Cog {msg_arg0} disabled.",
        "enableCog": f"Cog {msg_arg0} enabled.",
        "reloadCog": f"Cog {msg_arg0} reloaded.",
        "disableAll": f"All cogs except admin disabled.",
        "enableAll": f"All cogs enabled.",
        "reloadAll": f"Reloaded all enabled cogs. Disabled cogs unaffected. Use --load all to load them.",
        "cogNotFound": f"No cog named {msg_arg0}.",
        "enablePm": f"Commands in PMs enabled for userid {msg_arg0}.",
        "disablePm": f"Commands in PMs disabled for userid {msg_arg0}.",
        "enableAdmin": f"Admin permissions enabled for userid {msg_arg0}.",
        "disableAdmin": f"Admin permissions disabled for userid {msg_arg0}.",
        "alreadyBanned": f"Userid {msg_arg0} is already banned.",
        "isNotBanned": f"Userid {msg_arg0} is not banned.",
        "banned": f"Userid {msg_arg0} banned.",
        "unBanned": f"Userid {msg_arg0} unbanned.",
        "isAdmin": f"Userid {msg_arg0} is an admin.",
        "nickChanged": f"Thus, shalt thou call me {msg_arg0}.",
        "statusChanged": f"Playing {msg_arg0} ({msg_arg1}).",
        "notOwner": f"Nice try."
    }

    return messages[msg_name]


def getStatus():
    cogs = list()

    for file in os.listdir('./cogs'):
        if file.endswith(".py"):
            cogs.append(f"cogs.{file[:-3]}")

    default_status = {
        "nickname": "ereshBot",
        "playingStatus": "with Rin",
        "onlineStatus": "online",
        "disabledCogs": list(),
        "availableCogs": cogs
    }

    if not os.path.isfile("status.yml"):
        writeToYAML("status.yml", default_status)
        return default_status
    else:
        return getFromYAML("status.yml")


def getPermissions():
    def_perms = {
        "useridhere": {
            "admin": False,
            "pm_user": False,
            "banned": False
        },
    }
    if not os.path.isfile("permissions.yml"):
        writeToYAML("permissions.yml", def_perms)

    return getFromYAML("permissions.yml")


def checkStatusMode(mode):
    if mode == 'dnd':
        return discord.Status.dnd
    elif mode == 'idle':
        return discord.Status.idle
    elif mode == 'invis':
        return discord.Status.invisible
    else:
        return discord.Status.online


status = getStatus()
permissions = getPermissions()

default_permissions = {
    "useridhere": {
        "admin": False,
        "pm_user": False,
        "banned": False
    },
}
