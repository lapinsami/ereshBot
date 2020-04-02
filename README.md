# 「地の女神、エレシュキガルが命じます！」
A Python Discord bot using [discord.py](https://github.com/Rapptz/discord.py). Named after the character Ereshkigal from Fate/Grand Order.

#### Commands

Admin:
* `--admin [userid]` Toggles admin permissions for the user
* `--allowpm [userid]` Toggles private message permissions for the user
* `--ban [userid]` Prevents the user from running any commands
* `--unban [userid]` Unbans a user
    * Usage example: `--admin 0000000000` toggles admin rights for the userid "0000000000"
* `--disable [cog]` Disables a cog
* `--enable [cog]` Enables a cog
* `--reload [cog]` Reloads a cog
    * Usage example: `--reload all` reloads all cogs. Useful when you make changes to the code. `--disable math` disables the math cog and all commands in it.
* `--logout` Shuts down the bot
* `--nick [nickname]` Changes the nickname of the bot
    * Usage example: `--nick "A Python bot"`. Quote when spaces in the name.
* `--status [game][onlinestatus]` Sets the bot status.
    * Usage example: `--status "with Python" dnd`. Sets the status to "Playing with Python" and the online status to "do not disturb". Use quotes if your status has spaces.

DnD:
* `--roll [dice]` Rolls dice, DnD style.
    * Usage example: `--roll 2d6 1d4` rolls two 6-faced dice and one 4-faced die.

Math:
* `--prime [int]` Checks if the number is a prime. Keep the numbers below one trillion.
* `--square [number]` Squares a number
* `--squareroot [number]` Squareroots a number

Misc:
* `--dab` The bot dabs. Image file not in the repo because of copyright.
* `--info` Shows some information about the bot
* `--rin` Tells you a 100% truthful fact
No Category:
* `--help` The default help command in discord.py
