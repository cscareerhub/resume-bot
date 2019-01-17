import os

from discord import Game
from dotenv import load_dotenv
from os.path import join, dirname
from discord.ext.commands import Bot

# This is from rolley
PREFIX = '>'
DQ_CHANNEL = 'daily-coding-challenge'

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.environ.get('TOKEN')
bot = Bot(command_prefix=PREFIX)


# Bot Events
@bot.event
async def on_ready():
    await bot.change_presence(game=Game(name="Something CS Related"))
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


if __name__ == '__main__':
    bot.run(TOKEN)
