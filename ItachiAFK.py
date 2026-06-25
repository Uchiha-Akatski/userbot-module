# meta developer: @Itachi_Uchiha_sss, @Wers1xx

from .. import loader, utils
from telethon import types, functions
import time
import datetime
import logging
from collections import defaultdict

try:
    from herokutl.types import InputMediaWebPage
except ImportError:
    InputMediaWebPage = None

__version__ = (1, 13, 1)

name = "ItachiAFK"
logger = logging.getLogger(name)


@loader.tds
class ItachiAFKMod(loader.Module):
    """AFK/SLEEP модуль с логированием, кликабельными никами, кулдауном и баннерами"""

    strings = {
        "name": "ItachiAFK",
        "back": "<emoji document_id=5883964170268840032>👤</emoji> <b>@{username} вернулся в строй!</b>",
        "afk_on": (
            "<blockquote><emoji document_id=5870730156259152122>😀</emoji> AFK включён!</blockquote>\n\n"
            "<blockquote><emoji document_id=5877700484453634587>✈️</emoji> ItachiAFK будет отвечать этим:</blockquote>"
        ),
        "default_afk_message": (
            "<blockquote><emoji document_id=5870948572526022116>✋</emoji> <b>Хозяин</b> <i>@{username}</i> <b>вышел на связь</b></blockquote>\n\n"
            "<blockquote><emoji document_id=5870695289714643076>👤</emoji> <b>Абсенс:</b> <code>{was_online}</code> назад</blockquote>\n\n"
            "{reason_text}{come_time}\n\n"
            "<blockquote><emoji document_id=5897663599819624992>🪐</emoji> <b>Unit Alpha Heroku</b> | <i>Powered by Heroku Userbot</i></blockquote>\n\n"
            "<blockquote><emoji document_id=5469741319330996757>💫</emoji> <b>Статус:</b> <i>Премиум-режим активен</i> <emoji document_id=5431505596316665041>👑</emoji></blockquote>"
        ),
        "sleep_on": (
            "<blockquote><emoji document_id=5870729937215819584>💤</emoji> SLEEP-режим включён!</blockquote>\n\n"
            "<blockquote><emoji document_id=5873146865637133757>😴</emoji> ItachiAFK будет отвечать этим:</blockquote>"
        ),
        "sleep_msg": (
            "<blockquote><emoji document_id=5870729937215819584>💤</emoji> <b>Хозяин</b> <i>@{username}</i> <b>в спячке</b></blockquote>\n\n"
            "<blockquote><emoji document_id=5877700484453634587>🌙</emoji> <b>Не беспокоить, идёт техобслуживание</b></blockquote>\n\n"
            "<blockquote><emoji document_id=5870695289714643076>👤</emoji> <b>Сплю уже:</b> <code>{was_online}</code></blockquote>\n\n"
            "{wake_time}\n\n"
            "<blockquote><emoji document_id=5897663599819624992>🪐</emoji> <b>Unit Alpha Heroku</b> | <i>Sleep Mode Activated</i></blockquote>"
        ),
        "wake_text": "\n\n<blockquote><emoji document_id=5873146865637133757>🎤</emoji> <b>Проснусь через:</b> <code>{}</code></blockquote>",
        "sleep_off": "<emoji document_id=5883964170268840032>👤</emoji> <b>@{username} проснулся и готов к бою!</b>",
        "preset_saved": "<emoji document_id=5870730156259152122>✅</emoji> <b>Пресет '{}' сохранён!</b>",
        "preset_loaded": "<emoji document_id=5870730156259152122>✅</emoji> <b>Пресет '{}' загружен!</b>",
        "preset_deleted": "<emoji document_id=5870730156259152122>✅</emoji> <b>Пресет '{}' удалён!</b>",
        "preset_not_found": "<emoji document_id=5870730156259152122>❌</emoji> <b>Пресет '{}' не найден!</b>",
        "preset_pack_added": "<emoji document_id=5870730156259152122>✅</emoji> <b>Добавлено {} дефолтных пресетов!</b>",
        "presets_list": "<emoji document_id=5870730156259152122>📋</emoji> <b>Список пресетов:</b>\n\n",
        "cooldown_set": "<emoji document_id=5870730156259152122>⏰</emoji> <b>Кулдаун между AFK-ответами установлен на: {} секунд</b>",
        "cooldown_invalid": "<emoji document_id=5870730156259152122>❌</emoji> <b>Кулдаун должен быть целым числом и не менее 5 секунд!</b>",
        # Баннер команды
        "no_reply": "❌ <b>Нужно ответить на медиа</b>",
        "no_media": "❌ <b>В ответе нет медиа</b>",
        "uploading": "📤 <b>Загружаю баннер...</b>",
        "added_afk": "✅ <b>Баннер для AFK установлен!</b>",
        "added_sleep": "✅ <b>Баннер для SLEEP установлен!</b>",
        "added_afk_off": "✅ <b>Баннер для AFK OFF установлен!</b>",
        "added_sleep_off": "✅ <b>Баннер для SLEEP OFF установлен!</b>",
        "failed": "❌ <b>Не удалось загрузить баннер</b>",
        "no_requests": "❌ <b>Установи requests: pip install requests</b>",
        "showing_afk": "🖼️ <b>Текущий баннер AFK:</b>",
        "showing_sleep": "🖼️ <b>Текущий баннер SLEEP:</b>",
        "showing_afk_off": "🖼️ <b>Текущий баннер AFK OFF:</b>",
        "showing_sleep_off": "🖼️ <b>Текущий баннер SLEEP OFF:</b>",
        "no_banner": "📭 <b>Баннер для этого типа не установлен</b>",
        "cleared_afk": "🗑️ <b>Баннер AFK удалён</b>",
        "cleared_sleep": "🗑️ <b>Баннер SLEEP удалён</b>",
        "cleared_afk_off": "🗑️ <b>Баннер AFK OFF удалён</b>",
        "cleared_sleep_off": "🗑️ <b>Баннер SLEEP OFF удалён</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue("setPremiumStatus", True, "Ставить премиум-статус при AFK/SLEEP.", validator=loader.validators.Boolean()),
            loader.ConfigValue("customEmojiStatus", 4969889971700761796, "Кастомный премиум-статус для AFK.", validator=loader.validators.Integer()),
            loader.ConfigValue("customSleepEmojiStatus", 5433709773532962414, "Кастомный премиум-статус для SLEEP.", validator=loader.validators.Integer()),
            loader.ConfigValue("MSG_AFK_REPLY", self.strings["default_afk_message"], "Текст ответа в AFK."),
            loader.ConfigValue("MSG_AFK_ON", self.strings["afk_on"], "Текст включения AFK."),
            loader.ConfigValue("AFK_MEDIA", "", "Ссылка на медиа для AFK."),
            loader.ConfigValue("AFK_OFF_MEDIA", "", "Ссылка на медиа для отключения AFK."),
            loader.ConfigValue("MSG_AFK_OFF", self.strings["back"], "Текст выхода из AFK."),
            loader.ConfigValue("MSG_SLEEP_ON", self.strings["sleep_on"], "Текст включения SLEEP."),
            loader.ConfigValue("MSG_SLEEP_REPLY", self.strings["sleep_msg"], "Текст ответа в SLEEP."),
            loader.ConfigValue("SLEEP_MEDIA", "", "Ссылка на медиа для SLEEP."),
            loader.ConfigValue("SLEEP_OFF_MEDIA", "", "Ссылка на медиа для отключения SLEEP."),
            loader.ConfigValue("MSG_SLEEP_OFF", self.strings["sleep_off"], "Текст выхода из SLEEP."),
            loader.ConfigValue("MSG_WAKE_TIME", self.strings["wake_text"], "Формат текста времени просыпания."),
            loader.ConfigValue("quote_media", False, "Switch preview media to quote", validator=loader.validators.Boolean()),
            loader.ConfigValue("invert_media", False, "Invert media (медиа сверху)", validator=loader.validators.Boolean()),
            loader.ConfigValue("cooldown_seconds", 60, "Кулдаун между AFK-ответами одному пользователю (секунд, минимум 5)", validator=loader.validators.Integer()),
        )

        self.chat_messages = defaultdict(lambda: {"name": "", "count": 0})
        self._old_status = None
        
        # Инициализация словарей для кулдаунов
        self.afk_cooldowns = {}
        self.sleep_cooldowns = {}

    CONFIG_KEYS_TO_SAVE = [
        "setPremiumStatus", "customEmojiStatus", "customSleepEmojiStatus", 
        "MSG_AFK_REPLY", "MSG_AFK_ON",
        "AFK_MEDIA", "AFK_OFF_MEDIA", "MSG_AFK_OFF", 
        "MSG_SLEEP_ON", "MSG_SLEEP_REPLY",
        "SLEEP_MEDIA", "SLEEP_OFF_MEDIA", "MSG_SLEEP_OFF", 
        "MSG_WAKE_TIME",
        "quote_media", "invert_media", "cooldown_seconds",
    ]

    PRESET_PACK = {
        "anime": {
            "setPremiumStatus": True,
            "customEmojiStatus": 4969889971700761796,
            "customSleepEmojiStatus": 5433709773532962414,
            "MSG_AFK_REPLY": (
                "<blockquote><emoji document_id=5870948572526022116>✋</emoji> <b>Хозяин</b> <i>@{username}</i> <b>ушёл в мир аниме</b></blockquote>\n\n"
                "<blockquote><emoji document_id=5870695289714643076>👤</emoji> <b>Нет в сети:</b> <code>{was_online}</code></blockquote>\n\n"
                "{reason_text}{come_time}\n\n"
                "<blockquote><emoji document_id=5870729937215819584>💤</emoji> <b>Вернётся когда закончится арка</b></blockquote>"
            ),
            "MSG_AFK_ON": "<blockquote>😀 AFK включён!</blockquote>\n\n<blockquote>✈️ ItachiAFK будет отвечать этим:</blockquote>",
            "AFK_MEDIA": "",
            "AFK_OFF_MEDIA": "",
            "MSG_AFK_OFF": "<emoji document_id=5883964170268840032>👤</emoji> <b>@{username} вернулся с новым билдом!</b>",
            "MSG_SLEEP_ON": "<emoji document_id=5870729937215819584>💤</emoji> <b>Ушёл смотреть сны...</b>",
            "MSG_SLEEP_REPLY": (
                "<blockquote><emoji document_id=5870729937215819584>💤</emoji> <b>@{username} спит</b></blockquote>\n\n"
                "<blockquote><emoji document_id=5870695289714643076>👤</emoji> <b>Сплю уже:</b> <code>{was_online}</code></blockquote>\n\n"
                "{wake_time}"
            ),
            "SLEEP_MEDIA": "",
            "SLEEP_OFF_MEDIA": "",
            "MSG_SLEEP_OFF": "<emoji document_id=5883964170268840032>👤</emoji> <b>@{username} проснулся после сладких снов!</b>",
            "MSG_WAKE_TIME": "<emoji document_id=5873146865637133757>🎤</emoji> Проснусь через: <code>{}</code>",
            "quote_media": True,
            "invert_media": True,
            "cooldown_seconds": 60,
        },
        "strict": {
            "setPremiumStatus": True,
            "customEmojiStatus": 4969889971700761796,
            "customSleepEmojiStatus": 5433709773532962414,
            "MSG_AFK_REPLY": (
                "<blockquote><b>⚠️ ВНИМАНИЕ ⚠️</b></blockquote>\n\n"
                "<blockquote><b>Хозяин</b> <i>@{username}</i> <b>ОТСУТСТВУЕТ</b></blockquote>\n\n"
                "<blockquote>⏰ Время отсутствия: <code>{was_online}</code></blockquote>\n\n"
                "{reason_text}{come_time}\n\n"
                "<blockquote><b>Unit Alpha Heroku | Strict Mode</b></blockquote>"
            ),
            "MSG_AFK_ON": "<b>AFK ВКЛЮЧЕН.</b>",
            "AFK_MEDIA": "",
            "AFK_OFF_MEDIA": "",
            "MSG_AFK_OFF": "<b>✅ ХОЗЯИН ВЕРНУЛСЯ</b>",
            "MSG_SLEEP_ON": "<b>🌙 РЕЖИМ СНА АКТИВИРОВАН</b>",
            "MSG_SLEEP_REPLY": (
                "<blockquote><b>🔴 ХОЗЯИН НЕ ДОСТУПЕН</b></blockquote>\n\n"
                "<blockquote>Причина: <b>РЕЖИМ СНА</b></blockquote>\n\n"
                "<blockquote>Время сна: <code>{was_online}</code></blockquote>\n\n"
                "{wake_time}"
            ),
            "SLEEP_MEDIA": "",
            "SLEEP_OFF_MEDIA": "",
            "MSG_SLEEP_OFF": "<b>🟢 ХОЗЯИН ДОСТУПЕН</b>",
            "MSG_WAKE_TIME": "<b>⏰ Пробуждение в: <code>{}</code></b>",
            "quote_media": True,
            "invert_media": True,
            "cooldown_seconds": 30,
        },
    }

    async def client_ready(self, client, db):
        self._db = db
        self._me = await client.get_me()
        self.client = client
        self.username = self._me.username or self._me.first_name
        
        # Восстанавливаем кулдауны из БД
        self.afk_cooldowns = self._db.get(name, "afk_cooldowns", {})
        self.sleep_cooldowns = self._db.get(name, "sleep_cooldowns", {})
        
        # Валидация кулдауна при загрузке
        try:
            current_cooldown = self.config["cooldown_seconds"]
            if not isinstance(current_cooldown, int) or current_cooldown < 5:
                self.config["cooldown_seconds"] = 60
        except Exception:
            self.config["cooldown_seconds"] = 60

    def _get_username(self):
        return self._me.username or self._me.first_name or "Хозяин"

    def _get_config_value(self, key, default=None):
        """Безопасное получение значения из конфига"""
        try:
            if key in self.config:
                return self.config[key]
            return default
        except Exception:
            return default

    def _validate_cooldown_value(self, value):
        """Проверка валидности значения кулдауна"""
        if not isinstance(value, int) or value < 5:
            raise ValueError(self.strings["cooldown_invalid"])
        return value

    def _log_message(self, user):
        data = self.chat_messages[user.id]
        data["name"] = utils.escape_html(user.first_name or "Без имени")
        data["count"] += 1

    def _format_afk_log(self):
        if not self.chat_messages:
            return ""
        lines = []
        for user_id, data in self.chat_messages.items():
            name = data["name"]
            count = data["count"]
            lines.append(
                f'<emoji document_id=5778575233422200567>👤</emoji> <a href="tg://user?id={user_id}">{name}</a> '
                f"(<code>{user_id}</code>) — <b>{count}</b> сообщений"
            )
        return "\n\n<blockquote><b>Пока тебя не было, тебе писали:</b>\n" + "\n".join(lines) + "</blockquote>"

    def _format_duration(self, seconds: int) -> str:
        return str(datetime.timedelta(seconds=max(0, int(seconds))))

    async def _prepare_media(self, media_url: str):
        """Подготовка медиа как в Heroku"""
        media_url = (media_url or "").strip()
        if not media_url or media_url.lower() in {"", "none", "null", "false"}:
            return None
        media = str(media_url)
        if self._get_config_value("quote_media", False) and InputMediaWebPage is not None:
            try:
                return InputMediaWebPage(url=media, optional=True)
            except Exception:
                return media
        return media

    async def _send_with_invert(self, message, text: str, media_url: str = None, reply_to=None):
        """Отправка с инверсией через двухэтапный метод"""
        media = await self._prepare_media(media_url)
        
        if media is None:
            if reply_to:
                await utils.answer(message, text, reply_to=reply_to)
            else:
                await utils.answer(message, text)
            return
        
        if reply_to:
            temp_msg = await self.client.send_message(message.chat_id, "🔄", reply_to=reply_to)
        else:
            temp_msg = await utils.answer(message, "🔄")
        
        await utils.answer(
            temp_msg,
            text,
            file=media,
            invert_media=self._get_config_value("invert_media", False),
        )

    async def _send_response(self, message, text: str, media_url: str = None):
        await self._send_with_invert(message, text, media_url, reply_to=message.id)

    async def _send_command_response(self, message, text: str, media_url: str = None):
        await self._send_with_invert(message, text, media_url, reply_to=None)

    def _check_cooldown(self, cooldown_dict, user_id, mode="afk"):
        """Проверка кулдауна для пользователя"""
        cooldown_seconds = self._get_config_value("cooldown_seconds", 60)
        last_reply_time = cooldown_dict.get(user_id, 0)
        current_time = time.time()
        
        if current_time - last_reply_time >= cooldown_seconds:
            return True, current_time
        return False, None

    def _update_cooldown(self, cooldown_dict, user_id, current_time):
        """Обновление времени последнего ответа"""
        cooldown_dict[user_id] = current_time
        return cooldown_dict

    # ====================== БАННЕР КОМАНДЫ ======================
    @loader.command(
        ru_doc="Ответь на медиа - Установить баннер для AFK режима",
        en_doc="Reply to media - Set banner for AFK mode",
        ua_doc="Відповісти на медіа  — Встановити банер для режиму AFK",
    )
    async def add_afk_banner(self, message):
        """Ответь на медиа - Установить баннер для AFK режима"""
        await self._add_banner(message, "afk")

    @loader.command(
        ru_doc="Ответь на медиа - Установить баннер для SLEEP режима",
        en_doc="Reply to media - Set banner for SLEEP mode",
        ua_doc="Відповісти на медіа  — Встановити банер для режиму SLEEP",
    )
    async def add_sleep_banner(self, message):
        """Ответь на медиа - Установить баннер для SLEEP режима"""
        await self._add_banner(message, "sleep")

    @loader.command(
        ru_doc="Ответь на медиа - Установить баннер для выхода из AFK",
        en_doc="Reply to media - Set banner for AFK OFF mode",
        ua_doc="Відповісти на медіа - Встановити банер для виходу з AFK",
    )
    async def add_afkoff_banner(self, message):
        """Ответь на медиа - Установить баннер для выхода из AFK"""
        await self._add_banner(message, "afk_off")

    @loader.command(
        ru_doc="Ответь на медиа - Установить баннер для выхода из SLEEP",
        en_doc="Reply to media - Set banner for SLEEP OFF mode",
        ua_doc="Відповісти на медіа - Встановити банер для виходу із SLEEP",
    )
    async def add_sleepoff_banner(self, message):
        """Ответь на медиа - Установить баннер для выхода из SLEEP"""
        await self._add_banner(message, "sleep_off")

    @loader.command(
        ru_doc="Показать текущий баннер AFK",
        en_doc="Show current AFK banner",
        ua_doc="Показати поточний банер AFK",
    )
    async def show_afk_banner(self, message):
        """Показать текущий баннер AFK"""
        await self._show_banner(message, "afk")

    @loader.command(
        ru_doc="Показать текущий баннер SLEEP",
        en_doc="Show current SLEEP banner",
        ua_doc="Показати поточний банер SLEEP",
    )
    async def show_sleep_banner(self, message):
        """Показать текущий баннер SLEEP"""
        await self._show_banner(message, "sleep")

    @loader.command(
        ru_doc="Показать текущий баннер AFK OFF",
        en_doc="Show current AFK OFF banner",
        ua_doc="Показати поточний банер AFK OFF",
    )
    async def show_afkoff_banner(self, message):
        """Показать текущий баннер AFK OFF"""
        await self._show_banner(message, "afk_off")

    @loader.command(
        ru_doc="Показать текущий баннер SLEEP OFF",
        en_doc="Show current SLEEP OFF banner",
        ua_doc="Показати поточний банер SLEEP OFF",
    )
    async def show_sleepoff_banner(self, message):
        """Показать текущий баннер SLEEP OFF"""
        await self._show_banner(message, "sleep_off")

    @loader.command(
        ru_doc="Удалить баннер AFK",
        en_doc="Delete AFK banner",
        ua_doc="Видалити банер AFK",
    )
    async def del_afk_banner(self, message):
        """Удалить баннер AFK"""
        self.config["AFK_MEDIA"] = ""
        self._db.set(name, "afk_banner_url", "")
        await utils.answer(message, self.strings["cleared_afk"])

    @loader.command(
        ru_doc="Удалить баннер SLEEP",
        en_doc="Delete SLEEP banner",
        ua_doc="Видалити банер SLEEP",
    )
    async def del_sleep_banner(self, message):
        """Удалить баннер SLEEP"""
        self.config["SLEEP_MEDIA"] = ""
        self._db.set(name, "sleep_banner_url", "")
        await utils.answer(message, self.strings["cleared_sleep"])

    @loader.command(
        ru_doc="Удалить баннер AFK OFF",
        en_doc="Delete AFK OFF banner",
        ua_doc="Видалити банер AFK OFF",
    )
    async def del_afkoff_banner(self, message):
        """Удалить баннер AFK OFF"""
        self.config["AFK_OFF_MEDIA"] = ""
        self._db.set(name, "afk_off_banner_url", "")
        await utils.answer(message, self.strings["cleared_afk_off"])

    @loader.command(
        ru_doc="Удалить баннер SLEEP OFF",
        en_doc="Delete SLEEP OFF banner",
        ua_doc="Видалити банер SLEEP OFF",
    )
    async def del_sleepoff_banner(self, message):
        """Удалить баннер SLEEP OFF"""
        self.config["SLEEP_OFF_MEDIA"] = ""
        self._db.set(name, "sleep_off_banner_url", "")
        await utils.answer(message, self.strings["cleared_sleep_off"])

    async def _upload_media(self, file_path: str, ext: str):
        """Загрузка медиа на сервер"""
        try:
            import requests
            with open(file_path, 'rb') as f:
                resp = requests.post('https://x0.at/', files={'file': (f'banner.{ext}', f)}, timeout=30)
            if resp.status_code == 200 and resp.text.strip().startswith('http'):
                return resp.text.strip()
        except Exception as e:
            logger.error(f"Upload error: {e}")
        return None

    async def _add_banner(self, message, banner_type: str):
        """Добавление баннера для указанного типа"""
        try:
            import requests
        except ImportError:
            await utils.answer(message, self.strings("no_requests"))
            return

        replied = await message.get_reply_message()
        if not replied:
            await utils.answer(message, self.strings("no_reply"))
            return
        
        # Исправленная проверка наличия медиа
        has_media = False
        media_type = "jpg"
        
        # Проверяем наличие различных типов медиа
        if hasattr(replied, 'photo') and replied.photo:
            has_media = True
            media_type = "jpg"
        elif hasattr(replied, 'video') and replied.video:
            has_media = True
            media_type = "mp4"
        elif hasattr(replied, 'document') and replied.document:
            # Проверяем, не является ли документ GIF или другим анимированным файлом
            has_media = True
            # Пытаемся определить тип по mime_type или расширению
            if hasattr(replied.document, 'mime_type'):
                if 'gif' in replied.document.mime_type.lower():
                    media_type = "gif"
                elif 'video' in replied.document.mime_type.lower():
                    media_type = "mp4"
            # Также можно проверить атрибут animation, если он существует
            elif hasattr(replied, 'gif') and replied.gif:
                media_type = "gif"
        
        if not has_media:
            # Дополнительная проверка через media
            if hasattr(replied, 'media') and replied.media:
                has_media = True
                # Определяем тип по document
                if hasattr(replied.media, 'document'):
                    doc = replied.media.document
                    if hasattr(doc, 'mime_type'):
                        if 'gif' in doc.mime_type.lower():
                            media_type = "gif"
                        elif 'video' in doc.mime_type.lower():
                            media_type = "mp4"
                    # Проверяем атрибуты документа
                    if hasattr(doc, 'attributes'):
                        for attr in doc.attributes:
                            if hasattr(attr, 'file_name'):
                                if attr.file_name and attr.file_name.lower().endswith('.gif'):
                                    media_type = "gif"
            elif hasattr(replied, 'sticker') and replied.sticker:
                has_media = True
                media_type = "webp"
        
        if not has_media:
            await utils.answer(message, self.strings("no_media"))
            return
        
        status = await utils.answer(message, self.strings("uploading"))
        
        ext = media_type
        tmp_path = None
        try:
            import tempfile
            import os
            
            tmp_path = os.path.join(tempfile.gettempdir(), f"banner_{message.id}.{ext}")
            await self.client.download_media(replied, file=tmp_path)
            
            if not os.path.exists(tmp_path) or os.path.getsize(tmp_path) == 0:
                await status.edit(self.strings("failed"))
                return
            
            url = await self._upload_media(tmp_path, ext)
            
            if not url:
                await status.edit(self.strings("failed"))
                return
            
            # Сохраняем URL в соответствующую конфигурацию
            if banner_type == "afk":
                self.config["AFK_MEDIA"] = url
                self._db.set(name, "afk_banner_url", url)
                await status.edit(self.strings("added_afk"))
            elif banner_type == "sleep":
                self.config["SLEEP_MEDIA"] = url
                self._db.set(name, "sleep_banner_url", url)
                await status.edit(self.strings("added_sleep"))
            elif banner_type == "afk_off":
                self.config["AFK_OFF_MEDIA"] = url
                self._db.set(name, "afk_off_banner_url", url)
                await status.edit(self.strings("added_afk_off"))
            elif banner_type == "sleep_off":
                self.config["SLEEP_OFF_MEDIA"] = url
                self._db.set(name, "sleep_off_banner_url", url)
                await status.edit(self.strings("added_sleep_off"))
                
        except Exception as e:
            logger.error(f"Error: {e}")
            await status.edit(self.strings("failed"))
        finally:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except:
                    pass

    async def _show_banner(self, message, banner_type: str):
        """Показать текущий баннер"""
        if banner_type == "afk":
            url = self._get_config_value("AFK_MEDIA", "")
            text = self.strings("showing_afk")
        elif banner_type == "sleep":
            url = self._get_config_value("SLEEP_MEDIA", "")
            text = self.strings("showing_sleep")
        elif banner_type == "afk_off":
            url = self._get_config_value("AFK_OFF_MEDIA", "")
            text = self.strings("showing_afk_off")
        elif banner_type == "sleep_off":
            url = self._get_config_value("SLEEP_OFF_MEDIA", "")
            text = self.strings("showing_sleep_off")
        else:
            return
        
        if not url:
            await utils.answer(message, self.strings("no_banner"))
            return
        
        # Отправляем медиа
        media = await self._prepare_media(url)
        if media:
            await self._send_command_response(message, text, url)
        else:
            await utils.answer(message, f"{text}\n\n<code>{url}</code>")

    # ====================== AFK КОМАНДЫ ======================
    @loader.command(
        ru_doc="[причина] | [время] — Включить AFK режим",
        en_doc="[reason] | [time] — Enable AFK mode",
        ua_doc="[причина] | [час] — Увімкнути AFK",
    )
    async def afk(self, message):
        """Включить AFK режим. Можно указать причину и время возвращения через |"""
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
                    self._old_status = me.emoji_status
                await self.client(
                    functions.account.UpdateEmojiStatusRequest(
                        emoji_status=types.EmojiStatus(
                            document_id=self._get_config_value("customEmojiStatus", 4969889971700761796)
                        )
                    )
                )
            except Exception as e:
                logger.error(f"Не удалось обновить статус: {e}")

        self._db.set(name, "afk", reason or True)
        self._db.set(name, "gone", time.time())
        self._db.set(name, "return_time", time_val)
        self.chat_messages.clear()
        
        # Сброс кулдаунов при новом AFK
        self.afk_cooldowns = {}
        self._db.set(name, "afk_cooldowns", self.afk_cooldowns)

        username = self._get_username()
        reason_text = ""
        if reason:
            reason_text = f"<blockquote><emoji document_id=5870729937215819584>⏰️</emoji> <b>Причина:</b> {utils.escape_html(reason)}</blockquote>"
        come_time_text = ""
        if time_val:
            come_time_text = f"<blockquote><emoji document_id=5873146865637133757>🎤</emoji> <b>Прийду через:</b> {utils.escape_html(time_val)}</blockquote>"

        preview = self._get_config_value("MSG_AFK_REPLY", self.strings["default_afk_message"]).format(
            was_online="Только что",
            username=username,
            reason_text=reason_text,
            come_time=come_time_text,
        )

        full_text = self._get_config_value("MSG_AFK_ON", self.strings["afk_on"]) + "\n\n" + preview
        await self._send_command_response(message, full_text, self._get_config_value("AFK_MEDIA", ""))

    @loader.command(
        ru_doc="Выключить AFK режим",
        en_doc="Disable AFK mode",
        ua_doc="Вимкнути AFK",
    )
    async def unafk(self, message):
        """Выключить AFK режим и показать кто писал"""
        gone = self._db.get(name, "gone")
        duration_text = ""

        if gone:
            diff_seconds = time.time() - gone
            duration_text = (
                f"\n<emoji document_id=5870729937215819584>⏰️</emoji> "
                f"<b>Был в AFK:</b> <code>{self._format_duration(diff_seconds)}</code>"
            )

        self._db.set(name, "afk", False)
        self._db.set(name, "gone", None)
        self._db.set(name, "return_time", None)
        
        # Очищаем кулдауны при выходе из AFK
        self.afk_cooldowns = {}
        self._db.set(name, "afk_cooldowns", self.afk_cooldowns)

        log_text = self._format_afk_log()
        self.chat_messages.clear()

        if self._get_config_value("setPremiumStatus", True) and self._old_status:
            try:
                await self.client(
                    functions.account.UpdateEmojiStatusRequest(
                        emoji_status=self._old_status
                    )
                )
            except Exception as e:
                logger.error(f"Не удалось восстановить статус: {e}")

        username = self._get_username()
        full_text = self._get_config_value("MSG_AFK_OFF", self.strings["back"]).format(username=username) + duration_text + (log_text or "")
        await self._send_command_response(message, full_text, self._get_config_value("AFK_OFF_MEDIA", ""))

    # ====================== SLEEP КОМАНДЫ ======================
    @loader.command(
        ru_doc="[время] — Включить SLEEP режим",
        en_doc="[time] — Enable SLEEP mode",
        ua_doc="[час] — Увімкнути SLEEP",
    )
    async def sleep(self, message):
        """Включить SLEEP режим. Можно указать время пробуждения"""
        args = utils.get_args_raw(message)
        wake_time = args if args else None

        if self._get_config_value("setPremiumStatus", True):
            try:
                me = await self.client.get_me()
                if me.emoji_status:
                    self._old_status = me.emoji_status
                await self.client(
                    functions.account.UpdateEmojiStatusRequest(
                        emoji_status=types.EmojiStatus(
                            document_id=self._get_config_value("customSleepEmojiStatus", 5229252352948379900)
                        )
                    )
                )
            except Exception as e:
                logger.error(f"Не удалось обновить статус: {e}")

        self._db.set(name, "sleep", True)
        self._db.set(name, "sleep_start", time.time())
        self._db.set(name, "wake_time", wake_time)
        self.chat_messages.clear()
        
        # Сброс кулдаунов SLEEP при новом режиме
        self.sleep_cooldowns = {}
        self._db.set(name, "sleep_cooldowns", self.sleep_cooldowns)

        username = self._get_username()
        wake_text = self._get_config_value("MSG_WAKE_TIME", self.strings["wake_text"]).format(utils.escape_html(wake_time)) if wake_time else ""
        preview = self._get_config_value("MSG_SLEEP_REPLY", self.strings["sleep_msg"]).format(
            was_online="Только что",
            username=username,
            wake_time=wake_text
        )

        full_text = self._get_config_value("MSG_SLEEP_ON", self.strings["sleep_on"]) + "\n\n" + preview
        await self._send_command_response(message, full_text, self._get_config_value("SLEEP_MEDIA", ""))

    @loader.command(
        ru_doc="Выключить SLEEP режим",
        en_doc="Disable SLEEP mode",
        ua_doc="Вимкнути SLEEP",
    )
    async def unsleep(self, message):
        """Выключить SLEEP режим и показать кто писал"""
        sleep_start = self._db.get(name, "sleep_start")
        duration_text = ""

        if sleep_start:
            diff_seconds = time.time() - sleep_start
            duration_text = (
                f"\n<emoji document_id=5870729937215819584>⏰️</emoji> "
                f"<b>Спал:</b> <code>{self._format_duration(diff_seconds)}</code>"
            )

        self._db.set(name, "sleep", False)
        self._db.set(name, "sleep_start", None)
        self._db.set(name, "wake_time", None)
        
        # Очищаем кулдауны при выходе из SLEEP
        self.sleep_cooldowns = {}
        self._db.set(name, "sleep_cooldowns", self.sleep_cooldowns)

        log_text = self._format_afk_log()
        self.chat_messages.clear()

        if self._get_config_value("setPremiumStatus", True) and self._old_status:
            try:
                await self.client(
                    functions.account.UpdateEmojiStatusRequest(
                        emoji_status=self._old_status
                    )
                )
            except Exception as e:
                logger.error(f"Не удалось восстановить статус: {e}")

        username = self._get_username()
        full_text = self._get_config_value("MSG_SLEEP_OFF", self.strings["sleep_off"]).format(username=username) + duration_text + (log_text or "")
        await self._send_command_response(message, full_text, self._get_config_value("SLEEP_OFF_MEDIA", ""))

    # ====================== КОМАНДА УСТАНОВКИ КУЛДАУНА ======================
    @loader.command(
        ru_doc="<секунды> — Установить время кулдауна между AFK-ответами (минимум 5 секунд)",
        en_doc="<seconds> — Set cooldown time between AFK responses (minimum 5 seconds)",
        ua_doc="<секунди> — Встановити час кулдауну між AFK-відповідями (мінімум 5 секунд)",
    )
    async def afkcooldown(self, message):
        """Установить время кулдауна между AFK-ответами одному пользователю (минимум 5 секунд)"""
        args = utils.get_args_raw(message)
        try:
            new_cooldown = int(args)
            self._validate_cooldown_value(new_cooldown)
            self.config["cooldown_seconds"] = new_cooldown
            await utils.answer(message, self.strings["cooldown_set"].format(new_cooldown))
        except ValueError as e:
            await utils.answer(message, self.strings["cooldown_invalid"])

    # ====================== ПРЕСЕТЫ ======================
    @loader.command(
        en_doc=(
            "[save/load/del/list/pack] [name] — Preset manager. Examples: "
            ".afkpreset pack adds two packs (anime, strict); "
            ".afkpreset list shows saved presets; "
            ".afkpreset load [name] loads a preset; "
            ".afkpreset del [name] deletes a preset; "
            ".afkpreset save [name] saves current cfg as a preset."
        ),
        ru_doc=(
            "[save/load/del/list/pack] [название] — Управление пресетами. Примеры: "
            ".afkpreset pack - добавляет в базу данных два пака anime и strict; "
            ".afkpreset list - выводит сохранённые пресеты; "
            ".afkpreset load [название] - загружает пресет из БД; "
            ".afkpreset del [название] - удаляет пресет; "
            ".afkpreset save [название] - сохраняет текущий cfg как пресет."
        ),
        ua_doc=(
            "[save/load/del/list/pack] [назва] — Керування пресетами. Приклади: "
            ".afkpreset pack додає два паки (anime, strict); "
            ".afkpreset list показує збережені пресети; "
            ".afkpreset load [назва] завантажує пресет; "
            ".afkpreset del [назва] видаляє пресет; "
            ".afkpreset save [назва] зберігає поточний cfg як пресет."
        ),
    )
    async def afkpreset(self, message):
        """
        Управление пресетами настроек.
        save [name] - сохранить текущие настройки
        load [name] - загрузить пресет
        del [name] - удалить пресет
        list - показать все пресеты
        pack - добавить стандартные пресеты (anime, strict)
        """
        args = utils.get_args_raw(message).split(maxsplit=1)
        action = args[0].lower() if args else "list"
        name_preset = args[1] if len(args) > 1 else None
        presets = self._db.get(name, "presets", {})

        if action == "save":
            if not name_preset:
                await utils.answer(message, "Укажите название пресета!")
                return
            current_preset_data = {}
            for key in self.CONFIG_KEYS_TO_SAVE:
                if key in self.config:
                    current_preset_data[key] = self.config[key]
            presets[name_preset] = current_preset_data
            self._db.set(name, "presets", presets)
            await utils.answer(message, self.strings["preset_saved"].format(name_preset))

        elif action == "load":
            if not name_preset:
                await utils.answer(message, "Укажите название пресета для загрузки!")
                return
            if name_preset not in presets:
                await utils.answer(message, self.strings["preset_not_found"].format(name_preset))
                return
            preset_data = presets[name_preset]
            loaded_keys = []
            missing_keys = []
            
            for key, value in preset_data.items():
                if key in self.config:
                    self.config[key] = value
                    loaded_keys.append(key)
                else:
                    missing_keys.append(key)
            
            result_msg = self.strings["preset_loaded"].format(name_preset)
            if loaded_keys:
                result_msg += f"\n\n<emoji document_id=5870730156259152122>✅</emoji> <b>Загружено:</b> {', '.join(loaded_keys)}"
            if missing_keys:
                result_msg += f"\n\n<emoji document_id=5870730156259152122>⚠️</emoji> <b>Не загружены (неизвестные ключи):</b> {', '.join(missing_keys)}"
            await utils.answer(message, result_msg)

        elif action == "del":
            if not name_preset:
                await utils.answer(message, "Укажите название пресета для удаления!")
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
            await utils.answer(message, "Неизвестное действие. Доступные: save, load, del, list, pack")

    # ====================== WATCHER ======================
    async def watcher(self, message):
        if not isinstance(message, types.Message):
            return

        if message.mentioned or getattr(message.to_id, "user_id", None) == self._me.id:
            afk_state = self._db.get(name, "afk", False)
            sleep_state = self._db.get(name, "sleep", False)

            if not afk_state and not sleep_state:
                return

            try:
                user = await self.client.get_entity(message.sender_id)
            except:
                return

            if user.is_self or user.bot:
                return

            self._log_message(user)

            # Проверка кулдауна
            if sleep_state:
                can_reply, current_time = self._check_cooldown(self.sleep_cooldowns, user.id, "sleep")
                if not can_reply:
                    logger.debug(f"Кулдаун для пользователя {user.id} в SLEEP режиме, пропускаем ответ")
                    return
            else:
                can_reply, current_time = self._check_cooldown(self.afk_cooldowns, user.id, "afk")
                if not can_reply:
                    logger.debug(f"Кулдаун для пользователя {user.id} в AFK режиме, пропускаем ответ")
                    return

            username = self._get_username()

            if sleep_state:
                sleep_start = self._db.get(name, "sleep_start")
                diff_seconds = int(time.time() - sleep_start) if sleep_start else 0
                if diff_seconds < 0:
                    diff_seconds = 0

                was_online = str(datetime.timedelta(seconds=diff_seconds))
                wake_time = self._db.get(name, "wake_time")
                wake_text = self._get_config_value("MSG_WAKE_TIME", self.strings["wake_text"]).format(utils.escape_html(wake_time)) if wake_time else ""
                text = self._get_config_value("MSG_SLEEP_REPLY", self.strings["sleep_msg"]).format(
                    was_online=was_online,
                    username=username,
                    wake_time=wake_text,
                )
                media_url = self._get_config_value("SLEEP_MEDIA", "")
                
                # Обновляем кулдаун после успешной отправки
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

                reason_text = ""
                if reason:
                    reason_text = f"<blockquote><emoji document_id=5870729937215819584>⏰️</emoji> <b>Причина:</b> {utils.escape_html(reason)}</blockquote>"
                come_time_text = ""
                if return_time:
                    come_time_text = f"<blockquote><emoji document_id=5873146865637133757>🎤</emoji> <b>Прийду через:</b> {utils.escape_html(return_time)}</blockquote>"

                text = self._get_config_value("MSG_AFK_REPLY", self.strings["default_afk_message"]).format(
                    was_online=was_online,
                    username=username,
                    reason_text=reason_text,
                    come_time=come_time_text,
                )
                media_url = self._get_config_value("AFK_MEDIA", "")
                
                # Обновляем кулдаун после успешной отправки
                self.afk_cooldowns = self._update_cooldown(self.afk_cooldowns, user.id, current_time)
                self._db.set(name, "afk_cooldowns", self.afk_cooldowns)

            await self._send_response(message, text, media_url)
