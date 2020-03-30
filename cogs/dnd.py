import sys
import random as r
from discord.ext import commands


class DnD(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='roll',
                      description='Rolls dice, dnd style',
                      brief='Rolls dice',
                      aliases=['dnd', 'dice'])
    async def roll_dnd(self, ctx, *arguments):
        arguments = list(arguments)
        if len(arguments) > 15:
            message = "Maximum amount of dice: 15"
            await ctx.send(message)
            return

        total_tulokset = 0
        message = ">>> "
        splitter = "---------------\n"

        if len(arguments) == 0:
            arguments = ['1d6', ]

        for i in range(len(arguments)):
            if not arguments[i].split('d')[0]:
                arguments[i] = f"1d{arguments[i].split('d')[1]}"

        for noppa in arguments:
            try:
                maara = noppa.split("d")[0]
                maara = int(maara)
            except (IndexError, ValueError):
                maara = 1
            try:
                maksimi = noppa.split("d")[1]
                maksimi = int(maksimi)
            except (IndexError, ValueError):
                maksimi = 6

            if maara < 1 or maksimi < 1:
                message = "Use numbers above 0, please"
                await ctx.send(message)
                return

            if maara > 100 or maksimi > 1000:
                message = "Maximum amount of rolls per die: 100\nLargest die: d1000"
                await ctx.send(message)
                return

            message += f"Throwing d{maksimi} {maara} times:\n"
            nopan_tulokset = list()

            for j in range(maara):
                heitto = r.randint(1, maksimi)
                nopan_tulokset.append(heitto)
                message += f"{heitto}"
                if j != maara - 1:
                    message += ", "

            message += f"\nTotal for d{maksimi}: {sum(nopan_tulokset)}\n"
            message += splitter
            total_tulokset += sum(nopan_tulokset)

        message += f"Final total: {total_tulokset}"

        if len(message) < 1950:
            await ctx.send(message)
        else:
            multi_message = message.split(splitter)
            message = ""
            for i in range(len(multi_message)):
                if (len(message) + len(multi_message[i]) + len(splitter)) < 1950:
                    message += splitter
                    message += multi_message[i]
                else:
                    await ctx.send(message)
                    message = ">>> "
                    message += splitter
                    message += multi_message[i]

            await ctx.send(message)


def setup(bot):
    bot.add_cog(DnD(bot))
