import discord


async def mainMenu(bot):
    message_aliases = ["1", "message", "msg"]
    exit_aliases = ["2", "shutdown", "logout", "exit", "quit"]
    help_aliases = ["help", "info", "commands"]

    print("\n# Enter a command: ")
    print("1. Send a message to a channel")
    print("2. Shut down the bot")

    while True:

        command = input("> ")

        if command in help_aliases:
            print("\n1. Send a message to a channel")
            print("2. Shut down the bot")

        elif command in message_aliases:

            print("\nEnter the channel ID (empty for default):")
            channel_id = input("> ")

            if channel_id == "":
                channel_id = 712329162618044476

            print("\nEnter the message:")
            message = input("> ")

            channel = bot.get_channel(int(channel_id))
            await channel.send(message)
            print("\nMessage sent.")

        elif command in exit_aliases:
            print("\nLogging out...")
            await bot.logout()
            return

        else:
            print("\nNot a command. Type 'help' for commands")
