import disnake
from disnake.ext import commands
from data.config import TRUST_ROLE_ID

class LoadCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="load_cog", description="Загрузить ког")
    async def load(self, inter: disnake.ApplicationCommandInteraction, cog_name: str = commands.Param(description="Имя кога")):
        if not any(role.id == TRUST_ROLE_ID for role in inter.author.roles):
            await inter.response.send_message("У вас нет доступа к этой команде.", ephemeral=True)
            return

        await inter.response.defer(ephemeral=True)

        try:
            self.bot.load_extension(cog_name)
            await inter.followup.send(f"Ког `{cog_name}` загружен", ephemeral=True)
        except commands.ExtensionAlreadyLoaded:
            await inter.followup.send(f"Ког `{cog_name}` уже загружен", ephemeral=True)
        except commands.ExtensionNotFound:
            await inter.followup.send(f"Ког `{cog_name}` не найден", ephemeral=True)
        except Exception as e:
            await inter.followup.send(f"Ошибка при загрузке: {str(e)}", ephemeral=True)

def setup(bot):
    bot.add_cog(LoadCog(bot))
