import time
from decimal import Decimal

import discord
from discord.ext import commands

from application.cogs import math as emath


class Gacha(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

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

                    servant_chance_increase = emath.probability(rolls, i + 1, p)

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

        # author_icon = 'https://cdn.discordapp.com/avatars/459704067359244289/a120d9f0a972e15d9ac41a01ac28bcdb.png'
        footer_icon = 'https://vignette.wikia.nocookie.net/fategrandorder/images/f/ff/Saintquartz.png'

        embed = discord.Embed(title=f'Fate/Grand Order {server.upper()}   {flag}',
                              colour=discord.Colour.from_rgb(239, 183, 131))
        embed.set_footer(icon_url=footer_icon, text=footer)
        # embed.set_author(name=BotState.STATUS['nickname'], icon_url=author_icon)
        embed.add_field(name='Servant chances (▲ = rateup):', value=rates, inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='genshin',
                      description='Chances for characters in Genshin Impact with x amount of rolls/primos',
                      brief='Roll chances in Genshin Impact',
                      aliases=['gi'])
    async def genshin(self, ctx, rolls="1", mode='rolls'):

        with open("application/media/genshin-chances.txt", "r") as f:
            chances_str = f.readlines()

        chances = list()

        for s in chances_str:
            chances.append(float(s))

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

        rates = f"```"
        rates += f"5⭐ ▲     ≈ {(chance * 100):.2f} %\n"
        rates += f"```"

        footer = f"{rolls} roll{'' if rolls == 1 else 's'}  |  {primogems} Primogems"

        # author_icon = 'https://cdn.discordapp.com/avatars/459704067359244289/a120d9f0a972e15d9ac41a01ac28bcdb.png'
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
            'yellow': 10 / 3910,
            'red': 25 / 3910,
            'pink': 125 / 3910,
            'purple': 625 / 3910,
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

                    skin_chance_increase = emath.decimal_probability(rolls, i + 1, p)

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

        # author_icon = 'https://cdn.discordapp.com/avatars/459704067359244289/a120d9f0a972e15d9ac41a01ac28bcdb.png'
        footer_icon = 'https://static.wikia.nocookie.net/cswikia/images/1/12/CsGOKey.png'

        embed = discord.Embed(title=f'Counter-Strike: Global Offensive',
                              colour=discord.Colour.from_rgb(239, 183, 131))
        embed.set_footer(icon_url=footer_icon, text=footer)
        # embed.set_author(name=BotState.STATUS['nickname'], icon_url=author_icon)
        embed.add_field(name='Skin chances:', value=rates, inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Gacha(bot))
