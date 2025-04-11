import disnake
from disnake.ext import commands
import os

from data.config import TRUST_ROLE_ID

class CogReload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="reload_cogs", description="Перезагружает все коги бота")
    async def reload_cogs(self, inter: disnake.ApplicationCommandInteraction):
        if not any(role.id == TRUST_ROLE_ID for role in inter.author.roles):
            await inter.response.send_message("У вас нет доступа к этой команде.", ephemeral=True)
            return

        await inter.response.defer(ephemeral=True)

        success = []
        failed = []

        loaded_cogs = list(self.bot.extensions.keys())

        for cog in loaded_cogs:
            try:
                self.bot.unload_extension(cog)
            except Exception as e:
                failed.append(f"{cog}: {str(e)}")

        for root, _, files in os.walk("cogs"):
            for file in files:
                if file.endswith(".py") and not file.startswith("_"):
                    cog_path = os.path.join(root, file)
                    cog = cog_path.replace(os.sep, ".")[:-3]
                    try:
                        self.bot.load_extension(cog)
                        success.append(cog)
                    except Exception as e:
                        failed.append(f"{cog}: {str(e)}")

        message = "**Результат перезагрузки когов:**\n"
        if success:
            message += f"Успешно загружено: {len(success)}\n"
        if failed:
            message += f"Ошибки при загрузке: {len(failed)}\n"
            message += "\n".join(f"• {error}" for error in failed)

        await inter.followup.send(message, ephemeral=True)

def setup(bot):
    bot.add_cog(CogReload(bot))
