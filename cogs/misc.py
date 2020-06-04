import os
import sys
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

        msg1, msg2 = msg[:-1].upper().replace(":", "").replace("=", "").replace("/", "").split(",")

        if len(msg1) > 40 or len(msg2) > 40:
            await ctx.send("Max message length 40 craracters. Cutting to size.")

        msg1 = msg1[:40]
        msg2 = msg2[:40]

        video = "crab3.mp4"
        font = "migu2m.ttf"
        max_f_size = "64"
        f_color = "white"

        max_text_width = 1080
        f_size = min(int(max_f_size), max_text_width // max(len(msg1), len(msg2)))

        salt = str(uuid.uuid4()).replace("-", "")[:5]
        output = f'{msg1}_{msg2}_{salt}.mp4'

        line_args1 = f'drawtext=fontfile={font}:text='
        line_args2 = f':fontcolor={f_color}:fontsize={f_size}:bordercolor=black:borderw=2:x=(w-text_w)/2:y=(h-text_h-text_h)/2'

        ffmpeg = ['ffmpeg', '-i', f'{video}', '-vf',
                  f'[in]{line_args1}{msg1}{line_args2},{line_args1}{msg2}{line_args2}+{f_size}[out]',
                  '-codec:a', 'copy', '-preset', 'veryfast', '-y', f'{output}']

        commandLine(ffmpeg)

        if os.path.exists(output):
            if os.path.getsize(output) > 1024:
                await ctx.send(file=File(output))
            else:
                await ctx.send("Something went wrong")

            os.remove(output)
        else:
            await ctx.send("Something went wrong")

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
