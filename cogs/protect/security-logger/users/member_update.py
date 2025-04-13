import disnake
from disnake.ext import commands

from data.config import log_channel_id
from languages.logic.attribute import get_lang_data

class MemberUpdateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before: disnake.Member, after: disnake.Member):
        log_channel = after.guild.get_channel(log_channel_id)
        if not log_channel:
            return

        lang_data = get_lang_data().get("member_update", {})
        embed = disnake.Embed(title=lang_data.get("title"), color=disnake.Color.blue())
        changed = False

        embed.set_thumbnail(url=after.display_avatar.url)

        if before.nick != after.nick:
            changed = True
            embed.add_field(
                name=lang_data.get("nickname_changed"),
                value=f"{lang_data.get('was')}: `{before.nick}`\n{lang_data.get('now')}: `{after.nick}`",
                inline=False
            )


        if set(before.roles) != set(after.roles):
            changed = True
            before_roles = ", ".join(role.mention for role in before.roles if role.name != "@everyone") or lang_data.get("no_roles")
            after_roles = ", ".join(role.mention for role in after.roles if role.name != "@everyone") or lang_data.get("no_roles")
            embed.add_field(
                name=lang_data.get("roles_changed"),
                value=f"{lang_data.get('was')}: {before_roles}\n{lang_data.get('now')}: {after_roles}",
                inline=False
            )


        if not changed:
            return

        embed.add_field(
            name=lang_data.get("member"),
            value=f"{after.mention}\n{after.display_name}",
            inline=True
        )
        embed.add_field(
            name=lang_data.get("member_id"),
            value=str(after.id),
            inline=True
        )

        async for entry in after.guild.audit_logs(limit=1, action=disnake.AuditLogAction.member_update):
            if entry.user != self.bot.user:
                embed.add_field(
                    name=lang_data.get("user"),
                    value=f"{entry.user.mention}\n{entry.user.display_name}",
                    inline=True
                )
                embed.add_field(
                    name=lang_data.get("user_id"),
                    value=str(entry.user.id),
                    inline=True
                )
                embed.add_field(
                    name=lang_data.get("user_roles"),
                    value=", ".join(role.mention for role in entry.user.roles if role.name != "@everyone") or lang_data.get("no_roles"),
                    inline=False
                )
                break

        await log_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(MemberUpdateCog(bot))
