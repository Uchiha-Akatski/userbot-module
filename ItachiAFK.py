# meta developer: @Itachi_Uchiha_sss

from .. import loader, utils
from telethon import types, functions
import time
import datetime
import logging
from collections import defaultdict

__version__ = (1, 9, 0)

name = "ItachiAFK"
logger = logging.getLogger(name)


@loader.tds
class ItachiAFKMod(loader.Module):
    """AFK/SLEEP модуль с логированием и кликабельными никами"""

    strings = {
        "name": "ItachiAFK",
        "back": "<emoji document_id=5883964170268840032>👤</emoji> <b>Больше не в режиме AFK.</b>",
        "default_afk_message": (
            "<emoji document_id=5870948572526022116>✋</emoji> <b>Сейчас я в AFK-режиме</b>\n"
            "<emoji document_id=5870695289714643076>👤</emoji> <b>Был в сети:</b> {was_online} назад\n"
            "{reason_text}{come_time}"
        ),
        "sleep_on": (
            "<emoji document_id=5870729937215819584>💤</emoji> <b>SLEEP-режим включён!</b>\n"
            "<emoji document_id=5873146865637133757>😴</emoji> <b>ItachiAFK будет отвечать этим сообщением:</b>\n\n"
        ),
        "sleep_msg": (
            "<emoji document_id=5870729937215819584>💤</emoji> <b>Сейчас я в Sleep-режиме</b>\n"
            "<emoji document_id=5877700484453634587>🌙</emoji> <b>Не беспокоить, я сплю</b>\n"
            "<emoji document_id=5870695289714643076>👤</emoji> <b>Был в сети:</b> {was_online} назад\n"
            "{wake_time}"
        ),
        "wake_text": "<emoji document_id=5873146865637133757>🎤</emoji> <b>Проснусь в:</b> <b>{}</b>",
        "sleep_off": "<emoji document_id=5883964170268840032>👤</emoji> <b>Проснулся, Sleep-режим отключён.</b>",
        "preset_saved": "<emoji document_id=5870730156259152122>✅</emoji> <b>Пресет '{}' сохранён!</b>",
        "preset_loaded": "<emoji document_id=5870730156259152122>✅</emoji> <b>Пресет '{}' загружен!</b>",
        "preset_deleted": "<emoji document_id=5870730156259152122>✅</emoji> <b>Пресет '{}' удалён!</b>",
        "preset_not_found": "<emoji document_id=5870730156259152122>❌</emoji> <b>Пресет '{}' не найден!</b>",
        "preset_pack_added": "<emoji document_id=5870730156259152122>✅</emoji> <b>Добавлено {} дефолтных пресетов!</b>",
        "presets_list": "<emoji document_id=5870730156259152122>📋</emoji> <b>Список пресетов:</b>\n\n",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "setPremiumStatus",
                True,
                lambda: "Ставить премиум-статус при AFK/SLEEP.",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "customEmojiStatus",
                4969889971700761796,
                lambda: "Кастомный премиум-статус для AFK.",
                validator=loader.validators.Integer(),
            ),
            loader.ConfigValue(
                "customSleepEmojiStatus",
                5229252352948379900,
                lambda: "Кастомный премиум-статус для SLEEP.",
                validator=loader.validators.Integer(),
            ),
            loader.ConfigValue(
                "MSG_AFK_REPLY",
                self.strings["default_afk_message"],
                lambda: "Текст ответа в AFK.",
            ),
            loader.ConfigValue(
                "MSG_AFK_OFF",
                self.strings["back"],
                lambda: "Текст выхода из AFK.",
            ),
            loader.ConfigValue(
                "MSG_SLEEP_ON",
                self.strings["sleep_on"],
                lambda: "Текст включения SLEEP.",
            ),
            loader.ConfigValue(
                "MSG_SLEEP_REPLY",
                self.strings["sleep_msg"],
                lambda: "Текст ответа в SLEEP.",
            ),
            loader.ConfigValue(
                "MSG_SLEEP_OFF",
                self.strings["sleep_off"],
                lambda: "Текст выхода из SLEEP.",
            ),
            loader.ConfigValue(
                "MSG_WAKE_TIME",
                self.strings["wake_text"],
                lambda: "Формат текста времени просыпания.",
            ),
        )

        self.answered_users = set()
        # user_id -> {"name": str, "count": int}
        self.chat_messages = defaultdict(lambda: {"name": "", "count": 0})
        self._old_status = None

    CONFIG_KEYS_TO_SAVE = [
        "customEmojiStatus",
        "customSleepEmojiStatus",
        "MSG_AFK_REPLY",
        "MSG_AFK_OFF",
        "MSG_SLEEP_ON",
        "MSG_SLEEP_REPLY",
        "MSG_SLEEP_OFF",
        "MSG_WAKE_TIME",
    ]

    PRESET_PACK = {
        "anime": {
            "customEmojiStatus": 4969889971700761796,
            "customSleepEmojiStatus": 5229252352948379900,
            "MSG_AFK_REPLY": (
                "<emoji document_id=5870948572526022116>✋</emoji> <b>Аниме-пауза!</b>\n"
                "<emoji document_id=5870695289714643076>👤</emoji> <b>Нет в сети:</b> {was_online}\n"
                "{reason_text}{come_time}"
            ),
            "MSG_AFK_OFF": "<emoji document_id=5883964170268840032>👤</emoji> <b>Я вернулся из мира аниме!</b>",
            "MSG_SLEEP_ON": "<emoji document_id=5870729937215819584>💤</emoji> <b>Ушел смотреть сны...</b>",
            "MSG_SLEEP_REPLY": (
                "<emoji document_id=5870729937215819584>💤</emoji> <b>Я сплю.</b>\n"
                "<emoji document_id=5870695289714643076>👤</emoji> <b>Сплю уже:</b> {was_online}\n"
                "{wake_time}"
            ),
            "MSG_SLEEP_OFF": "<emoji document_id=5883964170268840032>👤</emoji> <b>Доброе утро!</b>",
            "MSG_WAKE_TIME": "<emoji document_id=5873146865637133757>🎤</emoji> <b>Проснусь в:</b> <b>{}</b>",
        },
        "strict": {
            "customEmojiStatus": 5229252352948379900,
            "customSleepEmojiStatus": 5229252352948379900,
            "MSG_AFK_REPLY": (
                "<b>ЗАНЯТ.</b>\nОтсутствую: {was_online}\n{reason_text}{come_time}"
            ),
            "MSG_AFK_OFF": "<b>ВЕРНУЛСЯ.</b>",
            "MSG_SLEEP_ON": "<b>РЕЖИМ СНА.</b>",
            "MSG_SLEEP_REPLY": ("<b>СПЛЮ.</b>\nВремя сна: {was_online}\n{wake_time}"),
            "MSG_SLEEP_OFF": "<b>ДОСТУПЕН.</b>",
            "MSG_WAKE_TIME": "Буду в: <b>{}</b>",
        },
    }

    async def client_ready(self, client, db):
        self._db = db
        self._me = await client.get_me()
        self.client = client

    # --- ЛОГ ---
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

        return (
            "\n\n<blockquote>"
            "<b>Пока тебя не было, тебе писали:</b>\n"
            + "\n".join(lines)
            + "</blockquote>"
        )

    def _format_duration(self, seconds: int) -> str:
        if seconds < 0:
            seconds = 0
        return str(datetime.timedelta(seconds=int(seconds)))

    # --- AFK ---
    @loader.command(
        en_doc="[reason] | [time] — Enable AFK",
        ru_doc="[причина] | [время] — Установить AFK",
        ua_doc="[причина] | [час] — Увімкнути AFK",
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

        preview = self.config["MSG_AFK_REPLY"].format(
            was_online="Только что",
            reason_text=(
                f"<emoji document_id=5870729937215819584>⏰️</emoji> <b>Причина:</b> <i>{reason}</i>\n"
                if reason
                else ""
            ),
            come_time=(
                f"<emoji document_id=5873146865637133757>🎤</emoji> <b>Прийду через:</b> <b>{time_val}</b>"
                if time_val
                else ""
            ),
        )

        await utils.answer(
            message,
            "<emoji document_id=5870730156259152122>😀</emoji> <b>AFK включён!</b>\n"
            "<emoji document_id=5877700484453634587>✈️</emoji> ItachiAFK будет отвечать этим:\n\n"
            + preview,
        )

    @loader.command(
        en_doc="Disable AFK",
        ru_doc="Отключить AFK",
        ua_doc="Вимкнути AFK",
    )
    async def unafk(self, message):
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

        await utils.answer(
            message,
            self.config["MSG_AFK_OFF"] + duration_text + (log_text or ""),
        )

    # --- SLEEP ---
    @loader.command(
        en_doc="[time] — Enable SLEEP",
        ru_doc="[время] — Включить SLEEP",
        ua_doc="[час] — Увімкнути SLEEP",
    )
    async def sleep(self, message):
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
                logger.error(f"Не удалсь обновить статус: {e}")

        self._db.set(name, "sleep", True)
        self._db.set(name, "sleep_start", time.time())
        self._db.set(name, "wake_time", wake_time)
        self.answered_users.clear()
        self.chat_messages.clear()

        wake_text = self.config["MSG_WAKE_TIME"].format(wake_time) if wake_time else ""
        preview = self.config["MSG_SLEEP_REPLY"].format(
            was_online="Только что", wake_time=wake_text
        )

        await utils.answer(message, self.config["MSG_SLEEP_ON"] + preview)

    @loader.command(
        en_doc="Disable SLEEP",
        ru_doc="Выключить SLEEP",
        ua_doc="Вимкнути SLEEP",
    )
    async def unsleep(self, message):
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

        await utils.answer(
            message,
            self.config["MSG_SLEEP_OFF"] + duration_text + (log_text or ""),
        )

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
        """[save/load/del/list/pack] [название]"""
        args = utils.get_args_raw(message).split(maxsplit=1)
        action = args[0].lower() if args else "list"
        name_preset = args[1] if len(args) > 1 else None

        presets = self._db.get(name, "presets", {})

        if action == "save":
            if not name_preset:
                await utils.answer(message, "Укажите название пресета!")
                return
            current_preset_data = {
                key: self.config[key]
                for key in self.CONFIG_KEYS_TO_SAVE
                if key in self.config
            }
            presets[name_preset] = current_preset_data
            self._db.set(name, "presets", presets)
            await utils.answer(
                message, self.strings["preset_saved"].format(name_preset)
            )

        elif action == "load":
            if not name_preset:
                await utils.answer(message, "Укажите название пресета!")
                return
            if name_preset in presets:
                saved_data = presets[name_preset]
                for key, value in saved_data.items():
                    if key in self.config:
                        self.config[key] = value
                await utils.answer(
                    message, self.strings["preset_loaded"].format(name_preset)
                )
            else:
                await utils.answer(
                    message, self.strings["preset_not_found"].format(name_preset)
                )

        elif action == "del":
            if not name_preset:
                await utils.answer(message, "Укажите название пресета!")
                return
            if name_preset in presets:
                del presets[name_preset]
                self._db.set(name, "presets", presets)
                await utils.answer(
                    message, self.strings["preset_deleted"].format(name_preset)
                )
            else:
                await utils.answer(
                    message, self.strings["preset_not_found"].format(name_preset)
                )

        elif action == "pack":
            count = 0
            for pk_name, pk_data in self.PRESET_PACK.items():
                if pk_name not in presets:
                    presets[pk_name] = pk_data
                    count += 1
            if count > 0:
                self._db.set(name, "presets", presets)
            await utils.answer(message, self.strings["preset_pack_added"].format(count))

        else:  # list
            if not presets:
                await utils.answer(message, "Пресеты отсутствуют.")
                return
            res = self.strings["presets_list"]
            for p in presets:
                res += f"  <emoji document_id=5870695289714643076>👤</emoji> <code>{p}</code>\n"
            await utils.answer(message, res)

    # --- WATCHER ---
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

            if sleep_state:
                sleep_start = self._db.get(name, "sleep_start")
                diff_seconds = int(time.time() - sleep_start)
                if diff_seconds < 0:
                    diff_seconds = 0

                was_online = str(datetime.timedelta(seconds=diff_seconds))
                wake_time = self._db.get(name, "wake_time")
                text = self.config["MSG_SLEEP_REPLY"].format(
                    was_online=was_online,
                    wake_time=self.config["MSG_WAKE_TIME"].format(wake_time)
                    if wake_time
                    else "",
                )
            else:
                gone = self._db.get(name, "gone")
                diff_seconds = int(time.time() - gone)
                if diff_seconds < 0:
                    diff_seconds = 0

                was_online = str(datetime.timedelta(seconds=diff_seconds))
                reason = afk_state if isinstance(afk_state, str) else None
                return_time = self._db.get(name, "return_time")

                text = self.config["MSG_AFK_REPLY"].format(
                    was_online=was_online,
                    reason_text=(
                        f"<emoji document_id=5870729937215819584>⏰️</emoji> <b>Причина:</b> <i>{reason}</i>\n"
                        if reason
                        else ""
                    ),
                    come_time=(
                        f"<emoji document_id=5873146865637133757>🎤</emoji> <b>Прийду через:</b> <b>{return_time}</b>"
                        if return_time
                        else ""
                    ),
                )

            await utils.answer(message, text, reply_to=message)
