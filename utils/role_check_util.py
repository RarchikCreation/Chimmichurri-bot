import disnake
from disnake import ApplicationCommandInteraction
from data.config import TRUST_ROLE_ID
from languages.logic.attribute import get_lang_data

def has_trust_role(member: disnake.Member) -> bool:
    return any(role.id == TRUST_ROLE_ID for role in member.roles)

async def check_trust_access(inter: ApplicationCommandInteraction) -> bool:
    lang_data = get_lang_data().get("access", {})
    if not has_trust_role(inter.author):
        await inter.response.send_message(lang_data.get("desc"), ephemeral=True)
        return False
    return True
