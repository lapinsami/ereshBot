import math as m
import time
import discord
from discord.ext import commands
from application import BotState
from decimal import Decimal


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


def decimal_probability(n, k, p):
    p = Decimal(p)
    return Decimal(m.comb(n, k) * (p ** k) * ((1 - p) ** (n - k)))


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
                if increase < 0.00000001 and i > n / 8:
                    break
                chance_for_k_or_more += increase

        await ctx.send(f"With a {p} chance:\n"
                       f"Chance for exactly {k} in {n}: {chance_for_exactly_k:.6f}\n"
                       f"Chance for {k} or more in {n}: {chance_for_k_or_more:.6f}")

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
        # Either of these 2, depending on if you round up or down (for 4 digit precision)
        # Numbers will change when NA rateup goes to 0.8%
        # 1312        1-((1-0.007)^1312) = 0.99990059367, lowest over 0.9999
        # 1254        1-((1-0.007)^1254) = 0.99985059758, lowest over 0.99985
        # 0.8% numbers:
        # 1147        1-((1-0.008)^1147) = 0.99990025572, lowest over 0.9999
        # 1097        1-((1-0.008)^1097) = 0.99985095948, lowest over 0.99985

        # 1-((1-0.01)^877)
        # 1-((1-0.007)^1254)
        # 1-((1-0.03)^290)
        # 1-((1-0.015)^583)

        max_rolls = {
            'ssr': 877,
            'banner_ssr': 1254,
            'sr': 290,
            'banner_sr': 583
        }

        rolls = quartz // 3

        if server.upper() == 'JP':
            rolls += rolls // 10
            chances['banner_ssr'] = 0.008
            flag = '🇯🇵'
        else:
            server = 'NA'
            flag = '🇺🇸'

        start_time = time.perf_counter()

        for servant in chances.keys():
            p = chances.get(servant)
            servant_chance = 0.0

            if rolls < 2:
                break

            elif rolls < max_rolls.get(servant):
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

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        perf_message = f"{(elapsed_time * 1000):.4f} ms"

        rates = f"```"
        rates += f"SSR ▲       ≈ {(chances.get('banner_ssr') * 100):05.2f} %\n"
        rates += f"SSR         ≈ {(chances.get('ssr') * 100):05.2f} %\n"
        rates += f"SR ▲        ≈ {(chances.get('banner_sr') * 100):05.2f} %\n"
        rates += f"SR          ≈ {(chances.get('sr') * 100):05.2f} %\n"
        rates += f"```"

        footer = f"{quartz} SQ  |  {rolls} roll{'' if rolls == 1 else 's'}"
        footer += f"  |  {perf_message}"

        author_icon = 'https://cdn.discordapp.com/avatars/459704067359244289/a120d9f0a972e15d9ac41a01ac28bcdb.png'
        footer_icon = 'https://vignette.wikia.nocookie.net/fategrandorder/images/f/ff/Saintquartz.png'

        embed = discord.Embed(title=f'Fate/Grand Order {server.upper()}   {flag}',
                              colour=discord.Colour.from_rgb(239, 183, 131))
        embed.set_footer(icon_url=footer_icon, text=footer)
        #embed.set_author(name=BotState.STATUS['nickname'], icon_url=author_icon)
        embed.add_field(name='Servant chances (▲ = rateup):', value=rates, inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='genshin',
                      description='Chances for characters in Genshin Impact with x amount of rolls/primos',
                      brief='Roll chances in Genshin Impact',
                      aliases=['gi'])
    async def genshin(self, ctx, rolls="1", mode='rolls'):

        chances = (0.0026241784302653876,
                   0.005806457368718241,
                   0.008966475913102918,
                   0.012104234063419421,
                   0.01521973181966775,
                   0.018312969181847903,
                   0.021383946149959882,
                   0.024432662724003688,
                   0.027459118903979316,
                   0.03046331468988677,
                   0.03344525008172556,
                   0.036385040863026595,
                   0.03927305001634463,
                   0.04222385746976074,
                   0.045145119320038556,
                   0.0480432951945073,
                   0.05082001307616793,
                   0.05387274926446472,
                   0.05671157240928325,
                   0.05954576659038814,
                   0.06244270676691638,
                   0.06542470088264042,
                   0.06828759725400357,
                   0.07132555737168904,
                   0.07434264792415712,
                   0.07741626021575564,
                   0.08038334096109721,
                   0.08372060150375817,
                   0.08660363517489249,
                   0.08954111147433669,
                   0.09236383131742262,
                   0.09564550506701396,
                   0.09872064073226398,
                   0.10162237986269873,
                   0.10457295194507854,
                   0.10751677018633382,
                   0.11048965021248609,
                   0.11366111147433636,
                   0.11653982347172107,
                   0.1195426544622408,
                   0.12234859104282264,
                   0.12543054593004066,
                   0.1280240993788801,
                   0.1307343707093802,
                   0.13371667865315265,
                   0.13673904543968415,
                   0.1398262504086282,
                   0.1426254004576638,
                   0.145279601176853,
                   0.14805484145145253,
                   0.1508587381497199,
                   0.15405827394573163,
                   0.15677357960117452,
                   0.1597205165086606,
                   0.16270084995096196,
                   0.16572005884275665,
                   0.16881684210526066,
                   0.171632500817258,
                   0.17438868257600265,
                   0.17718716574043542,
                   0.1800330434782582,
                   0.1828894867603765,
                   0.18541820856488775,
                   0.18835315462569188,
                   0.19143707093821227,
                   0.1945760836874767,
                   0.19745471722784932,
                   0.19967121281464234,
                   0.2024283295194478,
                   0.20504892448512282,
                   0.207454560313825,
                   0.2097960444589704,
                   0.21233089244850945,
                   0.2146761817587415,
                   0.21736507355344561,
                   0.22031233082706442,
                   0.22366531546256616,
                   0.22768760379208558,
                   0.2331379666557664,
                   0.24058564236678295,
                   0.25331039757496493,
                   0.26805806579690317,
                   0.2848286470326011,
                   0.30362214128205867,
                   0.324438548545276,
                   0.34727786882225303,
                   0.37214010211298976,
                   0.39902524841748616,
                   0.42793330773574223,
                   0.45886428006775803,
                   0.56554,
                   0.5663202597402596,
                   0.570618909090909,
                   0.5748918578263841,
                   0.5791391059466848,
                   0.5833606534518113,
                   0.5875565003417635,
                   0.5917266466165414,
                   0.595871092276145,
                   0.5999898373205743,
                   0.6040828817498293,
                   0.6081502255639009,
                   0.6122631644328121,
                   0.6162116181758653,
                   0.6201109774435999,
                   0.6239681006864897,
                   0.6277920169990101,
                   0.6318815102974735,
                   0.6358796404053518,
                   0.6394581235697845,
                   0.6429322589081304,
                   0.6464142857142762,
                   0.650245681595283,
                   0.6537765348152895,
                   0.6573851912389572,
                   0.660885629290608,
                   0.6650051912389572,
                   0.668700536122906,
                   0.6725201242235924,
                   0.6760570709382051,
                   0.6804078457011995,
                   0.6839638247793295,
                   0.6875828179143408,
                   0.6905675057208136,
                   0.6937511278195387,
                   0.6963900686498753,
                   0.6993447728015588,
                   0.7020731023210096,
                   0.7047512389669723,
                   0.707461118012412,
                   0.7102658450473907,
                   0.7131234521085216,
                   0.7161994900294109,
                   0.7191688002615128,
                   0.7220924615887439,
                   0.7252297352075735,
                   0.728583942464847,
                   0.7318165152010353,
                   0.7349467146126076,
                   0.7382496632886455,
                   0.7415624779339544,
                   0.744493658058178,
                   0.747327721477596,
                   0.7497355279502995,
                   0.752484236678642,
                   0.7553122654462131,
                   0.7578605034324831,
                   0.7602683360575239,
                   0.7631859496567392,
                   0.766016521739119,
                   0.7690172082379749,
                   0.7712504870872721,
                   0.773586348479884,
                   0.7758871918927639,
                   0.7780398496240486,
                   0.7805730173259119,
                   0.7831408564890371,
                   0.7857897744360786,
                   0.7882137626675269,
                   0.7908510428244407,
                   0.793488407976451,
                   0.7961909905197659,
                   0.7990994965674938,
                   0.8024345472376474,
                   0.8064391042824332,
                   0.8109542007191772,
                   0.8158423275580134,
                   0.8221590781300957,
                   0.8296009022556268,
                   0.8380947629944302,
                   0.8480879241582091,
                   0.8584982534993609,
                   0.8698358389253765,
                   0.8821006804362684,
                   0.8952927780320364,
                   0.9094121317126808,
                   0.9244587414782013,
                   0.940432607328598,
                   0.9573337292638708,
                   0.97516210728402,
                   0.9939177413890454,
                   1.0)

        if not rolls.isdigit():
            await ctx.send("Please give a number")
            return

        rolls = abs(int(rolls))

        if mode in ("primos", "primogems", "primo", "gem", "gems"):
            primogems = rolls
            rolls = rolls // 160
        else:
            primogems = rolls * 160

        if rolls > 50000000000:
            await ctx.send("It's 100% alright")
            return

        chance = 0
        if rolls == 1:
            chance = 0.003

        elif rolls >= 180:
            chance = 1

        elif rolls > 1:
            chance = chances[rolls]

        non_banner_chance = 0
        if rolls == 1:
            non_banner_chance = 0.006

        elif rolls >= 90:
            non_banner_chance = 1.0

        elif rolls > 1:
            non_banner_chance = 1 - (1 - 0.006) ** rolls

        rates = f"```"
        rates += f"5⭐ ▲     ≈ {(chance * 100):.2f} %\n"
        #rates += f"5⭐       ≈ {(non_banner_chance * 100):.2f} %\n"
        rates += f"```"

        footer = f"{rolls} roll{'' if rolls == 1 else 's'}  |  {primogems} Primogems"

        author_icon = 'https://cdn.discordapp.com/avatars/459704067359244289/a120d9f0a972e15d9ac41a01ac28bcdb.png'
        footer_icon = 'https://static.wikia.nocookie.net/gensin-impact/images/1/1f/Item_Intertwined_Fate.png'

        embed = discord.Embed(title=f'Genshin Impact',
                              colour=discord.Colour.from_rgb(239, 183, 131))
        embed.set_footer(icon_url=footer_icon, text=footer)
        # embed.set_author(name=BotState.STATUS['nickname'], icon_url=author_icon)
        embed.add_field(name='Roll chances (▲ = rateup)', value=rates, inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='csgo',
                      description='Chances for a skin fith x rolls',
                      brief='Chances for skins',
                      aliases=['cs'])
    async def csgo(self, ctx, rolls="1", currency="keys"):

        if not rolls.isdigit():
            await ctx.send("A positive integer please")
            return

        try:
            rolls = abs(int(rolls))
        except ValueError:
            await ctx.send("A positive integer please")
            return

        if currency.lower() in ["dollar", "dollars", "usd", "$"]:
            rolls = int(rolls // 2.50)

        elif currency.lower() in ["euro", "eur", "e", "€"]:
            rolls = int(rolls // 2.10)

        if rolls > 50000000000:
            await ctx.send("It's 100% alright")
            return

        if rolls == 0:
            await ctx.send("0%")
            return

        chances = {
            'yellow': 10/3910,
            'red': 25/3910,
            'pink': 125/3910,
            'purple': 625/3910,
        }

        # 1-((1-(10/3910))^3439) = 0.99985026791, lowest possible value that gives us 4 digits of precision
        # 1-((1-(25/3910))^1373)
        # 1-((1-(125/3910))^271)
        # 1-((1-(625/3910))^51)
        tier_max_rolls = {
            'yellow': 3439,
            'red': 1373,
            'pink': 271,
            'purple': 51
        }

        start_time = time.perf_counter()

        for tier in chances.keys():
            p = round(chances.get(tier), 5)
            skin_chance = Decimal(0.0)

            if rolls < 2:
                break

            elif rolls < tier_max_rolls.get(tier):
                for i in range(rolls + 1):

                    if skin_chance > Decimal(0.99985):
                        skin_chance = Decimal(0.9999)
                        break

                    skin_chance_increase = decimal_probability(rolls, i + 1, p)

                    # Break if the chance doesn't grow much anymore, but only if at least 1/8 of cases calculated
                    if skin_chance_increase < Decimal(0.00001) and i > rolls / 8:
                        break

                    skin_chance += skin_chance_increase

                chances[tier] = float(skin_chance)

            else:
                chances[tier] = 0.9999

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        perf_message = f"{(elapsed_time * 1000):.4f} ms"

        rates = f"```"
        rates += f"🟡 Yellow      ≈ {(chances.get('yellow') * 100):05.2f} %\n"
        rates += f"🔴 Red         ≈ {(chances.get('red') * 100):05.2f} %\n"
        rates += f"🌸 Pink        ≈ {(chances.get('pink') * 100):05.2f} %\n"
        rates += f"🟣 Purple      ≈ {(chances.get('purple') * 100):05.2f} %\n"
        rates += f"```"

        footer = f"{rolls} case{'' if rolls == 1 else 's'}"
        footer += f"  |  {perf_message}"

        author_icon = 'https://cdn.discordapp.com/avatars/459704067359244289/a120d9f0a972e15d9ac41a01ac28bcdb.png'
        footer_icon = 'https://static.wikia.nocookie.net/cswikia/images/1/12/CsGOKey.png'

        embed = discord.Embed(title=f'Counter-Strike: Global Offensive',
                              colour=discord.Colour.from_rgb(239, 183, 131))
        embed.set_footer(icon_url=footer_icon, text=footer)
        #embed.set_author(name=BotState.STATUS['nickname'], icon_url=author_icon)
        embed.add_field(name='Skin chances:', value=rates, inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Math(bot))
