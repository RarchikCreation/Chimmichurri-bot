import disnake
from disnake.ext import commands

from languages.logic.attribute import get_lang_data
from languages.logic.lang_loader import languages, save_global_language
from utils.role_check_util import check_trust_access

class LanguageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="lang_setup")
    async def lang_setup(self, inter: disnake.ApplicationCommandInteraction, lang: str):
        if not await check_trust_access(inter):
            return

        lang_data = get_lang_data()
        lang_data = (((lang_data.get("commands") or {}).get("lang") or {}).get("lang_setup") or {})

        if lang.lower() not in languages:
            await inter.response.send_message(lang_data.get("languages"), ephemeral=True)
            return
        save_global_language(lang.lower())
        await inter.response.send_message(lang_data.get("changed").format(lang=str(lang).upper()),ephemeral=True)


def setup(bot):
    bot.add_cog(LanguageCog(bot))
