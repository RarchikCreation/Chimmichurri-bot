import disnake
from disnake.ext import commands
import os

from data.config import TOKEN
from utils.logger_util import logger

intents = disnake.Intents(
    guilds=True,
    messages=True,
    members=True,
    message_content=True,
    voice_states=True
)

bot = commands.InteractionBot(intents=intents)

@bot.event
async def on_ready():
    logger(f"###################### {bot.user} ######################")

def load_cogs():
    for root, _, files in os.walk("cogs"):
        for file in files:
            if file.endswith(".py") and not file.startswith("_"):
                cog = f"{root.replace(os.sep, '.')}.{file[:-3]}"
                if cog not in bot.extensions:
                    try:
                        bot.load_extension(cog)
                        logger(f"{cog} has been loaded")
                    except Exception as e:
                        logger(f"Error loading cog {cog}: {e}")

if __name__ == "__main__":
    load_cogs()
    bot.run(TOKEN)
