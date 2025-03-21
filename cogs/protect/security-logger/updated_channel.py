import disnake
from disnake.ext import commands

from languages.logic.attribute import get_lang_data


class ChannelUpdateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: disnake.abc.GuildChannel, after: disnake.abc.GuildChannel):
        log_channel = after.guild.get_channel(1312804207186804810)
        if not log_channel:
            return

        audit_logs = [entry async for entry in
                      after.guild.audit_logs(limit=1, action=disnake.AuditLogAction.channel_update)]
        if not audit_logs:
            return

        entry = audit_logs[0]
        user = entry.user

        lang_data = get_lang_data()

        embed = disnake.Embed(title=lang_data.get("channel_update", "Изменение канала"), color=disnake.Color.blue())
        embed.set_thumbnail(url=user.display_avatar.url if user else None)
        embed.add_field(name=lang_data.get("user", "Пользователь"), value=f"{user.mention}\n{user.display_name}", inline=True)
        embed.add_field(name=lang_data.get("user_id", "ID пользователя"), value=f"{user.id}", inline=True)
        embed.add_field(name=lang_data.get("roles", "Роли пользователя"), value=", ".join([role.mention for role in user.roles if role.name != "@everyone"]) or lang_data.get("no_roles", "Нет ролей"), inline=False)
        embed.add_field(name=lang_data.get("channel", "Канал"), value=f"{after.mention}\n{after.name}", inline=True)
        embed.add_field(name=lang_data.get("channel_id", "ID канала"), value=f"{after.id}", inline=True)
        embed.add_field(name=lang_data.get("changes", "Изменения"), value=f"{before.name} → {after.name}" if before.name != after.name else lang_data.get("other_changes", "Другие изменения"), inline=False)
        await log_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(ChannelUpdateCog(bot))