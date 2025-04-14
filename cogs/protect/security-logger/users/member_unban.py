import disnake
from disnake.ext import commands

from data.config import log_channel_id
from languages.logic.attribute import get_lang_data

class MemberUnbanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_unban(self, guild: disnake.Guild, user: disnake.User):
        log_channel = guild.get_channel(log_channel_id)
        if not log_channel:
            return

        async for entry in guild.audit_logs(limit=1, action=disnake.AuditLogAction.unban):
            if entry.user == self.bot.user:
                return

            lang_data = get_lang_data().get("member_unban", {})
            embed = disnake.Embed(title=lang_data.get("title"), color=disnake.Color.blue())

            try:
                moderator = await guild.fetch_member(entry.user.id)
                roles = ", ".join(
                    [role.mention for role in moderator.roles if role.name != "@everyone"]
                ) or lang_data.get("no_roles")
            except disnake.NotFound:
                moderator = entry.user
                roles = lang_data.get("no_roles")

            embed.set_thumbnail(url=moderator.display_avatar.url if moderator else None)
            embed.add_field(name=lang_data.get("user"), value=f"{moderator.mention}\n{moderator.display_name}",
                            inline=True)
            embed.add_field(name=lang_data.get("user_id"), value=str(moderator.id), inline=True)
            embed.add_field(name=lang_data.get("roles"), value=roles, inline=False)

            embed.add_field(name=lang_data.get("member"), value=f"{user.mention}\n{user.display_name}", inline=True)
            embed.add_field(name=lang_data.get("member_id"), value=str(user.id), inline=True)

            await log_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(MemberUnbanCog(bot))
