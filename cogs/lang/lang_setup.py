import disnake
from disnake.ext import commands

from data.config import TRUST_ROLE_ID
from languages.logic.lang_loader import languages, save_global_language

class LanguageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="lang_setup")
    async def lang_setup(self, inter: disnake.ApplicationCommandInteraction, lang: str):
        if not any(role.id == TRUST_ROLE_ID for role in inter.author.roles):
            await inter.response.send_message("У вас нет доступа к этой команде.", ephemeral=True)
            return

        if inter.guild and inter.guild.owner_id == inter.author.id:
            if lang.lower() not in languages:
                await inter.response.send_message("Доступные языки: ru, eng", ephemeral=True)
                return
            save_global_language(lang.lower())
            await inter.response.send_message(f"Язык изменён на {lang.upper()}", ephemeral=True)
        else:
            await inter.response.send_message("У вас нет доступа к этой команде", ephemeral=True)

def setup(bot):
    bot.add_cog(LanguageCog(bot))
