import json
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv("data/.env")

TOKEN: str = os.getenv("TOKEN")
if TOKEN is None:
    raise ValueError("Токен бота не найден в .env файле (переменная TOKEN)")

TRUST_ROLE_ID: Optional[int] = None
trust_role_id_str = os.getenv("TRUSTED_ROLE_ID")
if trust_role_id_str is not None:
    try:
        TRUST_ROLE_ID = int(trust_role_id_str)
    except ValueError:
        raise ValueError("TRUSTED_ROLE_ID должен быть числом")

LOG_CHANNEL_PATH = "data/log_channel.json"

def load_log_channel_id() -> Optional[int]:
    try:
        with open(LOG_CHANNEL_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return int(data.get("log_channel_id"))
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        return None

def save_log_channel_id(channel_id: int):
    os.makedirs(os.path.dirname(LOG_CHANNEL_PATH), exist_ok=True)
    with open(LOG_CHANNEL_PATH, "w", encoding="utf-8") as f:
        json.dump({"log_channel_id": channel_id}, f)

log_channel_id: Optional[int] = load_log_channel_id()

GLOBAL_LANG_FILE = "data/global_language.json"
