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
                increase = probability(n, i, p)
                if round(increase, 8) < 0.00000001:
                    break
                chance_for_k_or_more += increase

        await ctx.send(f"With a {p} chance:\n"
                       f"Chance for exactly {k} in {n}: {chance_for_exactly_k}\n"
                       f"Chance for {k} or more in {n}: {chance_for_k_or_more}")

    @commands.command(name='sq',
                      description='Chances for a servant with x amount of SQ',
                      brief='Roll chance for x SQ',
                      aliases=['fgo'])
    async def fgo(self, ctx, quartz="3", server='NA'):

        if not quartz.isdigit():
            await ctx.send("Please give a number")
            return

        quartz = abs(int(quartz))

        if quartz > 50000000000:
            await ctx.send("It's 100% alright")
            return

        chances = {
            'ssr': 0.01,
            'banner_ssr': 0.007,
            'sr': 0.03,
            'banner_sr': 0.015
        }

        rolls = quartz // 3

        if server.upper() == 'JP':
            rolls += (rolls // 10)
            chances['banner_ssr'] = 0.008

        for servant in chances.keys():
            p = chances.get(servant)
            servant_chance = 0.0

            # Either of these 2, depending on if you round up or down (for 4 digit precision)
            # Numbers will change when NA rateup goes to 0.8%
            # 1312        1-((1-0.007)^1312) = 0.99990059367, lowest over 0.9999
            # 1254        1-((1-0.007)^1254) = 0.99985059758, lowest over 0.99985
            # 0.8% numbers:
            # 1147        1-((1-0.008)^1147) = 0.99990025572, lowest over 0.9999
            # 1097        1-((1-0.008)^1097) = 0.99985095948, lowest over 0.99985
            if rolls < 1254:
                for i in range(rolls + 1):

                    if servant_chance > 0.9999:
                        servant_chance = 0.9999
                        break

                    servant_chance_increase = probability(rolls, i + 1, p)

                    # Break if the chance doesn't grow much anymore, but only if at least 1/8 of cases calculated
                    if servant_chance_increase < 0.000001 and i > rolls / 8:
                        break
                    servant_chance += servant_chance_increase

                chances[servant] = servant_chance

            else:
                chances[servant] = 0.9999

        await ctx.send(f">>> For {quartz} <:sq:717830998091366518> ({rolls} roll{'' if rolls == 1 else 's'}) your chances are:\n"
                       f"Banner SSR (5\*): {(chances.get('banner_ssr') * 100):.2f}%\n"
                       f"SSR (5\*): {(chances.get('ssr') * 100):.2f}%\n"
                       f"Banner SR (4\*): {(chances.get('banner_sr') * 100):.2f}%\n"
                       f"SR (4\*): {(chances.get('sr') * 100):.2f}%\n"
                       f"<:gudako:717830982043959387>")


def setup(bot):
    bot.add_cog(Math(bot))
