import disnake
from disnake.ext import commands
import os
from languages.logic.attribute import get_lang_data
from utils.role_check_util import check_trust_access

class CogReload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="reload_cogs", description="Перезагружает все коги бота")
    async def reload_cogs(self, inter: disnake.ApplicationCommandInteraction):
        if not await check_trust_access(inter):
            return

        await inter.response.defer(ephemeral=True)

        lang_data = get_lang_data().get("cogs_control", {})

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

        message = lang_data.get("reload_result")

        if success:
            message += lang_data.get("success_loaded").format(count=len(success))
        if failed:
            message += lang_data.get("failed_loaded").format(count=len(failed))
            message += "\n".join(f"• {error}" for error in failed)

        await inter.followup.send(message, ephemeral=True)


def setup(bot):
    bot.add_cog(CogReload(bot))
