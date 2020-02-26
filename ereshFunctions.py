import discord


def getListFromFile(file):
    with open(file, "r") as f:
        file_contents = f.read()
    lista = file_contents.split(",")
    # ^ creates an empty string at the end of the list because the file ends with a comma

    return lista[:-1]  # removes said empty string


def writeListToFile(lista, file, mode="append"):
    if mode == "overwrite":
        open(file, "w+").close()  # empties the file if overwriting

    f = open(file, "a+")
    for item in lista:
        f.write(f"{item},")
    f.close()


def checkStatusMode(mode):
    if mode == 'dnd':
        return discord.Status.dnd
    elif mode == 'idle':
        return discord.Status.idle
    elif mode == 'invis':
        return discord.Status.invisible
    else:
        return discord.Status.online
