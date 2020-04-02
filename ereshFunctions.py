import os
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


def getStatus():
    cogs = list()

    for file in os.listdir('./cogs'):
        if file.endswith(".py"):
            cogs.append(f"cogs.{file[:-3]}")
            print(f"{file[:-3]} appended to list cogs")

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
