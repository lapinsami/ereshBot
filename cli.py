import discord


async def mainMenu(bot):

    while True:
        print("Enter a command: ")

        print("1. Send a message to a channel")
        message_aliases = ["1", "message", "msg"]

        print("2. Shut down the bot")
        exit_aliases = ["2", "shutdown", "logout", "exit", "quit"]

        command = input("> ")

        if command in message_aliases:

            print("Enter the channel ID (empty for default)")
            channel_id = input("> ")

            if channel_id == "":
                channel_id = 712329162618044476

            print("Enter the message")
            message = input("> ")

            channel = bot.get_channel(int(channel_id))
            await channel.send(message)
            print("Message sent.\n")

        elif command in exit_aliases:
            print("Logging out...\n")
            await bot.logout()
            return

        else:
            print("Not a command")
