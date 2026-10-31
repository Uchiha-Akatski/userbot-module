# meta source: https://raw.githubusercontent.com/Uchiha-Akatski/userbot-module/refs/heads/main/WersUchihaAFK.py
# meta developer: @Itachi_Uchiha_sss, @Wers1xx
# meta banner: https://raw.githubusercontent.com/Uchiha-Akatski/itachi/main/photo_2026-10-28_18-02-31.jpg
# meta pic: https://raw.githubusercontent.com/Uchiha-Akatski/itachi/main/photo_2026-10-28_18-02-31.jpg

from .. import loader, utils

try:
    from telethon.tl import types, functions
except ImportError:
    from telethon import types, functions  

import time
import datetime
import logging
import os
import tempfile
import sys
import asyncio
import hashlib
import re
from collections import defaultdict

try:
    from zoneinfo import ZoneInfo
except ImportError:
    try:
        from pytz import timezone as _pytz_timezone
        ZoneInfo = None
    except ImportError:
        _pytz_timezone = None
        ZoneInfo = None

try:
    from telethon.tl.types import InputMediaWebPage
except ImportError:
    InputMediaWebPage = None

try:
    from telethon.tl.types import (
        KeyboardButtonUrl,
        ReplyInlineMarkup,
        KeyboardButtonRow,
        KeyboardButtonCallback,
    )
except ImportError:
    KeyboardButtonUrl = None
    ReplyInlineMarkup = None
    KeyboardButtonRow = None
    KeyboardButtonCallback = None

__version__ = (1, 21, 16)

name = "WersUchihaAFK"
logger = logging.getLogger(name)

UPDATE_RAW_URL = "https://raw.githubusercontent.com/Uchiha-Akatski/userbot-module/refs/heads/main/WersUchihaAFK.py"
UPDATE_RAW_URL_ALT = "https://raw.githubusercontent.com/Uchiha-Akatski/userbot-module/main/WersUchihaAFK.py"
UPDATE_API_COMMITS = "https://api.github.com/repos/Uchiha-Akatski/userbot-module/commits?path=WersUchihaAFK.py&per_page=1"
UPDATE_API_COMMITS_ALT = "https://api.github.com/repos/Uchiha-Akatski/userbot-module/commits?path=WersUchihaAFK.py&sha=main&per_page=1"
GITHUB_HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "WersUchihaAFK-Updater/1.21",
    "X-GitHub-Api-Version": "2022-11-28",
}


AFK_REPLY_PLACEHOLDERS = (
    "\n\nПлейсхолдеры:\n"
    "{user_id} {display_name} {was_online} {unit_name} {userbot_name}\n"
    "{reason_text} {come_time} — блоки с цитатой (старый формат)\n"
    "{reason_row} {come_row} — строки таблицы (Rich)"
)
SLEEP_REPLY_PLACEHOLDERS = (
    "\n\nПлейсхолдеры:\n"
    "{user_id} {display_name} {was_online} {unit_name} {userbot_name}\n"
    "{wake_time} — блок с цитатой (старый формат)\n"
    "{wake_row} — строка таблицы (Rich)"
)
OFF_PLACEHOLDERS = (
    "\n\nПлейсхолдеры:\n"
    "{user_id} {display_name} {unit_name} {userbot_name}\n"
    "{duration} — длительность (0:01:06)\n"
    "{log_text} — чистый список писавших (без обёртки)\n"
    "{log_block} — готовый блок <details> с таблицей логов"
)
WAKE_TIME_PLACEHOLDERS = (
    "\n\nЭтот текст подставляется в {wake_time} внутри MSG_SLEEP_REPLY.\n"
    "Используй {} как место для времени пробуждения, например:\n"
    "«Проснусь в: {}»"
)


