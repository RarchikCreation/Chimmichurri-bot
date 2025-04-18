from disnake.ext import commands
from disnake import TextChannel, Option
from disnake import ApplicationCommandInteraction

from languages.logic.attribute import get_lang_data
from utils.role_check_util import check_trust_access
from data.config import save_log_channel_id

class SelectAuditChannelCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="select_audit_channel", description="Выбрать канал для логов")
    async def select_audit_channel(
        self,
        inter: ApplicationCommandInteraction,
        channel: TextChannel = Option(name="канал", required=True)):
        if not await check_trust_access(inter):
            return

        save_log_channel_id(channel.id)

        lang_data = get_lang_data()
        lang_data = (((lang_data.get("commands") or {}).get("audit") or {}).get("select_audit_channel") or {})
        message = lang_data.get("changed").format(channel=channel.mention)
        await inter.response.send_message(message, ephemeral=True)

def setup(bot):
    bot.add_cog(SelectAuditChannelCog(bot))
