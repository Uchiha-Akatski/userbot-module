# meta developer: @Itachi_Uchiha_sss

from .. import loader, utils
from telethon import types, functions
import time
import datetime
import logging
from collections import defaultdict

__version__ = (1, 8, 5)

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
        )

        self.answered_users = set()
        # user_id -> {"name": str, "count": int}
        self.chat_messages = defaultdict(lambda: {"name": "", "count": 0})
        self._old_status = None

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
                f'(<code>{user_id}</code>) — <b>{count}</b> сообщений'
            )

        return (
            "\n\n<blockquote>"
            "<b>Пока тебя не было, тебе писали:</b>\n"
            + "\n".join(lines)
            + "</blockquote>"
        )


    # --- AFK ---
    @loader.command(ru_doc="[причина] | [время] — Установить AFK")
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

        preview = self.strings["default_afk_message"].format(
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

    @loader.command(ru_doc="Отключить AFK")
    async def unafk(self, message):
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

        await utils.answer(message, self.strings["back"] + (log_text or ""))

    # --- SLEEP ---
    @loader.command(ru_doc="[время] — Включить SLEEP")
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

        wake_text = (
            self.strings["wake_text"].format(wake_time) if wake_time else ""
        )
        preview = self.strings["sleep_msg"].format(
            was_online="Только что", wake_time=wake_text
        )

        await utils.answer(message, self.strings["sleep_on"] + preview)

    @loader.command(ru_doc="Выключить SLEEP")
    async def unsleep(self, message):
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

        await utils.answer(message, self.strings["sleep_off"] + (log_text or ""))

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
                text = self.strings["sleep_msg"].format(
                    was_online=was_online,
                    wake_time=self.strings["wake_text"].format(wake_time)
                    if wake_time
                    else "",
                )
            else:
                now = datetime.datetime.now().replace(microsecond=0)
                gone = datetime.datetime.fromtimestamp(self._db.get(name, "gone"))
                diff = now - gone
                reason = afk_state if isinstance(afk_state, str) else None
                return_time = self._db.get(name, "return_time")

                text = self.strings["default_afk_message"].format(
                    was_online=str(diff).split(".")[0],
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
