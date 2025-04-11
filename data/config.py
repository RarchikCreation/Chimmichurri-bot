import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv("data/.env")

# Обязательная переменная (токен бота)
TOKEN: str = os.getenv("TOKEN")
if TOKEN is None:
    raise ValueError("Токен бота не найден в .env файле (переменная TOKEN)")

# Опциональная переменная (ID доверенной роли)
TRUST_ROLE_ID: Optional[int] = None
trust_role_id_str = os.getenv("TRUSTED_ROLE_ID")  # Лучше использовать подчёркивание вместо дефиса
if trust_role_id_str is not None:
    try:
        TRUST_ROLE_ID = int(trust_role_id_str)
    except ValueError:
        raise ValueError("TRUSTED_ROLE_ID должен быть числом (например: 1234567890)")