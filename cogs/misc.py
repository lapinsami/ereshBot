import os
import sys
import time
from discord.ext import commands
from discord import File
import uuid

sys.path.insert(0, '../')
from ereshFunctions import status, commandLine


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

    @commands.command(name='crab',
                      description='--crab <upper text>,<lower text>',
                      brief='Crabs')
    async def crab(self, ctx, *args):
        msg = ''
        for i in range(len(args)):
            msg += args[i]
            msg += " "

        if len(msg.split(",")) != 2:
            await ctx.send("Give me 2 messages separated by a comma")
            return

        msg1, msg2 = msg[:-1].split(",")
        video = "crab3.mp4"
        salt = str(uuid.uuid4()).replace("-", "")[:5]
        output = f'{msg1}_{msg2}_{salt}.mp4'

        ffmpeg = ['ffmpeg', '-i', f'{video}', '-vf',
                  f'[in]drawtext=fontfile=mplus.ttf:text={msg1}:fontcolor=white:fontsize=72:bordercolor=black:borderw=2:x=(w-text_w)/2:y=(h-text_h-text_h)/2,drawtext=fontfile=mplus.ttf:text={msg2}:fontcolor=white:fontsize=72:bordercolor=black:borderw=2:x=(w-text_w)/2:y=(h-text_h-text_h)/2+72[out]',
                  '-codec:a', 'copy', '-preset', 'veryfast', '-y', f'{output}']

        commandLine(ffmpeg)

        await ctx.send(file=File(output))

        if os.path.exists(output):
            os.remove(output)

    @commands.command(name='info',
                      description='Information about the bot and its status',
                      brief='Get the bot status and info')
    async def info(self, ctx):
        message = ""
        multiline_message = list()
        multiline_message.append(f">>> Ereshkigal https://github.com/Vogelchevalier/ereshBot")
        multiline_message.append(f"Nickname: {status['nickname']}")
        multiline_message.append(f"Status: {status['playingStatus']} ({status['onlineStatus']})")
        multiline_message.append(f"Available cogs: {status['availableCogs']}")
        multiline_message.append(f"Disabled cogs: {status['disabledCogs']}")

        for line in multiline_message:
            message += f"{line}\n"

        await ctx.send(message)


def setup(bot):
    bot.add_cog(Misc(bot))
