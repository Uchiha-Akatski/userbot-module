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

__version__ = (1, 10, 15)

name = "ItachiAFK"
logger = logging.getLogger(name)


@loader.tds
class ItachiAFKMod(loader.Module):
    """AFK/SLEEP модуль с логированием и кликабельными никами"""

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
            "<blockquote><emoji document_id=5229252352948379900>⭐️</emoji> <b>Unit Alpha Heroku</b> | <i>Powered by Heroku Userbot</i></blockquote>\n\n"
            "<blockquote><emoji document_id=4969889971700761796>✨</emoji> <b>Статус:</b> <i>Премиум-режим активен</i> 👑</blockquote>"
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
            "<blockquote><emoji document_id=5229252352948379900>⭐️</emoji> <b>Unit Alpha Heroku</b> | <i>Sleep Mode Activated</i></blockquote>"
        ),
        "wake_text": "\n\n<blockquote><emoji document_id=5873146865637133757>🎤</emoji> <b>Проснусь через:</b> <code>{}</code></blockquote>",
        "sleep_off": "<emoji document_id=5883964170268840032>👤</emoji> <b>@{username} проснулся и готов к бою!</b>",
        "preset_saved": "<emoji document_id=5870730156259152122>✅</emoji> <b>Пресет '{}' сохранён!</b>",
        "preset_loaded": "<emoji document_id=5870730156259152122>✅</emoji> <b>Пресет '{}' загружен!</b>",
        "preset_deleted": "<emoji document_id=5870730156259152122>✅</emoji> <b>Пресет '{}' удалён!</b>",
        "preset_not_found": "<emoji document_id=5870730156259152122>❌</emoji> <b>Пресет '{}' не найден!</b>",
        "preset_pack_added": "<emoji document_id=5870730156259152122>✅</emoji> <b>Добавлено {} дефолтных пресетов!</b>",
        "presets_list": "<emoji document_id=5870730156259152122>📋</emoji> <b>Список пресетов:</b>\n\n",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue("setPremiumStatus", True, "Ставить премиум-статус при AFK/SLEEP.", validator=loader.validators.Boolean()),
            loader.ConfigValue("customEmojiStatus", 4969889971700761796, "Кастомный премиум-статус для AFK.", validator=loader.validators.Integer()),
            loader.ConfigValue("customSleepEmojiStatus", 5229252352948379900, "Кастомный премиум-статус для SLEEP.", validator=loader.validators.Integer()),
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
        )

        self.answered_users = set()
        self.chat_messages = defaultdict(lambda: {"name": "", "count": 0})
        self._old_status = None

    CONFIG_KEYS_TO_SAVE = [
        "customEmojiStatus", "customSleepEmojiStatus", "MSG_AFK_REPLY", "MSG_AFK_ON",
        "AFK_MEDIA", "AFK_OFF_MEDIA", "MSG_AFK_OFF", "MSG_SLEEP_ON", "MSG_SLEEP_REPLY",
        "SLEEP_MEDIA", "SLEEP_OFF_MEDIA", "MSG_SLEEP_OFF", "MSG_WAKE_TIME",
        "quote_media", "invert_media",
    ]

    PRESET_PACK = {
        "anime": {
            "customEmojiStatus": 4969889971700761796,
            "customSleepEmojiStatus": 5229252352948379900,
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
        },
        "strict": {
            "customEmojiStatus": 5229252352948379900,
            "customSleepEmojiStatus": 5229252352948379900,
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
        },
    }

    async def client_ready(self, client, db):
        self._db = db
        self._me = await client.get_me()
        self.client = client
        self.username = self._me.username or self._me.first_name

    def _get_username(self):
        return self._me.username or self._me.first_name or "Хозяин"

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

    # ====================== ОСНОВНАЯ ОТПРАВКА С ИНВЕРСИЕЙ ======================
    async def _prepare_media(self, media_url: str):
        """Подготовка медиа как в Heroku"""
        media_url = (media_url or "").strip()
        if not media_url or media_url.lower() in {"", "none", "null", "false"}:
            return None
        media = str(media_url)
        if self.config.get("quote_media", False) and InputMediaWebPage is not None:
            try:
                return InputMediaWebPage(url=media, optional=True)
            except Exception:
                return media
        return media

    async def _send_with_invert(self, message, text: str, media_url: str = None, reply_to=None):
        """Отправка с инверсией через двухэтапный метод (как в Heroku)"""
        media = await self._prepare_media(media_url)
        
        # Нет медиа — отправляем сразу
        if media is None:
            if reply_to:
                await utils.answer(message, text, reply_to=reply_to)
            else:
                await utils.answer(message, text)
            return
        
        # Как в Heroku: сначала отправляем заглушку
        if reply_to:
            temp_msg = await self.client.send_message(message.chat_id, "🔄", reply_to=reply_to)
        else:
            temp_msg = await utils.answer(message, "🔄")
        
        # Потом редактируем её с медиа и invert_media
        await utils.answer(
            temp_msg,
            text,
            file=media,
            invert_media=self.config.get("invert_media", False),
        )

    async def _send_response(self, message, text: str, media_url: str = None):
        """Ответ пользователю в watcher"""
        await self._send_with_invert(message, text, media_url, reply_to=message.id)

    async def _send_command_response(self, message, text: str, media_url: str = None):
        """Ответ на команду"""
        await self._send_with_invert(message, text, media_url, reply_to=None)

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

        if self.config["setPremiumStatus"]:
            try:
                me = await self.client.get_me()
                if me.emoji_status:
                    self._old_status = me.emoji_status
                await self.client(
                    functions.account.UpdateEmojiStatusRequest(
                        emoji_status=types.EmojiStatus(
                            document_id=self.config["customEmojiStatus"]
                        )
                    )
                )
            except Exception as e:
                logger.error(f"Не удалось обновить статус: {e}")

        self._db.set(name, "afk", reason or True)
        self._db.set(name, "gone", time.time())
        self._db.set(name, "return_time", time_val)
        self.answered_users.clear()
        self.chat_messages.clear()

        username = self._get_username()
        reason_text = ""
        if reason:
            reason_text = f"<blockquote><emoji document_id=5870729937215819584>⏰️</emoji> <b>Причина:</b> {utils.escape_html(reason)}</blockquote>"
        come_time_text = ""
        if time_val:
            come_time_text = f"<blockquote><emoji document_id=5873146865637133757>🎤</emoji> <b>Прийду через:</b> {utils.escape_html(time_val)}</blockquote>"

        preview = self.config["MSG_AFK_REPLY"].format(
            was_online="Только что",
            username=username,
            reason_text=reason_text,
            come_time=come_time_text,
        )

        full_text = self.config["MSG_AFK_ON"] + "\n\n" + preview
        await self._send_command_response(message, full_text, self.config["AFK_MEDIA"])

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
        self.answered_users.clear()

        log_text = self._format_afk_log()
        self.chat_messages.clear()

        if self.config["setPremiumStatus"] and self._old_status:
            try:
                await self.client(
                    functions.account.UpdateEmojiStatusRequest(
                        emoji_status=self._old_status
                    )
                )
            except Exception as e:
                logger.error(f"Не удалось восстановить статус: {e}")

        username = self._get_username()
        full_text = self.config["MSG_AFK_OFF"].format(username=username) + duration_text + (log_text or "")
        await self._send_command_response(message, full_text, self.config["AFK_OFF_MEDIA"])

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

        if self.config["setPremiumStatus"]:
            try:
                me = await self.client.get_me()
                if me.emoji_status:
                    self._old_status = me.emoji_status
                await self.client(
                    functions.account.UpdateEmojiStatusRequest(
                        emoji_status=types.EmojiStatus(
                            document_id=self.config["customSleepEmojiStatus"]
                        )
                    )
                )
            except Exception as e:
                logger.error(f"Не удалось обновить статус: {e}")

        self._db.set(name, "sleep", True)
        self._db.set(name, "sleep_start", time.time())
        self._db.set(name, "wake_time", wake_time)
        self.answered_users.clear()
        self.chat_messages.clear()

        username = self._get_username()
        wake_text = self.config["MSG_WAKE_TIME"].format(utils.escape_html(wake_time)) if wake_time else ""
        preview = self.config["MSG_SLEEP_REPLY"].format(
            was_online="Только что",
            username=username,
            wake_time=wake_text
        )

        full_text = self.config["MSG_SLEEP_ON"] + "\n\n" + preview
        await self._send_command_response(message, full_text, self.config["SLEEP_MEDIA"])

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
        self.answered_users.clear()

        log_text = self._format_afk_log()
        self.chat_messages.clear()

        if self.config["setPremiumStatus"] and self._old_status:
            try:
                await self.client(
                    functions.account.UpdateEmojiStatusRequest(
                        emoji_status=self._old_status
                    )
                )
            except Exception as e:
                logger.error(f"Не удалось восстановить статус: {e}")

        username = self._get_username()
        full_text = self.config["MSG_SLEEP_OFF"].format(username=username) + duration_text + (log_text or "")
        await self._send_command_response(message, full_text, self.config["SLEEP_OFF_MEDIA"])

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
            media_keys = ["AFK_MEDIA", "AFK_OFF_MEDIA", "SLEEP_MEDIA", "SLEEP_OFF_MEDIA"]
            for key in self.CONFIG_KEYS_TO_SAVE:
                if key not in self.config:
                    continue
                value = self.config[key]
                # Пропускаем пустые медиа-поля
                if key in media_keys and (value is None or str(value).strip() == ""):
                    continue
                current_preset_data[key] = value
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
            for key, value in preset_data.items():
                if key in self.config:
                    self.config[key] = value
            await utils.answer(message, self.strings["preset_loaded"].format(name_preset))

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

            if user.id in self.answered_users:
                return

            self.answered_users.add(user.id)

            username = self._get_username()

            if sleep_state:
                sleep_start = self._db.get(name, "sleep_start")
                diff_seconds = int(time.time() - sleep_start) if sleep_start else 0
                if diff_seconds < 0:
                    diff_seconds = 0

                was_online = str(datetime.timedelta(seconds=diff_seconds))
                wake_time = self._db.get(name, "wake_time")
                wake_text = self.config["MSG_WAKE_TIME"].format(utils.escape_html(wake_time)) if wake_time else ""
                text = self.config["MSG_SLEEP_REPLY"].format(
                    was_online=was_online,
                    username=username,
                    wake_time=wake_text,
                )
                media_url = self.config["SLEEP_MEDIA"]
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

                text = self.config["MSG_AFK_REPLY"].format(
                    was_online=was_online,
                    username=username,
                    reason_text=reason_text,
                    come_time=come_time_text,
                )
                media_url = self.config["AFK_MEDIA"]

            await self._send_response(message, text, media_url)
