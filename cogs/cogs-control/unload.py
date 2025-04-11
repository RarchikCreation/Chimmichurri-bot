import disnake
from disnake.ext import commands
from data.config import TRUST_ROLE_ID

class UnloadCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="unload_cog", description="Загрузить ког")
    async def unload_cog(self, inter: disnake.ApplicationCommandInteraction, cog_name: str = commands.Param(description="Имя кога")):
        if not any(role.id == TRUST_ROLE_ID for role in inter.author.roles):
            await inter.response.send_message("У вас нет доступа к этой команде.", ephemeral=True)
            return

        await inter.response.defer(ephemeral=True)

        try:
            self.bot.unload_extension(cog_name)
            await inter.followup.send(f"Ког `{cog_name}` выгружен", ephemeral=True)
        except commands.ExtensionNotLoaded:
            await inter.followup.send(f"Ког `{cog_name}` не был загружен", ephemeral=True)
        except Exception as e:
            await inter.followup.send(f"Ошибка при загрузке: {str(e)}", ephemeral=True)

def setup(bot):
    bot.add_cog(UnloadCog(bot))
