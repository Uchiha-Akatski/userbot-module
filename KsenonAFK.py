# meta developer: @Itachi_Uchiha_sss

from .. import loader, utils
from telethon import types, functions
import time
import datetime
import logging
from collections import defaultdict

__version__ = (1, 8, 1)

name = "KsenonAFK"
logger = logging.getLogger(name)

@loader.tds
class KsenonAFKMod(loader.Module):
    """Универсальный AFK/SLEEP модуль с подсчётом времени и премиум-статусами."""

    strings = {
        "name": "KsenonAFK",
        "gone": "<emoji document_id=5870948572526022116>✋</emoji> <b>Сейчас я в AFK-режиме</b>\n<emoji document_id=5870695289714643076>👤</emoji> <b>Был в сети:</b> Только что\n<emoji document_id=5870729937215819584>⏰️</emoji> <b>Ушёл по причине:</b> <i>{}</i>",
        "back": "<emoji document_id=5883964170268840032>👤</emoji> <b>Больше не в режиме AFK.</b>",
        "default_afk_message": "<emoji document_id=5870948572526022116>✋</emoji> <b>Сейчас я в AFK-режиме</b>\n<emoji document_id=5870695289714643076>👤</emoji> <b>Был в сети:</b> {was_online} назад\n{reason_text}{come_time}",
        "sleep_on": "<emoji document_id=5870729937215819584>💤</emoji> <b>SLEEP-режим включён!</b>\n<emoji document_id=5873146865637133757>😴</emoji> <b>KsenonAFK будет отвечать этим сообщением:</b>\n\n",
        "sleep_msg": "<emoji document_id=5870729937215819584>💤</emoji> <b>Сейчас я в Sleep-режиме</b>\n<emoji document_id=5877700484453634587>🌙</emoji> <b>Не беспокоить, я сплю</b>\n<emoji document_id=5870695289714643076>👤</emoji> <b>Был в сети:</b> {was_online} назад\n{wake_time}",
        "wake_text": "<emoji document_id=5873146865637133757>🎤</emoji> <b>Проснусь в:</b> <b>{}</b>",
        "sleep_off": "<emoji document_id=5883964170268840032>👤</emoji> <b>Проснулся, Sleep-режим отключён.</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue("setPremiumStatus", True, lambda: "Ставить премиум-статус при AFK/SLEEP.", validator=loader.validators.Boolean()),
            loader.ConfigValue("customEmojiStatus", 4969889971700761796, lambda: "Кастомный премиум-статус для AFK.", validator=loader.validators.Integer()),
            loader.ConfigValue("customSleepEmojiStatus", 5229252352948379900, lambda: "Кастомный премиум-статус для SLEEP.", validator=loader.validators.Integer()),
        )
        self.answered_users = set()
        self.chat_messages = defaultdict(list)
        self._old_status = None

    async def client_ready(self, client, db):
        self._db = db
        self._me = await client.get_me()
        self.client = client

    async def safe_get_user(self, message):
        try:
            return await self.client.get_entity(message.sender_id)
        except Exception:
            return None

    # --- AFK ---
    @loader.command(ru_doc="[причина] [время] - Установить режим AFK")
    async def afk(self, message):
        args = utils.get_args_raw(message)
        reason = None
        time_val = None

        if args:
            parts = args.split(" ", 1)
            if len(parts) > 1:
                reason, time_val = parts
            else:
                reason = parts[0]

        if self.config["setPremiumStatus"]:
            try:
                me = await self.client.get_me()
                if me.emoji_status:
                    self._old_status = me.emoji_status
                await self.client(functions.account.UpdateEmojiStatusRequest(
                    emoji_status=types.EmojiStatus(document_id=self.config["customEmojiStatus"])
                ))
            except Exception as e:
                logger.error(f"Не удалось обновить эмодзи-статус: {e}")

        self._db.set(name, "afk", reason or True)
        self._db.set(name, "gone", time.time())
        self._db.set(name, "return_time", time_val)
        self.answered_users.clear()

        preview = self.strings["default_afk_message"].format(
            was_online="Только что",
            reason_text=f"<emoji document_id=5870729937215819584>⏰️</emoji> <b>Причина:</b> <i>{reason}</i>\n" if reason else "",
            come_time=f"<emoji document_id=5873146865637133757>🎤</emoji> <b>Прийду через:</b> <b>{time_val}</b>" if time_val else ""
        )
        preview_message = "<emoji document_id=5870730156259152122>😀</emoji> <b>AFK-режим включён!</b>\n<emoji document_id=5877700484453634587>✈️</emoji> <b>KsenonAFK будет отвечать этим сообщением:</b>\n\n"
        await utils.answer(message, preview_message + preview)

    @loader.command(ru_doc="Выйти из режима AFK")
    async def unafk(self, message):
        self._db.set(name, "afk", False)
        self._db.set(name, "gone", None)
        self._db.set(name, "return_time", None)
        self.answered_users.clear()

        if self.config["setPremiumStatus"] and self._old_status:
            try:
                await self.client(functions.account.UpdateEmojiStatusRequest(emoji_status=self._old_status))
            except Exception as e:
                logger.error(f"Не удалось восстановить эмодзи-статус: {e}")

        await utils.answer(message, self.strings["back"])

    # --- SLEEP ---
    @loader.command(ru_doc="[время] - Установить режим SLEEP (без причины)")
    async def sleep(self, message):
        args = utils.get_args_raw(message)
        wake_time = args if args else None

        if self.config["setPremiumStatus"]:
            try:
                me = await self.client.get_me()
                if me.emoji_status:
                    self._old_status = me.emoji_status
                await self.client(functions.account.UpdateEmojiStatusRequest(
                    emoji_status=types.EmojiStatus(document_id=self.config["customSleepEmojiStatus"])
                ))
            except Exception as e:
                logger.error(f"Не удалось обновить эмодзи-статус: {e}")

        self._db.set(name, "sleep", True)
        self._db.set(name, "sleep_start", time.time())
        self._db.set(name, "wake_time", wake_time)
        self.answered_users.clear()

        wake_text = self.strings["wake_text"].format(wake_time) if wake_time else ""
        now_text = "Только что"
        preview = self.strings["sleep_msg"].format(was_online=now_text, wake_time=wake_text)
        await utils.answer(message, self.strings["sleep_on"] + preview)

    @loader.command(ru_doc="Выключить режим SLEEP")
    async def unsleep(self, message):
        self._db.set(name, "sleep", False)
        self._db.set(name, "sleep_start", None)
        self._db.set(name, "wake_time", None)
        self.answered_users.clear()

        if self.config["setPremiumStatus"] and self._old_status:
            try:
                await self.client(functions.account.UpdateEmojiStatusRequest(emoji_status=self._old_status))
            except Exception as e:
                logger.error(f"Не удалось восстановить эмодзи-статус: {e}")

        await utils.answer(message, self.strings["sleep_off"])

    # --- Watcher ---
    async def watcher(self, message):
        if not isinstance(message, types.Message):
            return

        if message.mentioned or getattr(message.to_id, "user_id", None) == self._me.id:
            afk_state = self._db.get(name, "afk", False)
            sleep_state = self._db.get(name, "sleep", False)

            if not afk_state and not sleep_state:
                return

            user = await self.safe_get_user(message)

            if not user or getattr(user, "is_self", False) or getattr(user, "bot", False) or getattr(user, "verified", False):
                return

            if user.id in self.answered_users:
                return

            self.answered_users.add(user.id)
            now = datetime.datetime.now().replace(microsecond=0)
            text = None

            if sleep_state:
                sleep_start = self._db.get(name, "sleep_start")
                if sleep_start:
                    diff = now - datetime.datetime.fromtimestamp(sleep_start).replace(microsecond=0)
                    was_online = str(diff)
                else:
                    was_online = "давно"

                wake_time = self._db.get(name, "wake_time", None)
                wake_text = self.strings["wake_text"].format(wake_time) if wake_time else ""
                text = self.strings["sleep_msg"].format(was_online=was_online, wake_time=wake_text)

            elif afk_state:
                gone = datetime.datetime.fromtimestamp(self._db.get(name, "gone")).replace(microsecond=0)
                diff = now - gone
                return_time = self._db.get(name, "return_time", None)
                reason = afk_state if isinstance(afk_state, str) else None

                text = self.strings["default_afk_message"].format(
                    was_online=str(diff),
                    reason_text=f"<emoji document_id=5870729937215819584>⏰️</emoji> <b>Причина:</b> <i>{reason}</i>\n" if reason else "",
                    come_time=f"<emoji document_id=5873146865637133757>🎤</emoji> <b>Прийду через:</b> <b>{return_time}</b>" if return_time else ""
                )

            if text:
                await utils.answer(message, text, reply_to=message)