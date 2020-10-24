import os
import discord
from discord import File
from discord.ext import commands
from application import getMessage, commandLine
from PIL import Image, ImageEnhance, ImageOps
import requests
import uuid
from io import BytesIO


class Dev(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='deepfry',
                      description='Deepfries an image',
                      brief='Deepfries an image',
                      aliases=['df'])
    async def deepfry(self, ctx, col="3.0", cont="2.0", shrp="10.0"):

        def isnumber(s):
            try:
                float(s)
                return True
            except ValueError:
                return False

        def check(m):
            if len(m.attachments) > 0 and m.author == ctx.message.author:
                return m.attachments[0].url.split(".")[-1] in ['jpg', 'png']

        for value in [col, cont, shrp]:
            if not isnumber(value):
                await ctx.send("Usage example: `--df 3.2 2.1 10.7`")
                return

        col = float(col)
        cont = float(cont)
        shrp = float(shrp)

        if col > 500.0 or col < 0.0:
            col = 1.0

        if cont > 500.0 or cont < 0.0:
            cont = 1.0

        if shrp > 500.0 or shrp < 0.0:
            shrp = 1.0

        await ctx.send("Give me an image in the next 10 seconds")

        message = await self.bot.wait_for('message', check=check, timeout=10.0)
        response = requests.get(message.attachments[0].url)

        img = Image.open(BytesIO(response.content))
        img = img.copy().convert('RGB')

        img = ImageEnhance.Sharpness(img).enhance(shrp / 3)
        img = ImageEnhance.Color(img).enhance(col)
        img = ImageEnhance.Contrast(img).enhance(cont)
        img = ImageEnhance.Sharpness(img).enhance(shrp * 2 / 3)

        img = ImageOps.posterize(img, 4)
        arr = BytesIO()
        img.save(arr, format='PNG')
        arr.seek(0)

        await ctx.send(file=discord.File(arr, filename='fried.png'))

    @deepfry.error
    async def adminError(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send(getMessage("notOwner"))

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


def setup(bot):
    bot.add_cog(Dev(bot))
