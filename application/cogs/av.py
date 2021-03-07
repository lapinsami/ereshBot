import os
from io import BytesIO
import uuid
import regex as re
import requests
from PIL import Image, ImageDraw, ImageFont
import nekos

import discord
from discord import File
from discord.ext import commands

from application import getMessage, commandLine


class Av(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='dab',
                      description='Ereshkigal dabs',
                      brief='Eresh dabs')
    async def dab(self, ctx):
        await ctx.send(file=File('application/media/eresh-dab.png'))

    @commands.command(name='crab',
                      description='--crab <upper text>,<lower text>',
                      brief='Crabs')
    async def crab(self, ctx, *args):
        # TODO: subtitles instead of drawtext
        # TODO: line/underlined text
        msg = ''
        for i in range(len(args)):
            msg += args[i]
            msg += " "

        if len(msg.split(",")) != 2:
            await ctx.send("Give me 2 messages separated by a comma")
            return

        msg1 = re.sub(r'[\W_]+', ' ', msg[:-1].upper().split(",")[0])
        msg2 = re.sub(r'[\W_]+', ' ', msg[:-1].upper().split(",")[1])

        if len(msg1) > 40 or len(msg2) > 40:
            await ctx.send("Max message length 40 craracters. Cutting to size.")

        msg1 = msg1[:40]
        msg2 = msg2[:40]

        if len(msg1) == 0 and len(msg2) == 0:
            await ctx.send("Give me at least one message containing letters and/or numbers")
            return

        video = "application/media/crab3.mp4"
        font = "application/media/migu2m.ttf"
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

    @commands.command(name='neko',
                      description='neko',
                      brief='neko',
                      aliases=['nekos'])
    async def neko(self, ctx, category=None):
        allowed_categories = ['feet', 'yuri', 'trap', 'futanari', 'hololewd', 'lewdkemo', 'solog',
                              'feetg', 'cum', 'erokemo', 'les', 'wallpaper', 'lewdk', 'ngif', 'tickle',
                              'lewd', 'feed', 'gecg', 'eroyuri', 'eron', 'cum_jpg', 'bj', 'nsfw_neko_gif',
                              'solo', 'kemonomimi', 'nsfw_avatar', 'gasm', 'poke', 'anal', 'slap', 'hentai',
                              'avatar', 'erofeet', 'holo', 'keta', 'blowjob', 'pussy', 'tits', 'holoero',
                              'lizard', 'pussy_jpg', 'pwankg', 'classic', 'kuni', 'waifu', 'pat', '8ball',
                              'kiss', 'femdom', 'neko', 'spank', 'cuddle', 'erok', 'fox_girl', 'boobs',
                              'random_hentai_gif', 'hug', 'ero', 'smug', 'goose', 'baka', 'woof']

        if not category:
            msg = "```Categories:\n\n"
            msg += ", ".join(allowed_categories)
            msg += "```"
            await ctx.send(msg)

        elif category in allowed_categories:
            await ctx.send(nekos.img(category))

        else:
            await ctx.send("Not a valid category. Run `--neko` to see the categories.")

    @neko.error
    async def nekoError(self, ctx, error):
        await ctx.send(f"Error: {error}")

    @commands.command(name='possufy',
                      description='Possufies a video',
                      brief='Blame possu',
                      aliases=['possu'])
    async def possufy(self, ctx):

        def check(m):
            if len(m.attachments) > 0 and m.author == ctx.message.author:
                return m.attachments[0].url.split(".")[-1] in ['mp4', 'webm']

        await ctx.send("Give me a video in the next 20 seconds")

        message = await self.bot.wait_for('message', check=check, timeout=20.0)
        response = requests.get(message.attachments[0].url)

        fname = str(uuid.uuid4()).replace("-", "")[:10] + "." + message.attachments[0].url.split(".")[-1]
        output = "possufied_" + fname.split(".")[0] + ".mp4"

        with open(fname, 'wb') as f:
            f.write(BytesIO(response.content).read())

        ffmpeg = ["ffmpeg", "-i", f"{fname}", "-i", f"{fname}", "-c:v", "libx264", "-preset", "ultrafast",
                  "-s", "128x96", "-filter:v", "fps=10", "-crf", "51", "-c:a", "libopus", "-ac", "1", "-ar",
                  "8000", "-b:a", "1k", "-vbr", "constrained", "-strict", "-2", "-shortest", f"{output}"]

        commandLine(ffmpeg)

        if os.path.exists(fname) and os.path.exists(output):
            if os.path.getsize(fname) > 1024:
                await ctx.send(file=File(output))
            else:
                await ctx.send("Something went wrong")

            os.remove(fname)
            os.remove(output)
        else:
            await ctx.send("Something went wrong")

    @possufy.error
    async def adminError(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send(getMessage("notOwner"))

    @commands.command(name='pikachu',
                      description='--pikachu row1, row2, row3',
                      brief='Surprised Pikachu',
                      aliases=['pika'])
    async def pikachu(self, ctx, *args):
        hq = False
        if not args:
            text = "Käyttäjä: Testaa komentoa ilman tekstiä, Teksti:, Käyttäjä:"
        else:
            if args[0] in ("-hq", "-h", "-high", "--hq", "--h", "--high"):
                args = args[1:]
                hq = True

            text = " ".join(args)

        text_rows = text.replace(", ", "\n").replace(",", "\n").strip().split("\n")
        text = "\n".join(text_rows).strip()

        fontsize = 36
        line_spacing = 3
        # font = ImageFont.truetype("application/media/NotoSansCJKjp-Regular.otf", size=fontsize)
        font = ImageFont.truetype("application/media/migu2m.ttf", size=fontsize)

        if hq:
            img = Image.open("application/media/pika-hq.png")
        else:
            img = Image.open("application/media/pika.png")

        img = img.copy().convert("RGB")
        img_width, img_height = img.size
        line_max_chars = int(img_width / fontsize * 2)  # Japanese characters take up 2
        rows = list()
        current_row = ""
        row_len = 0
        pattern = re.compile(r'([０-９]|[Ａ-ｚ]|[\p{IsHan}\p{IsBopo}\p{IsHira}\p{IsKatakana}]+)', re.UNICODE)

        for i, c in enumerate(text):

            c_len = 2 if re.search(pattern, c) else 1

            if re.search('([ｧ-ﾝﾞﾟ])', c):
                c_len = 1

            # Newline
            if c == "\n":
                rows.append(current_row)
                current_row = ""
                row_len = 0

            # Below max
            elif row_len + c_len < line_max_chars:
                current_row += c
                row_len += c_len

                if i == len(text) - 1:
                    rows.append(current_row)

            # Exact
            elif row_len + c_len == line_max_chars:
                current_row += c
                rows.append(current_row)
                current_row = ""
                row_len = 0

            # Over
            elif row_len + c_len > line_max_chars:
                rows.append(current_row)
                current_row = c
                row_len = c_len

        rows = rows[:20]
        text = "\n".join(rows)
        text_height = fontsize * len(rows) + line_spacing * len(rows)

        canvas = Image.new("RGB", (img_width, img_height + text_height), color="#FFFFFF")
        canvas.paste(img, (0, text_height))

        if text:
            draw = ImageDraw.Draw(canvas)
            draw.multiline_text((0, 0), text, fill="black", font=font, anchor=None, spacing=line_spacing, align="left")
            del draw

            arr = BytesIO()
            canvas.save(arr, format='PNG')
            arr.seek(0)

        else:
            arr = BytesIO()
            img.save(arr, format='PNG')
            arr.seek(0)

        await ctx.send(file=discord.File(arr, filename='pikachu.png'))


def setup(bot):
    bot.add_cog(Av(bot))
