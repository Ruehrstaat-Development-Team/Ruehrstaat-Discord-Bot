import configparser
from nextcord.ext import commands as nxCommands

import sys
import logging

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

if sys.version_info[0] < 3 or sys.version_info[1] < 11:
    logging.CRITICAL(f"Error: This program requires running python 3.11 or higher! You are running {str(sys.version_info[0])}.{str(sys.version_info[1])}")
    input("Press Enter to exit...")
    sys.exit()

import os
from dotenv import load_dotenv

load_dotenv()
config = configparser.ConfigParser()
config.read('config.ini')

BOT_TOKEN = os.getenv("BOT_TOKEN")

TESTING_GUILD_ID = int(config['TESTING']['TESTING_GUILD_ID'])

VERSION = "0.1.0"
BRANCH = "beta"
VERSIONDATE = "01.02.2023"
LONGVERSION = f"{VERSION} {BRANCH} {VERSIONDATE} - by MTN Media Dev Team"
PROGRAMNAME = "Ruehrstaat Discord Bot"
LONGPROGRAMNAME = f"{PROGRAMNAME} - by MTN Media Dev Team"
print(LONGPROGRAMNAME)
print(LONGVERSION)

bot = nxCommands.Bot()


# initialize carriers
from classes import carrier
from caching import recacheAllCarriers

recacheAllCarriers()

#on_ready
@bot.event
async def on_ready():
    logging.info(f"Logged in as {bot.user.name} - {bot.user.id}")
    logging.info("------")

from commands.admin import initAdminCommands
initAdminCommands(bot, {"TESTING_GUILD_ID": TESTING_GUILD_ID})

from commands.carrier import initCarrierCommands
initCarrierCommands(bot, {"TESTING_GUILD_ID": TESTING_GUILD_ID})

from commands.fun import initFunCommands
initFunCommands(bot, {"TESTING_GUILD_ID": TESTING_GUILD_ID})

from commands.captain import initCaptainCommands
initCaptainCommands(bot, {"TESTING_GUILD_ID": TESTING_GUILD_ID})

from commands.market import initMarketCommands
initMarketCommands(bot, {"TESTING_GUILD_ID": TESTING_GUILD_ID})

bot.run(BOT_TOKEN)

