import disnake
from disnake.ext import commands

from data.config import log_channel_id
from languages.logic.attribute import get_lang_data


class ChannelCreateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: disnake.abc.GuildChannel):
        log_channel = channel.guild.get_channel(log_channel_id)
        if not log_channel:
            return

        async for entry in channel.guild.audit_logs(limit=1, action=disnake.AuditLogAction.channel_create):
            if entry.user == self.bot.user:
                return

            lang_data = get_lang_data().get("channel_create", {})
            embed = disnake.Embed(title=lang_data.get("title"), color=disnake.Color.blue())
            embed.set_thumbnail(url=entry.user.display_avatar.url if entry.user else None)
            embed.add_field(name=lang_data.get("user"), value=f"{entry.user.mention}\n{entry.user.display_name}",
                            inline=True)
            embed.add_field(name=lang_data.get("user_id"), value=f"{entry.user.id}", inline=True)
            embed.add_field(name=lang_data.get("roles"), value=", ".join(
                [role.mention for role in entry.user.roles if role.name != "@everyone"]) or lang_data.get("no_roles"),
                            inline=False)
            embed.add_field(name=lang_data.get("channel"), value=f"{channel.mention}\n{channel.name}", inline=True)
            embed.add_field(name=lang_data.get("channel_id"), value=f"{channel.id}", inline=True)

            await log_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(ChannelCreateCog(bot))
