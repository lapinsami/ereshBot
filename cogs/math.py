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


def probability(n, k, p):
    return m.comb(n, k) * (p ** k) * ((1 - p) ** (n - k))


class Math(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='square',
                      description='Squares the number',
                      brief='Square x')
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

    @commands.command(name='prob',
                      description='--prob <float>% <int k>/<int n>',
                      brief='k in n',
                      aliases=['probability', 'chance'])
    async def prob(self, ctx, percentage, fraction):
        k, n = fraction.split("/")
        percentage = percentage.replace("%", "")

        n = int(n)
        k = int(k)
        p = float(percentage) / 100
        if p > 1:
            p = 1

        chance_for_exactly_k = probability(n, k, p)
        chance_for_k_or_more = chance_for_exactly_k

        if n > k:
            for i in range(k + 1, n + 1):
                chance_for_k_or_more += probability(n, i, p)

        await ctx.send(f"With a {p} chance:\n"
                       f"Chance for exactly {k} in {n}: {chance_for_exactly_k}\n"
                       f"Chance for {k} or more in {n}: {chance_for_k_or_more}")

    @commands.command(name='sq',
                      description='Chances for a servant with x amount of SQ',
                      brief='Roll chance for x SQ',
                      aliases=['fgo'])
    async def fgo(self, ctx, quartz, server='NA'):
        quartz = int(quartz)
        rolls = quartz // 3

        if server.upper() == 'JP':
            rolls += (rolls // 10)

        single_chances = {
            'ssr': 0.01,
            'banner_ssr': 0.008,
            'sr': 0.03,
            'banner_sr': 0.015
        }

        total_chances = {
            'ssr': 0.0,
            'banner_ssr': 0.0,
            'sr': 0.0,
            'banner_sr': 0.0
        }

        for servant in total_chances.keys():
            p = single_chances.get(servant)
            servant_chance = probability(rolls, 1, p)
            for i in range(1, rolls + 1):
                servant_chance += probability(rolls, i+1, p)

            total_chances[servant] = servant_chance

        await ctx.send(f">>> For {quartz} <:sq:717830998091366518> ({rolls} rolls) your chances are:\n"
                       f"SSR (5\*): {round(total_chances.get('ssr') * 100, 2)}%\n"
                       f"Banner SSR (5\*): {round(total_chances.get('banner_ssr') * 100, 2)}%\n"
                       f"SR (4\*): {round(total_chances.get('sr') * 100, 2)}%\n"
                       f"Banner SR (4\*): {round(total_chances.get('banner_sr') * 100, 2)}%\n"
                       f"<:gudako:717830982043959387>")


def setup(bot):
    bot.add_cog(Math(bot))
