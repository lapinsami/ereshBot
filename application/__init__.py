import os
COGS = list()

for file in os.listdir('application/cogs'):
    if file.endswith(".py") and 'init' not in file:
        COGS.append(f"cogs.{file[:-3]}")