import disnake
from disnake.ext import commands

from languages.logic.attribute import get_lang_data
from utils.role_check_util import check_trust_access

class LoadCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="load_cog", description="Загрузить ког")
    async def load(self, inter: disnake.ApplicationCommandInteraction, cog_name: str = commands.Param(description="Имя кога")):
        if not await check_trust_access(inter):
            return

        await inter.response.defer(ephemeral=True)

        lang_data = get_lang_data().get("cogs_control", {})

        try:
            self.bot.load_extension(cog_name)
            await inter.followup.send(lang_data.get("load").format(cog_name=cog_name), ephemeral=True)
        except commands.ExtensionAlreadyLoaded:
            await inter.followup.send(lang_data.get("already_loaded").format(cog_name=cog_name), ephemeral=True)
        except commands.ExtensionNotFound:
            await inter.followup.send(lang_data.get("not_found").format(cog_name=cog_name), ephemeral=True)
        except Exception as e:
            await inter.followup.send(lang_data.get("error").format(error=str(e)), ephemeral=True)

def setup(bot):
    bot.add_cog(LoadCog(bot))