@loader.tds
class WersUchihaAFKMod(loader.Module):
    """WersUchihaAFK — AFK/SLEEP с авто-аватаркой, тегами, Rich-логами и авто-обновлениями"""

    strings = {
        "name": "WersUchihaAFK",
        "back": (
            "<blockquote><emoji document_id=5883964170268840032>👤</emoji> <b><a href=\"tg://user?id={user_id}\">{display_name}</a> вернулся в строй!</b></blockquote>\n"
            "<blockquote><emoji document_id=5870729937215819584>⏰</emoji> <b>Был в AFK:</b> <code>{duration}</code></blockquote>\n"
            "{log_text}"
            "<blockquote><emoji document_id=5897663599819624992>🪐</emoji> <b>{unit_name}</b> | <i>Powered by {userbot_name}</i></blockquote>"
        ),
        "afk_on": (
            "<blockquote><emoji document_id=5870730156259152122>😀</emoji> <b>AFK включён!</b></blockquote>\n"
            "<blockquote><emoji document_id=5877700484453634587>✈️</emoji> WersUchihaAFK будет отвечать этим:</blockquote>"
        ),
        "default_afk_message": (
            "<blockquote><emoji document_id=5870948572526022116>✋</emoji> <b>Хозяин</b> <a href=\"tg://user?id={user_id}\">{display_name}</a> <b>вышел на связь</b></blockquote>\n"
            "<blockquote><emoji document_id=5870695289714643076>👤</emoji> <b>Абсенс:</b> <code>{was_online}</code> назад</blockquote>\n"
            "{reason_text}{come_time}"
            "<blockquote><emoji document_id=5897663599819624992>🪐</emoji> <b>{unit_name}</b> | <i>Powered by {userbot_name}</i></blockquote>\n"
            "<blockquote><emoji document_id=5469741319330996757>💫</emoji> <b>Статус:</b> <i>Премиум-режим активен</i> <emoji document_id=5431505596316665041>👑</emoji></blockquote>"
        ),
        "sleep_on": (
            "<blockquote><emoji document_id=5870729937215819584>💤</emoji> <b>SLEEP-режим включён!</b></blockquote>\n"
            "<blockquote><emoji document_id=5873146865637133757>😴</emoji> WersUchihaAFK будет отвечать этим:</blockquote>"
        ),
        "sleep_msg": (
            "<blockquote><emoji document_id=5870729937215819584>💤</emoji> <b>Хозяин</b> <a href=\"tg://user?id={user_id}\">{display_name}</a> <b>в спячке</b></blockquote>\n"
            "<blockquote><emoji document_id=5877700484453634587>🌙</emoji> <b>Не беспокоить, идёт техобслуживание</b></blockquote>\n"
            "<blockquote><emoji document_id=5870695289714643076>👤</emoji> <b>Сплю уже:</b> <code>{was_online}</code></blockquote>\n"
            "{wake_time}"
            "<blockquote><emoji document_id=5897663599819624992>🪐</emoji> <b>{unit_name}</b> | <i>Sleep Mode • {userbot_name}</i></blockquote>"
        ),
        "wake_text": "<blockquote><emoji document_id=5873146865637133757>🎤</emoji> <b>Проснусь через:</b> <code>{}</code></blockquote>\n",
        "sleep_off": (
            "<blockquote><emoji document_id=5883964170268840032>👤</emoji> <b><a href=\"tg://user?id={user_id}\">{display_name}</a> проснулся и готов к бою!</b></blockquote>\n"
            "<blockquote><emoji document_id=5870729937215819584>⏰</emoji> <b>Спал:</b> <code>{duration}</code></blockquote>\n"
            "{log_text}"
            "<blockquote><emoji document_id=5897663599819624992>🪐</emoji> <b>{unit_name}</b> | <i>Sleep Mode • {userbot_name}</i></blockquote>"
        ),
        "preset_saved": "<emoji document_id=5870730156259152122>✅</emoji> <b>Пресет '{}' сохранён!</b>",
        "preset_loaded": "<emoji document_id=5870730156259152122>✅</emoji> <b>Пресет '{}' загружен!</b>",
        "preset_deleted": "<emoji document_id=5870730156259152122>✅</emoji> <b>Пресет '{}' удалён!</b>",
        "preset_not_found": "<emoji document_id=5870730156259152122>❌</emoji> <b>Пресет '{}' не найден!</b>",
        "preset_pack_added": "<emoji document_id=5870730156259152122>✅</emoji> <b>Добавлено {} дефолтных пресетов!</b>",
        "presets_list": "<emoji document_id=5870730156259152122>📋</emoji> <b>Список пресетов:</b>\n\n",
        "cooldown_set": "<emoji document_id=5870730156259152122>⏰</emoji> <b>Кулдаун между AFK-ответами установлен на: {} секунд</b>",
        "cooldown_invalid": "<emoji document_id=5870730156259152122>❌</emoji> <b>Кулдаун должен быть целым числом и не менее 5 секунд!</b>",
        "no_reply": "<emoji document_id=5870730156259152122>❌</emoji> <b>Нужно ответить на медиа</b>",
        "no_media": "<emoji document_id=5870730156259152122>❌</emoji> <b>В ответе нет медиа</b>",
        "uploading": "<emoji document_id=5445355530111437729>📤</emoji> <b>Загружаю баннер...</b>",
        "added_afk": "<emoji document_id=5206607081334906820>✔️</emoji> <b>Баннер для AFK установлен!</b>",
        "added_sleep": "<emoji document_id=5206607081334906820>✔️</emoji> <b>Баннер для SLEEP установлен!</b>",
        "added_afk_off": "<emoji document_id=5206607081334906820>✔️</emoji> <b>Баннер для AFK OFF установлен!</b>",
        "added_sleep_off": "<emoji document_id=5206607081334906820>✔️</emoji> <b>Баннер для SLEEP OFF установлен!</b>",
        "failed": "<emoji document_id=5870730156259152122>❌</emoji> <b>Не удалось загрузить баннер</b>",
        "no_requests": "<emoji document_id=5870730156259152122>❌</emoji> <b>Установи requests: pip install requests</b>",
        "showing_afk": "<emoji document_id=5766879414704935108>🖼</emoji> <b>Текущий баннер AFK:</b>",
        "showing_sleep": "<emoji document_id=5766879414704935108>🖼</emoji> <b>Текущий баннер SLEEP:</b>",
        "showing_afk_off": "<emoji document_id=5766879414704935108>🖼</emoji> <b>Текущий баннер AFK OFF:</b>",
        "showing_sleep_off": "<emoji document_id=5766879414704935108>🖼</emoji> <b>Текущий баннер SLEEP OFF:</b>",
        "no_banner": "<emoji document_id=5352896944496728039>📭</emoji> <b>Баннер для этого типа не установлен</b>",
        "cleared_afk": "<emoji document_id=5255831443816327915>🗑</emoji> <b>Баннер AFK удалён</b>",
        "cleared_sleep": "<emoji document_id=5255831443816327915>🗑</emoji> <b>Баннер SLEEP удалён</b>",
        "cleared_afk_off": "<emoji document_id=5255831443816327915>🗑</emoji> <b>Баннер AFK OFF удалён</b>",
        "cleared_sleep_off": "<emoji document_id=5255831443816327915>🗑</emoji> <b>Баннер SLEEP OFF удалён</b>",
        "ignore_chats_list": "<emoji document_id=5199750217586459631>📄</emoji> <b>Игнорируемые чаты:</b>\n{}",
        "ignore_users_list": "<emoji document_id=5199750217586459631>📄</emoji> <b>Игнорируемые пользователи:</b>\n{}",
        "no_ignored_chats": "<emoji document_id=5352896944496728039>📭</emoji> <b>Нет игнорируемых чатов</b>",
        "no_ignored_users": "<emoji document_id=5352896944496728039>📭</emoji> <b>Нет игнорируемых пользователей</b>",
        "config_edit_hint": "\n\n<emoji document_id=5222108309795908493>✨</emoji> <b>Для изменения списка отредактируй конфиг модуля:</b>\n<code>.cfg WersUchihaAFK</code>",
        "avatar_set_afk": "<emoji document_id=5206607081334906820>✔️</emoji> <b>Аватарка AFK установлена!</b>",
        "avatar_set_sleep": "<emoji document_id=5206607081334906820>✔️</emoji> <b>Аватарка SLEEP установлена!</b>",
        "avatar_cleared_afk": "<emoji document_id=5255831443816327915>🗑</emoji> <b>Аватарка AFK удалена</b>",
        "avatar_cleared_sleep": "<emoji document_id=5255831443816327915>🗑</emoji> <b>Аватарка SLEEP удалена</b>",
        "avatar_failed": "<emoji document_id=5870730156259152122>❌</emoji> <b>Не удалось установить аватарку</b>",
        "update_available": (
            "<emoji document_id=5870730156259152122>🔄</emoji> <b>Вышла новая версия WersUchihaAFK!</b>\n\n"
            "<b>Текущая:</b> <code>{local}</code>\n"
            "<b>Новая:</b> <code>{remote}</code>\n\n"
            "<b>Коммит:</b>\n<code>{commit}</code>"
        ),
        "update_success": "<emoji document_id=5206607081334906820>✔️</emoji> <b>WersUchihaAFK успешно обновлён!</b>\nПерезагружаю модуль…",
        "update_failed": "<emoji document_id=5870730156259152122>❌</emoji> <b>Не удалось обновить модуль</b>",
        "update_ignored": "<emoji document_id=5255831443816327915>🗑</emoji> <b>Обновление проигнорировано</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue("setPremiumStatus", True, "Ставить премиум-статус при AFK/SLEEP.", validator=loader.validators.Boolean()),
            loader.ConfigValue("customEmojiStatus", 4969889971700761796, "Кастомный премиум-статус для AFK.", validator=loader.validators.Integer()),
            loader.ConfigValue("customSleepEmojiStatus", 5433709773532962414, "Кастомный премиум-статус для SLEEP.", validator=loader.validators.Integer()),
            loader.ConfigValue("TIMEZONE", "Europe/Moscow", "Часовой пояс для времени в логах. Пример: Europe/Berlin, Europe/Moscow, Asia/Tokyo."),
            loader.ConfigValue("MSG_AFK_REPLY", self.strings["default_afk_message"], "Текст ответа в AFK." + AFK_REPLY_PLACEHOLDERS),
            loader.ConfigValue("MSG_AFK_ON", self.strings["afk_on"], "Текст включения AFK."),
            loader.ConfigValue("AFK_MEDIA", "", "Ссылка на медиа для AFK."),
            loader.ConfigValue("AFK_OFF_MEDIA", "", "Ссылка на медиа для отключения AFK."),
            loader.ConfigValue("MSG_AFK_OFF", self.strings["back"], "Текст выхода из AFK." + OFF_PLACEHOLDERS),
            loader.ConfigValue("MSG_SLEEP_ON", self.strings["sleep_on"], "Текст включения SLEEP."),
            loader.ConfigValue("MSG_SLEEP_REPLY", self.strings["sleep_msg"], "Текст ответа в SLEEP." + SLEEP_REPLY_PLACEHOLDERS),
            loader.ConfigValue("SLEEP_MEDIA", "", "Ссылка на медиа для SLEEP."),
            loader.ConfigValue("SLEEP_OFF_MEDIA", "", "Ссылка на медиа для отключения SLEEP."),
            loader.ConfigValue("MSG_SLEEP_OFF", self.strings["sleep_off"], "Текст выхода из SLEEP." + OFF_PLACEHOLDERS),
            loader.ConfigValue("MSG_WAKE_TIME", self.strings["wake_text"], "Формат текста времени просыпания." + WAKE_TIME_PLACEHOLDERS),
            loader.ConfigValue("quote_media", False, "Switch preview media to quote", validator=loader.validators.Boolean()),
            loader.ConfigValue("invert_media", False, "Invert media (медиа сверху)", validator=loader.validators.Boolean()),
            loader.ConfigValue("cooldown_seconds", 60, "Кулдаун между AFK-ответами одному пользователю (секунд, минимум 5)", validator=loader.validators.Integer()),
            loader.ConfigValue("ignore_chats", [], "ID чатов для игнорирования.", validator=loader.validators.Series(validator=loader.validators.TelegramID())),
            loader.ConfigValue("ignore_users", [], "ID пользователей для игнорирования.", validator=loader.validators.Series(validator=loader.validators.TelegramID())),
            loader.ConfigValue("change_avatar", True, "Автоматически менять аватарку при AFK/SLEEP.", validator=loader.validators.Boolean()),
            loader.ConfigValue("AFK_AVATAR", "", "Ссылка на аватарку для AFK (jpg/png/webp)."),
            loader.ConfigValue("SLEEP_AVATAR", "", "Ссылка на аватарку для SLEEP (jpg/png/webp)."),
            loader.ConfigValue("change_nickname", True, "Добавлять тег в ник при AFK/SLEEP.", validator=loader.validators.Boolean()),
            loader.ConfigValue("afk_tag", "#WersAFK", "Тег, который добавляется в ник при AFK."),
            loader.ConfigValue("sleep_tag", "#ItachiSleep", "Тег, который добавляется в ник при SLEEP."),
            loader.ConfigValue("unit_name", "Unit Delta", "Название юнита в текстах."),
            loader.ConfigValue("auto_update", True, "Проверять обновления каждые 5 минут.", validator=loader.validators.Boolean()),
        )

        self.chat_messages = {}
        self._old_status = None
        self.afk_cooldowns = {}
        self.sleep_cooldowns = {}
        self._old_first_name = None
        self._old_photo_path = None
        self._update_notified_hash = None
        self._update_task = None

    CONFIG_KEYS_TO_SAVE = [
        "setPremiumStatus", "customEmojiStatus", "customSleepEmojiStatus",
        "TIMEZONE", "MSG_AFK_REPLY", "MSG_AFK_ON",
        "AFK_MEDIA", "AFK_OFF_MEDIA", "MSG_AFK_OFF",
        "MSG_SLEEP_ON", "MSG_SLEEP_REPLY",
        "SLEEP_MEDIA", "SLEEP_OFF_MEDIA", "MSG_SLEEP_OFF",
        "MSG_WAKE_TIME",
        "quote_media", "invert_media", "cooldown_seconds",
        "change_avatar", "AFK_AVATAR", "SLEEP_AVATAR",
        "change_nickname", "afk_tag", "sleep_tag",
        "unit_name", "auto_update",
    ]

    PRESET_PACK = {
        "anime": {
            "setPremiumStatus": True,
            "customEmojiStatus": 4969889971700761796,
            "customSleepEmojiStatus": 5433709773532962414,
            "MSG_AFK_REPLY": (
                "<blockquote><emoji document_id=5870948572526022116>✋</emoji> <b>Хозяин</b> <a href=\"tg://user?id={user_id}\">{display_name}</a> <b>ушёл в мир аниме</b></blockquote>\n"
                "<blockquote><emoji document_id=5870695289714643076>👤</emoji> <b>Нет в сети:</b> <code>{was_online}</code></blockquote>\n"
                "{reason_text}{come_time}"
                "<blockquote><emoji document_id=5870729937215819584>💤</emoji> <b>Вернётся когда закончится арка</b></blockquote>"
            ),
            "MSG_AFK_ON": "<blockquote>😀 AFK включён!</blockquote>\n<blockquote>✈️ WersUchihaAFK будет отвечать этим:</blockquote>",
            "AFK_MEDIA": "",
            "AFK_OFF_MEDIA": "",
            "MSG_AFK_OFF": "<emoji document_id=5883964170268840032>👤</emoji> <b><a href=\"tg://user?id={user_id}\">{display_name}</a> вернулся с новым билдом!</b>",
            "MSG_SLEEP_ON": "<emoji document_id=5870729937215819584>💤</emoji> <b>Ушёл смотреть сны...</b>",
            "MSG_SLEEP_REPLY": (
                "<blockquote><emoji document_id=5870729937215819584>💤</emoji> <b><a href=\"tg://user?id={user_id}\">{display_name}</a> спит</b></blockquote>\n"
                "<blockquote><emoji document_id=5870695289714643076>👤</emoji> <b>Сплю уже:</b> <code>{was_online}</code></blockquote>\n"
                "{wake_time}"
            ),
            "SLEEP_MEDIA": "",
            "SLEEP_OFF_MEDIA": "",
            "MSG_SLEEP_OFF": "<emoji document_id=5883964170268840032>👤</emoji> <b><a href=\"tg://user?id={user_id}\">{display_name}</a> проснулся после сладких снов!</b>",
            "MSG_WAKE_TIME": "<blockquote><emoji document_id=5873146865637133757>🎤</emoji> Проснусь через: <code>{}</code></blockquote>\n",
            "quote_media": True,
            "invert_media": True,
            "cooldown_seconds": 60,
            "change_avatar": True,
            "change_nickname": True,
            "afk_tag": "#WersAFK",
            "sleep_tag": "#ItachiSleep",
        },
        "strict": {
            "setPremiumStatus": True,
            "customEmojiStatus": 4969889971700761796,
            "customSleepEmojiStatus": 5433709773532962414,
            "MSG_AFK_REPLY": (
                "<blockquote><b>⚠️ ВНИМАНИЕ ⚠️</b></blockquote>\n"
                "<blockquote><b>Хозяин</b> <a href=\"tg://user?id={user_id}\">{display_name}</a> <b>ОТСУТСТВУЕТ</b></blockquote>\n"
                "<blockquote>⏰ Время отсутствия: <code>{was_online}</code></blockquote>\n"
                "{reason_text}{come_time}"
                "<blockquote><b>{unit_name} | Strict Mode</b></blockquote>"
            ),
            "MSG_AFK_ON": "<b>AFK ВКЛЮЧЕН.</b>",
            "AFK_MEDIA": "",
            "AFK_OFF_MEDIA": "",
            "MSG_AFK_OFF": "<b>✅ ХОЗЯИН ВЕРНУЛСЯ</b>",
            "MSG_SLEEP_ON": "<b>🌙 РЕЖИМ СНА АКТИВИРОВАН</b>",
            "MSG_SLEEP_REPLY": (
                "<blockquote><b>🔴 ХОЗЯИН НЕ ДОСТУПЕН</b></blockquote>\n"
                "<blockquote>Причина: <b>РЕЖИМ СНА</b></blockquote>\n"
                "<blockquote>Время сна: <code>{was_online}</code></blockquote>\n"
                "{wake_time}"
            ),
            "SLEEP_MEDIA": "",
            "SLEEP_OFF_MEDIA": "",
            "MSG_SLEEP_OFF": "<b>🟢 ХОЗЯИН ДОСТУПЕН</b>",
            "MSG_WAKE_TIME": "<b>⏰ Пробуждение в: <code>{}</code></b>\n",
            "quote_media": True,
            "invert_media": True,
            "cooldown_seconds": 30,
            "change_avatar": True,
            "change_nickname": True,
            "afk_tag": "#WersAFK",
            "sleep_tag": "#ItachiSleep",
        },
    }

    async def client_ready(self, client, db):
        self._db = db
        self._me = await client.get_me()
        self.client = client
        self.username = self._me.username or self._me.first_name
        self.afk_cooldowns = self._db.get(name, "afk_cooldowns", {})
        self.sleep_cooldowns = self._db.get(name, "sleep_cooldowns", {})

        saved_status = self._db.get(name, "old_status", None)
        if saved_status:
            try:
                if isinstance(saved_status, dict):
                    self._old_status = types.EmojiStatus(**saved_status)
                else:
                    self._old_status = saved_status
            except Exception as e:
                logger.error(f"Не удалось восстановить _old_status из БД: {e}")

        self._old_first_name = self._db.get(name, "old_first_name", None)
        self._old_photo_path = self._db.get(name, "old_photo_path", None)
        self._update_notified_hash = self._db.get(name, "update_notified_hash", None)

        saved_messages = self._db.get(name, "chat_messages", {})
        self.chat_messages = saved_messages if isinstance(saved_messages, dict) else {}

        try:
            if self.config["cooldown_seconds"] < 5:
                self.config["cooldown_seconds"] = 60
        except Exception:
            self.config["cooldown_seconds"] = 60



 

        self._detected_userbot = self._detect_userbot()

        if self._get_config_value("auto_update", True):
            self._update_task = asyncio.create_task(self._update_loop())

    def _detect_userbot(self) -> str:
        """
        Детектор юзербота (строгий, без ложных Heroku).
        Приоритет: Hikkari/Hikari → Heroku → Hikka → остальные.
        """
        try:
            import inspect
            import os as _os

            mod_names = [str(m).lower() for m in sys.modules.keys()]
            # только «релевантные» модули, не весь joined (иначе heroku/hikka ловятся мусором)
            interesting = [
                m for m in mod_names
                if any(
                    x in m
                    for x in (
                        "hikkari", "hikkaritl", "hikari", "heroku", "herokutl",
                        "hikka", "fox", "geek", "friendly", "loader", "userbot",
                    )
                )
            ]
            joined = " ".join(interesting)

            def exact_or_prefix(*needles: str) -> bool:
                for n in needles:
                    n = n.lower()
                    for m in mod_names:
                        if m == n or m.startswith(n + ".") or m.startswith(n + "_"):
                            return True
                return False

            def path_blob() -> str:
                chunks = []
                try:
                    from .. import loader as _ldr
                    chunks.append(inspect.getfile(_ldr) or "")
                except Exception:
                    pass
                try:
                    chunks.append(inspect.getfile(self.__class__) or "")
                except Exception:
                    pass
                try:
                    chunks.append(_os.getcwd() or "")
                except Exception:
                    pass
                for key in ("USERBOT", "USERBOT_NAME", "HIKKA", "HIKKARI", "HEROKU", "HOSTNAME"):
                    try:
                        chunks.append(_os.environ.get(key, "") or "")
                    except Exception:
                        pass
                return " ".join(chunks).lower()

            def brand_blob() -> str:
                parts = []
                try:
                    if hasattr(self, "inline") and self.inline is not None:
                        parts.append(str(getattr(self.inline, "bot_username", "") or ""))
                        # имя бота из кэша, если есть
                        for attr in ("bot_name", "_bot_name", "name"):
                            parts.append(str(getattr(self.inline, attr, "") or ""))
                        bot = getattr(self.inline, "bot", None)
                        if bot is not None:
                            parts.append(str(type(bot)))
                            # aiogram bot id / token prefix не трогаем
                            me = getattr(bot, "_me", None) or getattr(bot, "me", None)
                            if me is not None:
                                parts.append(str(getattr(me, "username", "") or ""))
                                parts.append(str(getattr(me, "full_name", "") or ""))
                                parts.append(str(getattr(me, "first_name", "") or ""))
                except Exception:
                    pass
                try:
                    parts.append(str(type(getattr(self, "client", None))))
                except Exception:
                    pass
                return " ".join(parts).lower()

            paths = path_blob()
            brand = brand_blob()
            all_txt = f"{joined} {paths} {brand}"

            # --- 1) Hikkari (бренд) / Hikari ---
            # Hikkari — отдельное имя (двойная k), не путать с Hikari
            if exact_or_prefix("hikkaritl", "hikkari") or any(
                x in all_txt for x in ("hikkaritl", "hikkari", "hikkari userbot")
            ):
                return "Hikkari Userbot"
            if re.search(r"(^|[\s/_.-])hikkari([\s/_.-]|$)", paths) or re.search(
                r"(^|[\s/_.-])hikkari([\s/_.-]|$)", brand
            ):
                return "Hikkari Userbot"

            if exact_or_prefix("hikari") or "hikari userbot" in all_txt:
                return "Hikari Userbot"
            if re.search(r"(^|[\s/_.-])hikari([\s/_.-]|$)", paths) or re.search(
                r"(^|[\s/_.-])hikari([\s/_.-]|$)", brand
            ):
                return "Hikari Userbot"

            # --- 2) Heroku (только явные маркеры, не любой 'heroku' в мусоре) ---
            if exact_or_prefix("herokutl", "heroku.client", "heroku.loader"):
                return "Heroku Userbot"
            if "herokutl" in all_txt or "heroku userbot" in all_txt:
                return "Heroku Userbot"
            if re.search(r"(^|[\s/_.-])heroku([\s/_.-]|$)", paths) and "hikkari" not in paths:
                return "Heroku Userbot"
            if re.search(r"(^|[\s/_.-])heroku([\s/_.-]|$)", brand):
                return "Heroku Userbot"

            # --- 3) Hikka ---
            # не ловить hikka внутри hikkaritl — hikari уже выше
            if exact_or_prefix("hikka"):
                # если в interesting только hikkaritl — already returned
                return "Hikka Userbot"
            if re.search(r"(^|[\s/_.-])hikka([\s/_.-]|$)", paths):
                return "Hikka Userbot"

            # --- 4) прочие ---
            if exact_or_prefix("foxuserbot") or "foxuserbot" in all_txt:
                return "Fox Userbot"
            if exact_or_prefix("geektg") or "geektg" in all_txt or "friendly-telegram" in all_txt:
                return "GeekTG Userbot"

            # --- 5) loader path final ---
            try:
                from .. import loader as _ldr
                p = (inspect.getfile(_ldr) or "").lower()
                if "hikkari" in p:
                    return "Hikkari Userbot"
                if "hikari" in p:
                    return "Hikari Userbot"
                if "heroku" in p:
                    return "Heroku Userbot"
                if "hikka" in p:
                    return "Hikka Userbot"
            except Exception:
                pass

            # --- 6) inline bot username ---
            try:
                if hasattr(self, "inline") and self.inline is not None:
                    bot_u = str(getattr(self.inline, "bot_username", "") or "").lower()
                    if "hikkari" in bot_u:
                        return "Hikkari Userbot"
                    if "hikari" in bot_u:
                        return "Hikari Userbot"
                    if "heroku" in bot_u:
                        return "Heroku Userbot"
                    if "hikka" in bot_u:
                        return "Hikka Userbot"
            except Exception:
                pass
        except Exception as e:
            logger.debug(f"detect userbot: {e}")
        return "Userbot"

    def _get_userbot_name(self) -> str:


        name_ub = getattr(self, "_detected_userbot", None) or ""
        if not str(name_ub).strip():
            name_ub = self._detect_userbot()
            self._detected_userbot = name_ub
        return str(name_ub).strip() or "Userbot"

    def _get_unit_name(self) -> str:
        return self._get_config_value("unit_name", "Unit Delta") or "Unit Delta"

    def _get_display_name(self) -> str:
        first = self._me.first_name or ""
        last = self._me.last_name or ""
        full = f"{first} {last}".strip() or self.username or "Хозяин"
        return utils.escape_html(full)

    def _get_username(self):
        return self._me.username or self._me.first_name or "Хозяин"

    def _get_config_value(self, key, default=None):
        try:
            return self.config.get(key, default)
        except Exception:
            return default

    def _tz(self):
        tz_name = (self._get_config_value("TIMEZONE", "") or "").strip()
        if not tz_name:
            return None
        try:
            if ZoneInfo is not None:
                return ZoneInfo(tz_name)
            if _pytz_timezone is not None:
                return _pytz_timezone(tz_name)
        except Exception as e:
            logger.warning(f"WersUchihaAFK: неверный TIMEZONE '{tz_name}': {e}")
        return None

    def _now(self) -> datetime.datetime:
        tz = self._tz()
        if tz is not None:
            return datetime.datetime.now(tz)
        return datetime.datetime.now()

    def _now_str(self) -> str:
        return self._now().strftime("%Y-%m-%d %H:%M:%S")                                        

    def _validate_cooldown_value(self, value):
        if not isinstance(value, int) or value < 5:
            raise ValueError(self.strings["cooldown_invalid"])
        return value

    def _safe_format(self, template: str, data: dict) -> str:
        data = dict(data or {})
        # гарантия ключевых полей
        data.setdefault("unit_name", self._get_unit_name())
        data.setdefault("userbot_name", self._get_userbot_name())
        data.setdefault("display_name", self._get_display_name() if hasattr(self, "_me") else "Хозяин")
        data.setdefault("user_id", getattr(getattr(self, "_me", None), "id", 0) or 0)
        for k in ("was_online", "duration", "reason_text", "come_time", "wake_time",
                  "reason_row", "come_row", "wake_row", "log_text", "log_block"):
            data.setdefault(k, "")
        try:
            return template.format(**data)
        except (KeyError, IndexError, ValueError):
            safe = defaultdict(str)
            safe.update(data)
            try:
                return template.format_map(safe)
            except Exception:
                return template

    def _save_old_status(self, status):
        self._old_status = status
        if status:
            if hasattr(status, "document_id"):
                self._db.set(name, "old_status", {"document_id": status.document_id})
            else:
                self._db.set(name, "old_status", status)
        else:
            self._db.set(name, "old_status", None)

    def _log_message(self, user):
        user_id = str(user.id)
        now_str = self._now_str()
        if user_id not in self.chat_messages:
            self.chat_messages[user_id] = {"name": "", "count": 0, "last_time": now_str}
        data = self.chat_messages[user_id]
        data["name"] = utils.escape_html(user.first_name or "Без имени")
        data["count"] += 1
        self._db.set(name, "chat_messages", self.chat_messages)
        last_users = self._db.get(name, "last_users", {})
        last_users[user_id] = {
            "id": user.id,
            "name": data["name"],
            "count": data["count"],
            "last_time": now_str,
        }
        self._db.set(name, "last_users", last_users)

    def _format_afk_log(self, mode: str = "afk"):
        """
        Каждый писавший — в своём blockquote.
        mode: "afk" | "sleep" — разный заголовок.
        """
        if not self.chat_messages:
            return ""
        sorted_items = sorted(
            self.chat_messages.items(),
            key=lambda kv: (kv[1].get("count", 0), kv[1].get("last_time", "")),
            reverse=True,
        )
        if mode == "sleep":
            title = "Пока ты спал, тебе писали:"
        else:
            title = "Пока тебя не было, тебе писали:"

        parts = [
            "\n<blockquote><emoji document_id=5260702125708557233>✋</emoji> "
            f"<b>{title}</b></blockquote>"
        ]
        for user_id, data in sorted_items:
            name = data.get("name") or "User"
            count = data.get("count", 0)
            last_time = data.get("last_time", "—")
            parts.append(
                "<blockquote>"
                f'<emoji document_id=5870695289714643076>👤</emoji> '
                f'<a href="tg://user?id={user_id}"><b>{name}</b></a> — '
                f'<b>{count}</b> сообщ.\n'
                f'<emoji document_id=5870729937215819584>⏰</emoji> '
                f'последнее: <code>{last_time}</code> · <code>{user_id}</code>'
                "</blockquote>"
            )
        return "\n".join(parts) + "\n"

    def _format_afk_log_rich(self, mode: str = "afk"):
        """Таблица для {log_block}, сортировка по count (убыв.)."""
        if not self.chat_messages:
            return ""

        sorted_items = sorted(
            self.chat_messages.items(),
            key=lambda kv: (kv[1].get("count", 0), kv[1].get("last_time", "")),
            reverse=True,
        )
        rows = []
        for user_id, data in sorted_items:
            name = data.get("name") or "User"
            count = data.get("count", 0)
            last_time = data.get("last_time", "—")
            rows.append(
                "<tr>"
                f"<td><a href=\"tg://user?id={user_id}\">{name}</a></td>"
                f"<td><code>{user_id}</code></td>"
                f"<td><b>{count}</b></td>"
                f"<td><code>{last_time}</code></td>"
                "</tr>"
            )

        title = (
            "Пока ты спал, тебе писали"
            if mode == "sleep"
            else "Пока тебя не было, тебе писали"
        )
        table_html = (
            "<table bordered striped compact>"
            "<tr>"
            "<th><tg-emoji emoji-id=5902335789798265487>👤</tg-emoji> Ник</th>"
            "<th><tg-emoji emoji-id=6021367625836140615>🪪</tg-emoji> ID</th>"
            "<th><tg-emoji emoji-id=5219688538106239995>✍️</tg-emoji> Сообщений</th>"
            "<th><tg-emoji emoji-id=5440621591387980068>🔜</tg-emoji> Последнее</th>"
            "</tr>"
            + "".join(rows)
            + "</table>"
        )
        return (
            f"<details><summary><tg-emoji emoji-id=5260702125708557233>✋</tg-emoji> {title}</summary>"
            f"{table_html}"
            f"</details>"
        )

    def _format_duration(self, seconds: int) -> str:
        return str(datetime.timedelta(seconds=max(0, int(seconds))))

    def _should_ignore_message(self, message):
        try:
            chat_id = utils.get_chat_id(message)
            if chat_id in self.config["ignore_chats"]:
                return True
            sender_id = getattr(message, "sender_id", None) or getattr(message, "from_id", None)
            if sender_id and sender_id in self.config["ignore_users"]:
                return True
        except Exception:
            pass
        return False

    # ====================== НИК + АВАТАР ======================

    async def _apply_nickname_tag(self, tag: str):
        if not self._get_config_value("change_nickname", True):
            return
        try:
            me = await self.client.get_me()
            current_first = me.first_name or ""
            if not self._old_first_name:
                self._old_first_name = current_first
                self._db.set(name, "old_first_name", current_first)
            clean = current_first
            for t in [self._get_config_value("afk_tag", "#WersAFK"), self._get_config_value("sleep_tag", "#ItachiSleep")]:
                if t and t in clean:
                    clean = clean.replace(t, "").strip()
            new_first = f"{clean} {tag}".strip()
            if len(new_first) > 64:
                new_first = new_first[:64]
            await self.client(functions.account.UpdateProfileRequest(first_name=new_first))
        except Exception as e:
            logger.error(f"Не удалось изменить ник: {e}")

    async def _restore_nickname(self):
        if not self._get_config_value("change_nickname", True):
            return
        try:
            if self._old_first_name is not None:
                await self.client(functions.account.UpdateProfileRequest(first_name=self._old_first_name))
                self._old_first_name = None
                self._db.set(name, "old_first_name", None)
        except Exception as e:
            logger.error(f"Не удалось восстановить ник: {e}")

    def _photo_to_input(self, photo):
        """Преобразует Photo в InputPhoto для DeletePhotosRequest"""
        try:
            return types.InputPhoto(
                id=photo.id,
                access_hash=photo.access_hash,
                file_reference=photo.file_reference,
            )
        except Exception:
            return None

    async def _download_and_set_avatar(self, media_url: str) -> bool:
        """
        Ставит AFK/SLEEP аватарку.
        Сохраняет id новой аватарки, чтобы потом УДАЛИТЬ её (а не просто перекрыть старой).
        """
        if not media_url or not media_url.strip():
            return False
        media_url = media_url.strip()
        tmp_path = None
        try:
            import requests
            resp = requests.get(media_url, timeout=25, stream=True)
            if resp.status_code != 200:
                return False
            content_type = resp.headers.get("content-type", "").lower()
            ext = "jpg"
            if "png" in content_type:
                ext = "png"
            elif "webp" in content_type:
                ext = "webp"
            elif "gif" in content_type:
                ext = "gif"
            tmp_path = os.path.join(tempfile.gettempdir(), f"afk_avatar_{int(time.time())}.{ext}")
            with open(tmp_path, "wb") as f:
                for chunk in resp.iter_content(8192):
                    f.write(chunk)
            if not os.path.exists(tmp_path) or os.path.getsize(tmp_path) == 0:
                return False

            # Запоминаем текущую верхнюю аватарку (на всякий случай — backup файлом)
            if not self._old_photo_path:
                try:
                    photos = await self.client.get_profile_photos("me", limit=1)
                    if photos:
                        old_tmp = os.path.join(tempfile.gettempdir(), f"old_avatar_{int(time.time())}.jpg")
                        await self.client.download_media(photos[0], file=old_tmp)
                        if os.path.exists(old_tmp) and os.path.getsize(old_tmp) > 0:
                            self._old_photo_path = old_tmp
                            self._db.set(name, "old_photo_path", old_tmp)
                except Exception as e:
                    logger.warning(f"Не удалось сохранить старую аватарку: {e}")

            # Запоминаем id текущей верхней фотки ДО загрузки (чтобы отличить новую)
            before_ids = set()
            try:
                before = await self.client.get_profile_photos("me", limit=5)
                before_ids = {p.id for p in before}
            except Exception:
                pass

            file = await self.client.upload_file(tmp_path)
            await self.client(functions.photos.UploadProfilePhotoRequest(file=file))

            # Находим id только что загруженной AFK/SLEEP аватарки
            try:
                after = await self.client.get_profile_photos("me", limit=5)
                for p in after:
                    if p.id not in before_ids:
                        # Это новая аватарка режима — сохраняем, чтобы потом удалить
                        self._db.set(name, "mode_photo_id", {
                            "id": p.id,
                            "access_hash": p.access_hash,
                            "file_reference": p.file_reference.hex() if isinstance(p.file_reference, (bytes, bytearray)) else str(p.file_reference),
                        })
                        break
                else:
                    # Fallback: берём самую верхнюю
                    if after:
                        p = after[0]
                        self._db.set(name, "mode_photo_id", {
                            "id": p.id,
                            "access_hash": p.access_hash,
                            "file_reference": p.file_reference.hex() if isinstance(p.file_reference, (bytes, bytearray)) else str(p.file_reference),
                        })
            except Exception as e:
                logger.warning(f"Не удалось запомнить id mode-аватарки: {e}")

            return True
        except Exception as e:
            logger.error(f"Ошибка установки аватарки: {e}")
            return False
        finally:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass

    async def _restore_avatar(self):
        """
        Удаляет ТОЛЬКО mode-аватарку, если она реально ставилась.
        Если AFK_AVATAR/SLEEP_AVATAR пустые — ничего не трогаем (свою аву не удаляем!).
        """
        if not self._get_config_value("change_avatar", True):
            return

        mode_data = self._db.get(name, "mode_photo_id", None)
        avatar_was_set = bool(self._db.get(name, "avatar_was_set", False))

        # Не ставили mode-аву — выходим, свою аватарку НЕ трогаем
        if not avatar_was_set and not (isinstance(mode_data, dict) and mode_data.get("id")):
            self._db.set(name, "mode_photo_id", None)
            self._db.set(name, "avatar_was_set", False)
            self._old_photo_path = None
            self._db.set(name, "old_photo_path", None)
            return

        deleted = False
        try:
            if mode_data and isinstance(mode_data, dict) and mode_data.get("id"):
                try:
                    fr = mode_data.get("file_reference", b"")
                    if isinstance(fr, str):
                        try:
                            fr = bytes.fromhex(fr)
                        except Exception:
                            fr = fr.encode("utf-8", errors="ignore")
                    if not isinstance(fr, (bytes, bytearray)):
                        fr = b""

                    input_photo = types.InputPhoto(
                        id=int(mode_data["id"]),
                        access_hash=int(mode_data["access_hash"]),
                        file_reference=fr,
                    )
                    await self.client(functions.photos.DeletePhotosRequest(id=[input_photo]))
                    deleted = True
                    logger.info("Mode-аватарка удалена по сохранённому id")
                except Exception as e:
                    logger.warning(f"Не удалось удалить mode-аватарку по id: {e}")

            # Fallback удаления верхней ТОЛЬКО если mode-ава точно ставилась
            if not deleted and avatar_was_set:
                try:
                    photos = await self.client.get_profile_photos("me", limit=1)
                    if photos:
                        inp = self._photo_to_input(photos[0])
                        if inp:
                            await self.client(functions.photos.DeletePhotosRequest(id=[inp]))
                            deleted = True
                            logger.info("Mode-аватарка удалена как верхняя")
                except Exception as e:
                    logger.warning(f"Fallback delete верхней аватарки: {e}")

            if not deleted and self._old_photo_path and os.path.exists(self._old_photo_path):
                try:
                    file = await self.client.upload_file(self._old_photo_path)
                    await self.client(functions.photos.UploadProfilePhotoRequest(file=file))
                    logger.info("Старая аватарка восстановлена загрузкой (fallback)")
                except Exception as e:
                    logger.error(f"Fallback upload старой аватарки: {e}")

        except Exception as e:
            logger.error(f"Не удалось восстановить аватарку: {e}")
        finally:
            self._db.set(name, "mode_photo_id", None)
            self._db.set(name, "avatar_was_set", False)
            if self._old_photo_path and os.path.exists(self._old_photo_path):
                try:
                    os.remove(self._old_photo_path)
                except Exception:
                    pass
            self._old_photo_path = None
            self._db.set(name, "old_photo_path", None)

    async def _set_mode_avatar(self, mode: str):
        """Ставит mode-аву ТОЛЬКО если в конфиге есть URL. Иначе — no-op."""
        if not self._get_config_value("change_avatar", True):
            return
        url = (self._get_config_value("AFK_AVATAR" if mode == "afk" else "SLEEP_AVATAR", "") or "").strip()
        if not url:
            # Явно сбрасываем флаги — чтобы restore ничего не удалял
            self._db.set(name, "avatar_was_set", False)
            self._db.set(name, "mode_photo_id", None)
            return
        ok = await self._download_and_set_avatar(url)
        self._db.set(name, "avatar_was_set", bool(ok))



    # ====================== АВТО-ОБНОВЛЕНИЯ ======================

    async def _update_loop(self):
        await asyncio.sleep(30)
        while True:
            try:
                if self._get_config_value("auto_update", True):
                    await self._check_for_updates()
            except Exception as e:
                logger.error(f"Update check error: {e}")
            await asyncio.sleep(300)

    def _parse_remote_version(self, content: str):
        m = re.search(r"__version__\s*=\s*\(([^)]+)\)", content)
        if not m:
            return None
        try:
            parts = [int(x.strip()) for x in m.group(1).split(",")]
            return tuple(parts)
        except Exception:
            return None

    def _http_get(self, url: str, headers: dict = None, timeout: int = 20):
        """
        Устойчивый GET: requests → urllib.
        GitHub без User-Agent часто отдаёт 403 — поэтому заголовки обязательны.
        """
        hdrs = {
            "User-Agent": "WersUchihaAFK-Updater/1.21",
            "Accept": "*/*",
        }
        if headers:
            hdrs.update(headers)

        # 1) requests
        try:
            import requests
            r = requests.get(url, timeout=timeout, headers=hdrs)
            return r.status_code, r.text, (r.content if r.content is not None else b"")
        except Exception as e:
            logger.debug(f"requests GET {url}: {e}")

        # 2) urllib
        try:
            import urllib.request
            req = urllib.request.Request(url, headers=hdrs)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
                code = getattr(resp, "status", 200) or 200
                try:
                    text = raw.decode("utf-8", errors="replace")
                except Exception:
                    text = str(raw)
                return code, text, raw
        except Exception as e:
            logger.debug(f"urllib GET {url}: {e}")

        return None, None, None

    def _extract_commit_from_api_json(self, data) -> str:
        try:
            if isinstance(data, list) and data:
                item = data[0]
            elif isinstance(data, dict):
                item = data
            else:
                return ""
            msg = (
                (item.get("commit") or {}).get("message")
                or item.get("message")
                or ""
            )
            msg = (msg or "").strip()
            if not msg:
                # sha как запасной идентификатор
                sha = item.get("sha") or (item.get("commit") or {}).get("tree", {}).get("sha")
                if sha:
                    return f"sha {str(sha)[:7]}"
            return msg
        except Exception:
            return ""

    def _fetch_commit_message(self) -> str:
        """Тянет текст последнего коммита несколькими способами."""
        urls = [UPDATE_API_COMMITS, UPDATE_API_COMMITS_ALT]
        for url in urls:
            try:
                code, body, _ = self._http_get(url, headers=GITHUB_HEADERS, timeout=15)
                if code != 200 or not body:
                    logger.debug(f"commits API {code} for {url}")
                    continue
                import json
                data = json.loads(body)
                msg = self._extract_commit_from_api_json(data)
                if msg:
                    msg = msg.split("\n")[0].strip()  # первая строка
                    if len(msg) > 200:
                        msg = msg[:200] + "…"
                    return msg
            except Exception as e:
                logger.debug(f"commit fetch {url}: {e}")

        # Fallback: коммит из комментария в самом файле (# meta / # commit)
        return ""

    def _fetch_module_source(self):
        for url in (UPDATE_RAW_URL, UPDATE_RAW_URL_ALT):
            try:
                code, body, raw = self._http_get(url, timeout=20)
                if code == 200 and body and "__version__" in body:
                    return body
            except Exception as e:
                logger.debug(f"raw fetch {url}: {e}")
        return None

    async def _fetch_remote(self):
        try:
            content = self._fetch_module_source()
            if not content:
                return None, None, None, None

            version = self._parse_remote_version(content)
            commit_msg = self._fetch_commit_message() or "—"

            # Если API молчит — попробуем вытащить из шапки файла
            if commit_msg == "—":
                m = re.search(r"#\s*meta\s+commit:\s*(.+)", content, re.I)
                if m:
                    commit_msg = m.group(1).strip()[:200]
                else:
                    m = re.search(r"#\s*commit:\s*(.+)", content, re.I)
                    if m:
                        commit_msg = m.group(1).strip()[:200]

            content_hash = hashlib.md5(content.encode("utf-8")).hexdigest()
            return version, content, commit_msg, content_hash
        except Exception as e:
            logger.error(f"Fetch remote error: {e}")
            return None, None, None, None

    async def _check_for_updates(self):
        result = await self._fetch_remote()
        if not result or result[0] is None:
            return
        remote_ver, content, commit_msg, content_hash = result
        local_ver = __version__

        if remote_ver <= local_ver:
            return

        if content_hash and content_hash == self._update_notified_hash:
            return

        self._update_notified_hash = content_hash
        self._db.set(name, "update_notified_hash", content_hash)

        text = self.strings["update_available"].format(
            local=".".join(map(str, local_ver)),
            remote=".".join(map(str, remote_ver)),
            commit=utils.escape_html(commit_msg),
        )

        buttons = self._build_update_buttons()
        await self._send_update_notify(text, buttons)

    def _build_aiogram_markup(self):
        """Клавиатура для aiogram-бота (Hikka / Hikari / Heroku)."""
        # aiogram 3.x
        try:
            from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
            return InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="🔄 Обновить", callback_data="wersafk_upd"),
                        InlineKeyboardButton(text="🗑 Игнорировать", callback_data="wersafk_ign"),
                    ]
                ]
            )
        except Exception as e:
            logger.debug(f"aiogram3 markup: {e}")
        # aiogram 2.x
        try:
            from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
            kb = InlineKeyboardMarkup(row_width=2)
            kb.add(
                InlineKeyboardButton("🔄 Обновить", callback_data="wersafk_upd"),
                InlineKeyboardButton("🗑 Игнорировать", callback_data="wersafk_ign"),
            )
            return kb
        except Exception as e:
            logger.debug(f"aiogram2 markup: {e}")
        return None

    def _build_telethon_buttons(self):
        """Кнопки для Telethon client."""
        try:
            try:
                from telethon import Button
            except ImportError:
                Button = None
            return [
                [
                    Button.inline("🔄 Обновить", b"wersafk_upd"),
                    Button.inline("🗑 Игнорировать", b"wersafk_ign"),
                ]
            ]
        except Exception as e:
            logger.debug(f"Button.inline: {e}")
        if KeyboardButtonCallback and ReplyInlineMarkup and KeyboardButtonRow:
            try:
                return ReplyInlineMarkup(
                    rows=[
                        KeyboardButtonRow(
                            buttons=[
                                KeyboardButtonCallback(text="🔄 Обновить", data=b"wersafk_upd"),
                                KeyboardButtonCallback(text="🗑 Игнорировать", data=b"wersafk_ign"),
                            ]
                        )
                    ]
                )
            except Exception:
                pass
        return None

    def _build_update_buttons(self):
        # legacy alias
        return self._build_telethon_buttons()

    async def _send_update_notify(self, text: str, buttons=None):
        """
        Уведомление об обновлении С кнопками.
        Hikka/Hikari бот = aiogram → reply_markup=InlineKeyboardMarkup.
        Telethon client → buttons=[[Button.inline...]].
        """
        chat_id = self._me.id
        aiogram_kb = self._build_aiogram_markup()
        tl_buttons = buttons or self._build_telethon_buttons()

        # --- 1) Инлайн-бот юзербота (aiogram) ---
        bot = None
        try:
            if hasattr(self, "inline") and self.inline:
                bot = getattr(self.inline, "bot", None)
        except Exception:
            bot = None

        if bot is not None:
            # aiogram reply_markup
            if aiogram_kb is not None:
                for kwargs in (
                    {"reply_markup": aiogram_kb, "disable_web_page_preview": True},
                    {"reply_markup": aiogram_kb, "link_preview": False},
                    {"reply_markup": aiogram_kb},
                ):
                    try:
                        await bot.send_message(chat_id, text, **kwargs)
                        logger.info("Update notify sent via aiogram bot + keyboard")
                        return
                    except TypeError:
                        continue
                    except Exception as e:
                        logger.warning(f"aiogram bot+kb failed: {e}")
                        break

            # telethon-style buttons on bot (на всякий)
            if tl_buttons is not None:
                for kwargs in (
                    {"buttons": tl_buttons, "link_preview": False},
                    {"reply_markup": tl_buttons, "link_preview": False},
                    {"buttons": tl_buttons},
                    {"reply_markup": tl_buttons},
                ):
                    try:
                        await bot.send_message(chat_id, text, **kwargs)
                        logger.info("Update notify sent via bot + telethon buttons")
                        return
                    except TypeError:
                        continue
                    except Exception as e:
                        logger.debug(f"bot telethon buttons: {e}")
                        break

            # бот без кнопок — НЕ return, попробуем client
            logger.warning("Bot available but keyboard attach failed, trying client")

        # --- 2) От аккаунта (Telethon buttons) ---
        if tl_buttons is not None:
            for send, cid in (
                (self.client.send_message, chat_id),
                (self.client.send_message, "me"),
            ):
                for kwargs in (
                    {"buttons": tl_buttons, "link_preview": False},
                    {"reply_markup": tl_buttons, "link_preview": False},
                    {"buttons": tl_buttons},
                ):
                    try:
                        await send(cid, text, **kwargs)
                        logger.info("Update notify sent via client + buttons")
                        return
                    except TypeError:
                        continue
                    except Exception as e:
                        logger.debug(f"client buttons {cid}: {e}")
                        break

        # --- 3) Текст без кнопок (последний шанс) ---
        try:
            if bot is not None:
                await bot.send_message(chat_id, text)
                return
        except Exception:
            pass
        try:
            await self.client.send_message("me", text)
        except Exception as e:
            logger.error(f"Fallback notify failed: {e}")

    async def _install_update(self):
        try:
            import requests
            r = requests.get(UPDATE_RAW_URL, timeout=30)
            if r.status_code != 200:
                return False
            content = r.text

            module_path = None
            try:
                import inspect
                module_path = inspect.getfile(self.__class__)
            except Exception:
                pass

            if not module_path or not os.path.exists(module_path):
                candidates = [
                    f"/data/data/com.termux/files/home/hikka/modules/{name}.py",
                    f"/root/hikka/modules/{name}.py",
                    os.path.expanduser(f"~/hikka/modules/{name}.py"),
                ]
                for c in candidates:
                    if os.path.exists(c):
                        module_path = c
                        break

            if not module_path:
                try:
                    import inspect
                    module_path = inspect.getfile(self.__class__)
                except Exception:
                    return False

            with open(module_path, "w", encoding="utf-8") as f:
                f.write(content)

            try:
                if hasattr(self, "allmodules") and self.allmodules:
                    await self.allmodules.reload_module(name)
                elif hasattr(self, "lookup"):
                    pass
            except Exception as e:
                logger.warning(f"Reload after update: {e}")

            return True
        except Exception as e:
            logger.error(f"Install update error: {e}")
            return False

    # ====================== CALLBACKS ======================

    @loader.callback_handler()
    async def update_callback_handler(self, call):
        try:
            data = getattr(call, "data", None)
            if data is None and hasattr(call, "data"):
                data = call.data
            if isinstance(data, bytes):
                data = data.decode("utf-8", errors="ignore")
            data = (data or "").strip()

            async def _answer(msg: str):
                try:
                    await call.answer(msg)
                except Exception:
                    try:
                        # aiogram
                        await call.answer(text=msg, show_alert=False)
                    except Exception:
                        pass

            async def _edit(msg: str):
                try:
                    await call.edit(msg)
                    return
                except Exception:
                    pass
                try:
                    await call.message.edit_text(msg)
                except Exception:
                    try:
                        if hasattr(call, "edit_message_text"):
                            await call.edit_message_text(msg)
                    except Exception:
                        pass

            async def _delete():
                try:
                    await call.delete()
                    return
                except Exception:
                    pass
                try:
                    await call.message.delete()
                except Exception:
                    pass

            if data == "wersafk_upd":
                await _answer("Обновляю…")
                ok = await self._install_update()
                await _edit(self.strings["update_success"] if ok else self.strings["update_failed"])
                return

            if data == "wersafk_ign":
                await _answer("Игнорирую")
                try:
                    await _delete()
                except Exception:
                    await _edit(self.strings["update_ignored"])
                return
        except Exception as e:
            logger.error(f"Callback error: {e}")


    # ====================== КОМАНДЫ ======================

    @loader.command(
        ru_doc="— Показать список игнорируемых чатов",
        en_doc="— Show ignored chats list",
        alias="ignchats",
    )
    async def ignorechats(self, message):
        ignore_chats = self._get_config_value("ignore_chats", [])
        if not ignore_chats:
            await utils.answer(message, self.strings["no_ignored_chats"])
            return
        lines = [f"  <emoji document_id=5870695289714643076>👤</emoji> <code>{chat_id}</code>" for chat_id in ignore_chats]
        await utils.answer(message, self.strings["ignore_chats_list"].format("\n".join(lines)) + self.strings["config_edit_hint"])

    @loader.command(
        ru_doc="— Показать список игнорируемых пользователей",
        en_doc="— Show ignored users list",
        alias="ignusers",
    )
    async def ignoreusers(self, message):
        ignore_users = self._get_config_value("ignore_users", [])
        if not ignore_users:
            await utils.answer(message, self.strings["no_ignored_users"])
            return
        lines = [f"  <emoji document_id=5870695289714643076>👤</emoji> <code>{user_id}</code>" for user_id in ignore_users]
        await utils.answer(message, self.strings["ignore_users_list"].format("\n".join(lines)) + self.strings["config_edit_hint"])

    # ====================== ХЕЛПЕР ДЛЯ RICH ======================

    async def _send_rich(self, m, html: str, title: str = "Status") -> bool:
        """Отправляет Rich отдельным сообщением и удаляет только команду."""
        try:
            await utils.answer(m, html, rich=True)
            return True
        except Exception as e:
            logger.warning(f"WersUchihaAFK: utils.answer(rich=True) failed: {e}")    


        # 2. Фоллбек — utils.answer с rich=True
        try:
            await utils.answer(m, html)
            return True
        except Exception as e:
            logger.warning(f"WersUchihaAFK: utils.answer(html) failed: {e}")

        return False            

    @loader.command(
        ru_doc="[причина] | [время] — Включить AFK режим",
        en_doc="[reason] | [time] — Enable AFK mode",
        alias="a",
    )
    async def afk(self, message):
        args = utils.get_args_raw(message)
        reason = None
        time_val = None
        if args:
            if "|" in args:
                reason, time_val = map(str.strip, args.split("|", 1))
            else:
                reason = args.strip()
        if self._get_config_value("setPremiumStatus", True):
            try:
                me = await self.client.get_me()
                if me.emoji_status:
                    self._save_old_status(me.emoji_status)
                await self.client(
                    functions.account.UpdateEmojiStatusRequest(
                        emoji_status=types.EmojiStatus(
                            document_id=self._get_config_value("customEmojiStatus", 4969889971700761796)
                        )
                    )
                )
            except Exception as e:
                logger.error(f"Не удалось обновить статус: {e}")

        await self._apply_nickname_tag(self._get_config_value("afk_tag", "#WersAFK"))
        await self._set_mode_avatar("afk")

        self._db.set(name, "afk", reason or True)
        self._db.set(name, "gone", time.time())
        self._db.set(name, "return_time", time_val)

        self.chat_messages = {}
        self._db.set(name, "chat_messages", {})
        self._db.set(name, "last_users", {})
        self.afk_cooldowns = {}
        self._db.set(name, "afk_cooldowns", self.afk_cooldowns)

        display_name = self._get_display_name()
        user_id = self._me.id

        reason_text = (
            f"<blockquote><emoji document_id=5870729937215819584>⏰️</emoji> "
            f"<b>Причина:</b> {utils.escape_html(reason)}</blockquote>\n"
            if reason else ""
        )
        come_time_text = (
            f"<blockquote><emoji document_id=5873146865637133757>🎤</emoji> "
            f"<b>Прийду через:</b> {utils.escape_html(time_val)}</blockquote>\n"
            if time_val else ""
        )
        reason_row = (
            f"<tr><td><tg-emoji emoji-id=5287752276415368705>❓</tg-emoji> Причина</td><td>{utils.escape_html(reason)}</td></tr>"
            if reason else ""
        )
        come_row = (
            f"<tr><td><tg-emoji emoji-id=5408866986908201757>🎤</tg-emoji> Прийду через</td><td>{utils.escape_html(time_val)}</td></tr>"
            if time_val else ""
        )

        preview = self._safe_format(
            self._get_config_value("MSG_AFK_REPLY", self.strings["default_afk_message"]),
            {
                "was_online": "Только что",
                "display_name": display_name,
                "user_id": user_id,
                "reason_text": reason_text,
                "come_time": come_time_text,
                "reason_row": reason_row,
                "come_row": come_row,
                "unit_name": self._get_unit_name(),
                "userbot_name": self._get_userbot_name(),
            },
        )
        
        on_text = self._safe_format(self._get_config_value("MSG_AFK_ON", self.strings["afk_on"]), {})
        full_text = on_text + "\n" + preview

        media_url = self._get_config_value("AFK_MEDIA", "")
        # Если есть баннер — всегда через _send_command_response (rich-only его пропускает)
        if media_url:
            await self._send_command_response(message, full_text, media_url)
        elif not await self._send_rich(message, full_text, title="AFK Включен"):
            await self._send_command_response(message, full_text, None)

    @loader.command(
        ru_doc="Выключить AFK режим",
        en_doc="Disable AFK mode",
        alias="back",
    )
    async def unafk(self, message):
        gone = self._db.get(name, "gone")
        duration_value = self._format_duration(time.time() - gone) if gone else ""

        self._db.set(name, "afk", False)
        self._db.set(name, "gone", None)
        self._db.set(name, "return_time", None)
        self.afk_cooldowns = {}
        self._db.set(name, "afk_cooldowns", self.afk_cooldowns)

        log_text = self._format_afk_log()
        log_block = self._format_afk_log_rich()

        if self._get_config_value("setPremiumStatus", True) and self._old_status:
            try:
                await self.client(
                    functions.account.UpdateEmojiStatusRequest(emoji_status=self._old_status)
                )
            except Exception as e:
                logger.error(f"Не удалось восстановить статус: {e}")
        self._save_old_status(None)

        await self._restore_nickname()
        await self._restore_avatar()

        display_name = self._get_display_name()
        user_id = self._me.id

        template = self._get_config_value("MSG_AFK_OFF", self.strings["back"])
        full_text = self._safe_format(
            template,
            {
                "display_name": display_name,
                "user_id": user_id,
                "duration": duration_value or "0:00:00",
                "log_text": log_text if "{log_text}" in template else "",
                "log_block": log_block,
                "unit_name": self._get_unit_name(),
                "userbot_name": self._get_userbot_name(),
            },
        )

        # Дописываем только если в шаблоне нет плейсхолдеров — и всегда в blockquote
        if duration_value and "{duration}" not in template:
            full_text += (
                f"\n<blockquote><emoji document_id=5870729937215819584>⏰</emoji> "
                f"<b>Был в AFK:</b> <code>{duration_value}</code></blockquote>"
            )
        if log_text and "{log_text}" not in template and "{log_block}" not in template:
            full_text += log_text

        media_url = self._get_config_value("AFK_OFF_MEDIA", "")
        if media_url:
            await self._send_command_response(message, full_text, media_url)
        elif not await self._send_rich(message, full_text, title="AFK Выключен"):
            await self._send_command_response(message, full_text, None)

        self.chat_messages = {}
        self._db.set(name, "chat_messages", {})
        self._db.set(name, "last_users", {})

    @loader.command(
        ru_doc="[время] — Включить SLEEP режим",
        en_doc="[time] — Enable SLEEP mode",
        alias="gn",
    )
    async def sleep(self, message):
        args = utils.get_args_raw(message)
        wake_time = args if args else None
        if self._get_config_value("setPremiumStatus", True):
            try:
                me = await self.client.get_me()
                if me.emoji_status:
                    self._save_old_status(me.emoji_status)
                await self.client(
                    functions.account.UpdateEmojiStatusRequest(
                        emoji_status=types.EmojiStatus(
                            document_id=self._get_config_value("customSleepEmojiStatus", 5433709773532962414)
                        )
                    )
                )
            except Exception as e:
                logger.error(f"Не удалось обновить статус: {e}")

        await self._apply_nickname_tag(self._get_config_value("sleep_tag", "#ItachiSleep"))
        await self._set_mode_avatar("sleep")

        self._db.set(name, "sleep", True)
        self._db.set(name, "sleep_start", time.time())
        self._db.set(name, "wake_time", wake_time)

        self.chat_messages = {}
        self._db.set(name, "chat_messages", {})
        self._db.set(name, "last_users", {})
        self.sleep_cooldowns = {}
        self._db.set(name, "sleep_cooldowns", self.sleep_cooldowns)

        display_name = self._get_display_name()
        user_id = self._me.id

        wake_text_old = (
            self._get_config_value("MSG_WAKE_TIME", self.strings["wake_text"]).format(utils.escape_html(wake_time))
            if wake_time else ""
        )
        wake_row = (
            f"<tr><td><tg-emoji emoji-id=5408866986908201757>🎤</tg-emoji> Проснусь в</td><td><code>{utils.escape_html(wake_time)}</code></td></tr>"
            if wake_time else ""
        )

        preview = self._safe_format(
            self._get_config_value("MSG_SLEEP_REPLY", self.strings["sleep_msg"]),
            {
                "was_online": "Только что",
                "display_name": display_name,
                "user_id": user_id,
                "wake_time": wake_text_old,
                "wake_row": wake_row,
                "unit_name": self._get_unit_name(),
                "userbot_name": self._get_userbot_name(),
            },
        )
        
        on_text = self._safe_format(self._get_config_value("MSG_SLEEP_ON", self.strings["sleep_on"]), {})
        full_text = on_text + "\n" + preview

        media_url = self._get_config_value("SLEEP_MEDIA", "")
        if media_url:
            await self._send_command_response(message, full_text, media_url)
        elif not await self._send_rich(message, full_text, title="SLEEP Включен"):
            await self._send_command_response(message, full_text, None)

    @loader.command(
        ru_doc="Выключить SLEEP режим",
        en_doc="Disable SLEEP mode",
        alias="wake",
    )
    async def unsleep(self, message):
        sleep_start = self._db.get(name, "sleep_start")
        duration_value = self._format_duration(time.time() - sleep_start) if sleep_start else ""

        self._db.set(name, "sleep", False)
        self._db.set(name, "sleep_start", None)
        self._db.set(name, "wake_time", None)
        self.sleep_cooldowns = {}
        self._db.set(name, "sleep_cooldowns", self.sleep_cooldowns)

        log_text = self._format_afk_log("sleep")
        log_block = self._format_afk_log_rich("sleep")

        if self._get_config_value("setPremiumStatus", True) and self._old_status:
            try:
                await self.client(
                    functions.account.UpdateEmojiStatusRequest(emoji_status=self._old_status)
                )
            except Exception as e:
                logger.error(f"Не удалось восстановить статус: {e}")
        self._save_old_status(None)

        await self._restore_nickname()
        await self._restore_avatar()

        display_name = self._get_display_name()
        user_id = self._me.id

        template = self._get_config_value("MSG_SLEEP_OFF", self.strings["sleep_off"])
        full_text = self._safe_format(
            template,
            {
                "display_name": display_name,
                "user_id": user_id,
                "duration": duration_value or "0:00:00",
                "log_text": log_text if "{log_text}" in template else "",
                "log_block": log_block,
                "unit_name": self._get_unit_name(),
                "userbot_name": self._get_userbot_name(),
            },
        )

        if duration_value and "{duration}" not in template:
            full_text += (
                f"\n<blockquote><emoji document_id=5870729937215819584>⏰</emoji> "
                f"<b>Спал:</b> <code>{duration_value}</code></blockquote>"
            )
        if log_text and "{log_text}" not in template and "{log_block}" not in template:
            full_text += log_text

        media_url = self._get_config_value("SLEEP_OFF_MEDIA", "")
        if media_url:
            await self._send_command_response(message, full_text, media_url)
        elif not await self._send_rich(message, full_text, title="SLEEP Выключен"):
            await self._send_command_response(message, full_text, None)

        self.chat_messages = {}
        self._db.set(name, "chat_messages", {})
        self._db.set(name, "last_users", {})

    @loader.command(
        ru_doc="<секунды> — Установить кулдаун (минимум 5 сек)",
        en_doc="<seconds> — Set cooldown (min 5 sec)",
        alias="afkcd",
    )
    async def afkcooldown(self, message):
        args = utils.get_args_raw(message)
        try:
            new_cooldown = int(args)
            self._validate_cooldown_value(new_cooldown)
            self.config["cooldown_seconds"] = new_cooldown
            await utils.answer(message, self.strings["cooldown_set"].format(new_cooldown))
        except ValueError:
            await utils.answer(message, self.strings["cooldown_invalid"])

    @loader.command(ru_doc="Ответь на медиа — баннер AFK", alias="addafk")
    async def add_afk_banner(self, message):
        await self._add_banner(message, "afk")

    @loader.command(ru_doc="Ответь на медиа — баннер SLEEP", alias="addsleep")
    async def add_sleep_banner(self, message):
        await self._add_banner(message, "sleep")

    @loader.command(ru_doc="Ответь на медиа — баннер AFK OFF", alias="addafkoff")
    async def add_afkoff_banner(self, message):
        await self._add_banner(message, "afk_off")

    @loader.command(ru_doc="Ответь на медиа — баннер SLEEP OFF", alias="addsleepoff")
    async def add_sleepoff_banner(self, message):
        await self._add_banner(message, "sleep_off")

    @loader.command(ru_doc="Ответь на медиа — аватарка AFK", alias="addafkav")
    async def add_afk_avatar(self, message):
        await self._add_avatar(message, "afk")

    @loader.command(ru_doc="Ответь на медиа — аватарка SLEEP", alias="addsleepav")
    async def add_sleep_avatar(self, message):
        await self._add_avatar(message, "sleep")

    @loader.command(ru_doc="Удалить аватарку AFK", alias="delafkav")
    async def del_afk_avatar(self, message):
        self.config["AFK_AVATAR"] = ""
        await utils.answer(message, self.strings["avatar_cleared_afk"])

    @loader.command(ru_doc="Удалить аватарку SLEEP", alias="delsleepav")
    async def del_sleep_avatar(self, message):
        self.config["SLEEP_AVATAR"] = ""
        await utils.answer(message, self.strings["avatar_cleared_sleep"])

    @loader.command(ru_doc="Показать баннер AFK", alias="showafk")
    async def show_afk_banner(self, message):
        await self._show_banner(message, "afk")

    @loader.command(ru_doc="Показать баннер SLEEP", alias="showsleep")
    async def show_sleep_banner(self, message):
        await self._show_banner(message, "sleep")

    @loader.command(ru_doc="Показать баннер AFK OFF", alias="showafkoff")
    async def show_afkoff_banner(self, message):
        await self._show_banner(message, "afk_off")

    @loader.command(ru_doc="Показать баннер SLEEP OFF", alias="showsleepoff")
    async def show_sleepoff_banner(self, message):
        await self._show_banner(message, "sleep_off")

    @loader.command(ru_doc="Удалить баннер AFK", alias="delafk")
    async def del_afk_banner(self, message):
        self.config["AFK_MEDIA"] = ""
        self._db.set(name, "afk_banner_url", "")
        await utils.answer(message, self.strings["cleared_afk"])

    @loader.command(ru_doc="Удалить баннер SLEEP", alias="delsleep")
    async def del_sleep_banner(self, message):
        self.config["SLEEP_MEDIA"] = ""
        self._db.set(name, "sleep_banner_url", "")
        await utils.answer(message, self.strings["cleared_sleep"])

    @loader.command(ru_doc="Удалить баннер AFK OFF", alias="delafkoff")
    async def del_afkoff_banner(self, message):
        self.config["AFK_OFF_MEDIA"] = ""
        self._db.set(name, "afk_off_banner_url", "")
        await utils.answer(message, self.strings["cleared_afk_off"])

    @loader.command(ru_doc="Удалить баннер SLEEP OFF", alias="delsleepoff")
    async def del_sleepoff_banner(self, message):
        self.config["SLEEP_OFF_MEDIA"] = ""
        self._db.set(name, "sleep_off_banner_url", "")
        await utils.answer(message, self.strings["cleared_sleep_off"])

    @loader.command(
        ru_doc="[save/load/del/list/pack] [название] — Пресеты",
        en_doc="[save/load/del/list/pack] [name] — Presets",
        alias="preset",
    )
    async def afkpreset(self, message):
        args = utils.get_args_raw(message).split(maxsplit=1)
        if not args or not args[0]:
            await utils.answer(message, "<emoji document_id=5465665476971471368>❌</emoji> <b>Укажи аргументы!</b>\n<code>.afkpreset save/load/del/list/pack</code>")
            return

        action = args[0].lower()
        name_preset = args[1] if len(args) > 1 else None
        presets = self._db.get(name, "presets", {})

        if action == "save":
            if not name_preset:
                await utils.answer(message, "Укажите название пресета!")
                return
            current_preset_data = {key: self.config[key] for key in self.CONFIG_KEYS_TO_SAVE if key in self.config}
            presets[name_preset] = current_preset_data
            self._db.set(name, "presets", presets)
            await utils.answer(message, self.strings["preset_saved"].format(name_preset))

        elif action == "load":
            if not name_preset:
                await utils.answer(message, "Укажите название пресета!")
                return
            if name_preset not in presets:
                await utils.answer(message, self.strings["preset_not_found"].format(name_preset))
                return
            preset_data = presets[name_preset]
            loaded_keys, missing_keys = [], []
            for key, value in preset_data.items():
                if key in self.config:
                    self.config[key] = value
                    loaded_keys.append(key)
                else:
                    missing_keys.append(key)
            result_msg = self.strings["preset_loaded"].format(name_preset)
            if loaded_keys:
                result_msg += f"\n\n✅ <b>Загружено:</b> {', '.join(loaded_keys)}"
            if missing_keys:
                result_msg += f"\n\n⚠️ <b>Не загружены:</b> {', '.join(missing_keys)}"
            await utils.answer(message, result_msg)

        elif action == "del":
            if not name_preset:
                await utils.answer(message, "Укажите название пресета!")
                return
            if name_preset not in presets:
                await utils.answer(message, self.strings["preset_not_found"].format(name_preset))
                return
            del presets[name_preset]
            self._db.set(name, "presets", presets)
            await utils.answer(message, self.strings["preset_deleted"].format(name_preset))

        elif action == "pack":
            count = 0
            for pk_name, pk_data in self.PRESET_PACK.items():
                if pk_name not in presets:
                    presets[pk_name] = pk_data
                    count += 1
            if count > 0:
                self._db.set(name, "presets", presets)
            await utils.answer(message, self.strings["preset_pack_added"].format(count))

        elif action == "list":
            if not presets:
                await utils.answer(message, "Пресеты отсутствуют.")
                return
            res = self.strings["presets_list"]
            for p in presets:
                res += f"  <emoji document_id=5870695289714643076>👤</emoji> <code>{p}</code>\n"
            await utils.answer(message, res)
        else:
            await utils.answer(message, "Доступные: save, load, del, list, pack")

    # ====================== ВСПОМОГАТЕЛЬНЫЕ ======================

    async def _prepare_media(self, media_url: str):
        media_url = (media_url or "").strip()
        if not media_url or media_url.lower() in {"", "none", "null", "false"}:
            return None
        if self._get_config_value("quote_media", False) and InputMediaWebPage is not None:
            try:
                return InputMediaWebPage(url=media_url, optional=True)
            except Exception:
                pass
        return media_url

    async def _send_with_invert(self, message, text: str, media_url: str = None, reply_to=None, force_invert=False):
        """
        Одна отправка: текст + медиа.
        Цепочка 🔄 сохранена (для quote/invert).
        Без дублей — fallback только если основная отправка реально упала.
        """
        media = await self._prepare_media(media_url)
        is_rich = any(tag in (text or "") for tag in ("<table", "<details", "<figure", "<h2", "<h3"))
        should_invert = not force_invert and self._get_config_value("invert_media", False)

        # --- только текст ---
        if media is None:
            kwargs = {}
            if reply_to:
                kwargs["reply_to"] = reply_to
            if is_rich:
                try:
                    await utils.answer(message, text, rich=True, **kwargs)
                    return
                except Exception as e:
                    logger.debug(f"rich text-only: {e}")
            await utils.answer(message, text, **kwargs)
            return

        # --- 🔄 цепочка ---
        try:
            if reply_to:
                temp_msg = await self.client.send_message(message.chat_id, "🔄", reply_to=reply_to)
            else:
                temp_msg = await utils.answer(message, "🔄")
        except Exception as e:
            logger.warning(f"🔄 failed: {e}")
            temp_msg = message

        async def _one_shot(target, invert: bool) -> bool:
            """True только если отправка прошла без исключения."""
            kwargs = {"file": media}
            if invert:
                kwargs["invert_media"] = True
            if is_rich:
                try:
                    await utils.answer(target, text, rich=True, **kwargs)
                    return True
                except TypeError:
                    pass
                except Exception as e:
                    logger.debug(f"rich+file: {e}")
            try:
                await utils.answer(target, text, **kwargs)
                return True
            except TypeError:
                kwargs.pop("invert_media", None)
                try:
                    await utils.answer(target, text, **kwargs)
                    return True
                except Exception as e:
                    logger.warning(f"answer retry: {e}")
                    return False
            except Exception as e:
                logger.warning(f"answer+file: {e}")
                return False

        if await _one_shot(temp_msg, should_invert):
            return
        if should_invert and await _one_shot(temp_msg, False):
            return

        # Fallback ОДИН раз: новое сообщение, 🔄 удаляем
        try:
            chat_id = utils.get_chat_id(message)
            await self.client.send_message(
                chat_id,
                text,
                file=media,
                reply_to=reply_to,
                link_preview=bool(self._get_config_value("quote_media", False)),
            )
            if temp_msg is not message:
                try:
                    await temp_msg.delete()
                except Exception:
                    pass
            else:
                try:
                    await message.delete()
                except Exception:
                    pass
        except Exception as e:
            logger.error(f"fallback media send: {e}")
            try:
                await utils.answer(temp_msg, text)
            except Exception:
                pass

    async def _send_response(self, message, text: str, media_url: str = None):
        await self._send_with_invert(message, text, media_url, reply_to=message.id)

    async def _send_command_response(self, message, text: str, media_url: str = None):
        await self._send_with_invert(message, text, media_url, reply_to=None)

    def _check_cooldown(self, cooldown_dict, user_id, mode="afk"):
        cooldown_seconds = self._get_config_value("cooldown_seconds", 60)
        last_reply_time = cooldown_dict.get(user_id, 0)
        current_time = time.time()
        if current_time - last_reply_time >= cooldown_seconds:
            return True, current_time
        return False, None

    def _update_cooldown(self, cooldown_dict, user_id, current_time):
        cooldown_dict[user_id] = current_time
        return cooldown_dict

    async def _upload_media(self, file_path: str, ext: str):
        try:
            import requests
            with open(file_path, "rb") as f:
                resp = requests.post("https://x0.at/", files={"file": (f"banner.{ext}", f)}, timeout=30)
            if resp.status_code == 200 and resp.text.strip().startswith("http"):
                return resp.text.strip()
        except Exception as e:
            logger.error(f"Upload error: {e}")
        return None

    async def _add_banner(self, message, banner_type: str):
        try:
            import requests
        except ImportError:
            await utils.answer(message, self.strings["no_requests"])
            return
        replied = await message.get_reply_message()
        if not replied:
            await utils.answer(message, self.strings["no_reply"])
            return
        has_media = False
        media_type = "jpg"
        if getattr(replied, "photo", None):
            has_media = True
        elif getattr(replied, "video", None):
            has_media = True
            media_type = "mp4"
        elif getattr(replied, "document", None):
            has_media = True
            mime = getattr(replied.document, "mime_type", "") or ""
            if "gif" in mime.lower():
                media_type = "gif"
            elif "video" in mime.lower():
                media_type = "mp4"
        if not has_media and getattr(replied, "media", None):
            has_media = True
        if not has_media:
            await utils.answer(message, self.strings["no_media"])
            return
        status = await utils.answer(message, self.strings["uploading"])
        tmp_path = None
        try:
            tmp_path = os.path.join(tempfile.gettempdir(), f"banner_{message.id}.{media_type}")
            await self.client.download_media(replied, file=tmp_path)
            if not os.path.exists(tmp_path) or os.path.getsize(tmp_path) == 0:
                await status.edit(self.strings["failed"])
                return
            url = await self._upload_media(tmp_path, media_type)
            if not url:
                await status.edit(self.strings["failed"])
                return
            key_map = {
                "afk": ("AFK_MEDIA", "afk_banner_url", "added_afk"),
                "sleep": ("SLEEP_MEDIA", "sleep_banner_url", "added_sleep"),
                "afk_off": ("AFK_OFF_MEDIA", "afk_off_banner_url", "added_afk_off"),
                "sleep_off": ("SLEEP_OFF_MEDIA", "sleep_off_banner_url", "added_sleep_off"),
            }
            conf_key, db_key, str_key = key_map[banner_type]
            self.config[conf_key] = url
            self._db.set(name, db_key, url)
            await status.edit(self.strings[str_key])
        except Exception as e:
            logger.error(f"Error: {e}")
            await status.edit(self.strings["failed"])
        finally:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass

    async def _add_avatar(self, message, avatar_type: str):
        try:
            import requests
        except ImportError:
            await utils.answer(message, self.strings["no_requests"])
            return
        replied = await message.get_reply_message()
        if not replied:
            await utils.answer(message, self.strings["no_reply"])
            return
        has_media = bool(getattr(replied, "photo", None) or getattr(replied, "document", None) or getattr(replied, "media", None))
        if not has_media:
            await utils.answer(message, self.strings["no_media"])
            return
        status = await utils.answer(message, self.strings["uploading"])
        tmp_path = None
        try:
            tmp_path = os.path.join(tempfile.gettempdir(), f"avatar_{message.id}.jpg")
            await self.client.download_media(replied, file=tmp_path)
            if not os.path.exists(tmp_path) or os.path.getsize(tmp_path) == 0:
                await status.edit(self.strings["avatar_failed"])
                return
            url = await self._upload_media(tmp_path, "jpg")
            if not url:
                await status.edit(self.strings["avatar_failed"])
                return
            if avatar_type == "afk":
                self.config["AFK_AVATAR"] = url
                await status.edit(self.strings["avatar_set_afk"])
            else:
                self.config["SLEEP_AVATAR"] = url
                await status.edit(self.strings["avatar_set_sleep"])
        except Exception as e:
            logger.error(f"Avatar set error: {e}")
            await status.edit(self.strings["avatar_failed"])
        finally:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass

    async def _show_banner(self, message, banner_type: str):
        mapping = {
            "afk": ("AFK_MEDIA", "showing_afk"),
            "sleep": ("SLEEP_MEDIA", "showing_sleep"),
            "afk_off": ("AFK_OFF_MEDIA", "showing_afk_off"),
            "sleep_off": ("SLEEP_OFF_MEDIA", "showing_sleep_off"),
        }
        conf_key, str_key = mapping[banner_type]
        url = self._get_config_value(conf_key, "")
        text = self.strings[str_key]
        if not url:
            await utils.answer(message, self.strings["no_banner"])
            return
        media = await self._prepare_media(url)
        if media:
            await self._send_with_invert(message, text, media_url=url, reply_to=None, force_invert=True)
        else:
            await utils.answer(message, f"{text}\n\n<code>{url}</code>")

    # ====================== WATCHER AFK ======================

    async def watcher(self, message):
        if not isinstance(message, types.Message):
            return

        is_ignored = self._should_ignore_message(message)

        if not (message.mentioned or getattr(message.to_id, "user_id", None) == self._me.id):
            return

        afk_state = self._db.get(name, "afk", False)
        sleep_state = self._db.get(name, "sleep", False)
        if not afk_state and not sleep_state:
            return

        try:
            user = await self.client.get_entity(message.sender_id)
        except Exception:
            return

        if user.is_self or user.bot:
            return

        self._log_message(user)

        if is_ignored:
            return

        if sleep_state:
            can_reply, current_time = self._check_cooldown(self.sleep_cooldowns, user.id, "sleep")
            if not can_reply:
                return
        else:
            can_reply, current_time = self._check_cooldown(self.afk_cooldowns, user.id, "afk")
            if not can_reply:
                return

        display_name = self._get_display_name()
        user_id = self._me.id

        if sleep_state:
            sleep_start = self._db.get(name, "sleep_start")
            diff_seconds = int(time.time() - sleep_start) if sleep_start else 0
            if diff_seconds < 0:
                diff_seconds = 0
            was_online = str(datetime.timedelta(seconds=diff_seconds))
            wake_time = self._db.get(name, "wake_time")
            wake_text_old = (
                self._get_config_value("MSG_WAKE_TIME", self.strings["wake_text"]).format(utils.escape_html(wake_time))
                if wake_time else ""
            )
            wake_row = (
                f"<tr><td><tg-emoji emoji-id=5408866986908201757>🎤</tg-emoji> Проснусь в</td><td><code>{utils.escape_html(wake_time)}</code></td></tr>"
                if wake_time else ""
            )
            text = self._safe_format(
                self._get_config_value("MSG_SLEEP_REPLY", self.strings["sleep_msg"]),
                {
                    "was_online": was_online,
                    "display_name": display_name,
                    "user_id": user_id,
                    "wake_time": wake_text_old,
                    "wake_row": wake_row,
                    "unit_name": self._get_unit_name(),
                    "userbot_name": self._get_userbot_name(),
                },
            )
            media_url = self._get_config_value("SLEEP_MEDIA", "")
            self.sleep_cooldowns = self._update_cooldown(self.sleep_cooldowns, user.id, current_time)
            self._db.set(name, "sleep_cooldowns", self.sleep_cooldowns)
        else:
            gone = self._db.get(name, "gone")
            diff_seconds = int(time.time() - gone) if gone else 0
            if diff_seconds < 0:
                diff_seconds = 0
            was_online = str(datetime.timedelta(seconds=diff_seconds))
            reason = afk_state if isinstance(afk_state, str) else None
            return_time = self._db.get(name, "return_time")

            reason_text = (
                f"<blockquote><emoji document_id=5870729937215819584>⏰️</emoji> "
                f"<b>Причина:</b> {utils.escape_html(reason)}</blockquote>\n"
                if reason else ""
            )
            come_time_text = (
                f"<blockquote><emoji document_id=5873146865637133757>🎤</emoji> "
                f"<b>Прийду через:</b> {utils.escape_html(return_time)}</blockquote>\n"
                if return_time else ""
            )
            reason_row = (
                f"<tr><td><tg-emoji emoji-id=5287752276415368705>❓</tg-emoji> Причина</td><td>{utils.escape_html(reason)}</td></tr>"
                if reason else ""
            )
            come_row = (
                f"<tr><td><tg-emoji emoji-id=5408866986908201757>🎤</tg-emoji> Прийду через</td><td>{utils.escape_html(return_time)}</td></tr>"
                if return_time else ""
            )

            text = self._safe_format(
                self._get_config_value("MSG_AFK_REPLY", self.strings["default_afk_message"]),
                {
                    "was_online": was_online,
                    "display_name": display_name,
                    "user_id": user_id,
                    "reason_text": reason_text,
                    "come_time": come_time_text,
                    "reason_row": reason_row,
                    "come_row": come_row,
                    "unit_name": self._get_unit_name(),
                    "userbot_name": self._get_userbot_name(),
                },
            )
            media_url = self._get_config_value("AFK_MEDIA", "")
            self.afk_cooldowns = self._update_cooldown(self.afk_cooldowns, user.id, current_time)
            self._db.set(name, "afk_cooldowns", self.afk_cooldowns)

        await self._send_response(message, text, media_url)

    async def on_unload(self):
        if self._update_task and not self._update_task.done():
            self._update_task.cancel()