import math as m
from discord.ext import commands


def convertNumber(number):
    if number.isdigit() or number.lstrip("-").isdigit():
        return float(number)
    elif number == "e":
        return m.e
    elif number == "pi":
        return m.pi
    elif number == "-e":
        return -m.e
    elif number == "-pi":
        return -m.pi
    else:
        return None


class Math(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='square',
                      description='Squares the number',
                      brief='Square x',
                      aliases=['sq'])
    async def square(self, ctx, number=''):
        if convertNumber(number) is None:
            await ctx.send("Numbers, please.")
            return
        else:
            number = convertNumber(number)

        squared_value = number * number
        message = str(number) + " squared is " + str(squared_value)

        await ctx.send(message)

    @commands.command(name='squareroot',
                      description='Squareroots the number',
                      brief="Squareroot x",
                      aliases=['sqrt'])
    async def squareroot(self, ctx, number=''):
        if convertNumber(number) is None:
            await ctx.send("Numbers, please.")
            return
        else:
            number = convertNumber(number)

        squarerooted_value = m.sqrt(abs(number))
        message = str(number) + " squarerooted is " + str(squarerooted_value)

        if number < 0:
            message += " i"

        await ctx.send(message)

    @commands.command(name='prime',
                      desription='Checks if the number is a prime',
                      brief='Check if x is prime',
                      aliases=['isprime, checkprime'])
    async def isPrime(self, ctx, number=''):
        if not number.isdigit():
            await ctx.send("Please give me a number below one trillion (1 000 000 000 000)")
            return

        number = int(number)

        if number > 999999999999:
            await ctx.send("Please give me a number below one trillion (1 000 000 000 000)")
            return

        if number <= 1:
            await ctx.send(f"{number} is not a prime.")
            return

        if number <= 3:
            await ctx.send(f"{number} is a prime!")
            return

        if number % 2 == 0:
            await ctx.send(f"{number} is not a prime.")
            return

        if number % 3 == 0:
            await ctx.send(f"{number} is not a prime.")
            return

        divisor = 5

        while divisor * divisor <= number:
            if number % divisor == 0 or number % (divisor + 2) == 0:
                await ctx.send(f"{number} is not a prime.")
                return
            divisor += 6

        await ctx.send(f"{number} is a prime!")


def setup(bot):
    bot.add_cog(Math(bot))
