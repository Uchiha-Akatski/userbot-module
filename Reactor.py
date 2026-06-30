#
#   ██╗████████╗ █████╗  ██████╗██╗  ██╗██╗
#   ██║╚══██╔══╝██╔══██╗██╔════╝██║  ██║██║
#   ██║   ██║   ███████║██║     ███████║██║
#   ██║   ██║   ██╔══██║██║     ██╔══██║██║
#   ██║   ██║   ██║  ██║╚██████╗██║  ██║██║
#   ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝
# Original developer: @undef1n3dd
# The rights to this module were kindly transferred by the original author


# meta developer: @Itachi_Uchiha_sss

import asyncio
import re

from .. import loader, utils

from legacytl.types import Message
from legacytl.tl.functions.messages import SendReactionRequest
from legacytl.tl.types import (
    ReactionEmoji,
    ReactionCustomEmoji,
    MessageEntityCustomEmoji
)


@loader.tds
class ReactorMod(loader.Module):
    """Модуль для реакций"""
    strings = {
        "name": "Reactor",
        "_cfg_silent": "React silently",
        "incorrect_format": "<emoji document_id=5881702736843511327>⚠️</emoji> <b>Incorrect format</b>",
        "reaction_added": "<emoji document_id=5776375003280838798>✅</emoji><b> Reaction</b> <code>{}</code> <b>with emoji</b> <code>{}</code> <b>successfully added</b>",
        "reaction_removed": "<emoji document_id=5879896690210639947>🗑</emoji> <b>Reaction</b> <code>{}</code> <b>removed</b>",
        "not_found": "<emoji document_id=6037243349675544634>👁</emoji> <b>Reaction</b> <code>{}</code> <b>not found</b>",
        "no_reply": "<emoji document_id=5879813604068298387>❗️</emoji> <b>Reply to message</b>",
        "reactions_list": "<emoji document_id=5766994197705921104>🗂</emoji> <b>List of available reactions:</b>\n\n{}",
        "done": "<emoji document_id=5776375003280838798>✅</emoji> <b>Done</b>"
    }

    strings_ru = {
        "_cfg_silent": "Молча отреагировать",
        "incorrect_format": "<emoji document_id=5881702736843511327>⚠️</emoji> <b>Неправильный формат</b>",
        "reaction_added": "<emoji document_id=5776375003280838798>✅</emoji><b> Реакция</b> <code>{}</code> <b>с эмоджи</b> <code>{}</code> <b>успешно добавлена</b>",
        "reaction_removed": "<emoji document_id=5879896690210639947>🗑</emoji> <b>Реакция</b> <code>{}</code> <b>удалена</b>",
        "not_found": "<emoji document_id=6037243349675544634>👁</emoji> <b>Реакция</b> <code>{}</code> <b>не найдена</b>",
        "no_reply": "<emoji document_id=5879813604068298387>❗️</emoji> <b>Ответьте на сообщение</b>",
        "reactions_list": "<emoji document_id=5766994197705921104>🗂</emoji> <b>Список доступных реакций:</b>\n\n{}",
        "done": "<emoji document_id=5776375003280838798>✅</emoji> <b>Готово</b>"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "silent",
                False,
                lambda: self.strings("_cfg_silent"),
                validator=loader.validators.Boolean(),
            ),
        )

    async def client_ready(self, client, _):
        self._client = client
        self.reactions = self.get("reactions", {})

    def _message_text(self, message: Message) -> str:
        return (
            getattr(message, "text", None)
            or getattr(message, "raw_text", None)
            or getattr(message, "message", None)
            or ""
        )

    def _iter_custom_emoji(self, message: Message, min_offset: int = 0):
        entities = getattr(message, "entities", None) or []
        return [
            entity
            for entity in sorted(entities, key=lambda item: item.offset)
            if isinstance(entity, MessageEntityCustomEmoji) and entity.offset >= min_offset
        ]

    def _is_emoji_token(self, token: str) -> bool:
        return any(
            0x1F000 <= ord(char) <= 0x1FAFF
            or 0x2600 <= ord(char) <= 0x27BF
            for char in token
        )

    def _strip_emoji_chars(self, token: str) -> str:
        return "".join(
            char
            for char in token
            if not (
                0x1F000 <= ord(char) <= 0x1FAFF
                or 0x2600 <= ord(char) <= 0x27BF
                or ord(char) == 0xFE0F
            )
        )

    def _clean_reaction_name_token(self, token: str) -> str:
        token = re.sub(r"<[^>]*>", "", token)
        token = re.sub(r"document_id=\d+", "", token)
        token = self._strip_emoji_chars(token)
        return token.strip(" ,;:|")

    def _normalize_reaction_value(self, value):
        if isinstance(value, str) and value.isdigit():
            return int(value)

        return value

    def _reaction_values_from_message(self, message: Message, min_offset: int = 0):
        text = self._message_text(message)
        custom_entities = self._iter_custom_emoji(message, min_offset)
        custom_spans = [
            (entity.offset, entity.offset + entity.length)
            for entity in custom_entities
        ]
        values = [(entity.offset, entity.document_id) for entity in custom_entities]

        offset = min_offset
        for token in text[min_offset:].split():
            start = text.find(token, offset)
            end = start + len(token)
            offset = end

            if any(start < span_end and end > span_start for span_start, span_end in custom_spans):
                continue

            if self._is_emoji_token(token):
                values.append((start, token))

        return [value for _, value in sorted(values, key=lambda item: item[0])]

    def _parse_custom_emoji_pairs(self, message: Message):
        custom_emojis = self._iter_custom_emoji(message)

        if not custom_emojis:
            return [], []

        names = [
            name
            for name in (
                self._clean_reaction_name_token(token)
                for token in utils.get_args(message)
            )
            if name
            and not name.isdigit()
            and not name.lower().startswith(("docum", "emoji"))
            and "document" not in name.lower()
            and "emoji" not in name.lower()
        ]

        return names[:len(custom_emojis)], [entity.document_id for entity in custom_emojis]

    def _parse_addreact_args(self, message: Message, raw_args: str):
        args = utils.get_args(message)

        if "|" in args:
            pipe_index = args.index("|")
            names = args[:pipe_index]
            emoji_args = args[pipe_index + 1:]
            pipe_offset = self._message_text(message).find("|")
            custom_emojis = [
                entity.document_id
                for entity in self._iter_custom_emoji(message, pipe_offset + 1)
            ]

            emojis = custom_emojis if len(custom_emojis) == len(names) else emoji_args
            return names, [self._normalize_reaction_value(emoji) for emoji in emojis]

        names, custom_emojis = self._parse_custom_emoji_pairs(message)
        if custom_emojis and len(names) == len(custom_emojis):
            return names, custom_emojis

        if len(args) == 2:
            return [args[0]], [self._normalize_reaction_value(args[1])]

        if len(args) < 2 or len(args) % 2:
            return [], []

        names = args[::2]
        custom_emojis = [
            entity.document_id
            for entity in self._iter_custom_emoji(message)
        ]

        emojis = custom_emojis if len(custom_emojis) == len(names) else args[1::2]

        return names, [self._normalize_reaction_value(emoji) for emoji in emojis]

    @loader.command(en_doc="- Add reaction [name | emoji] (e.g. .addreact like 👍 | .addreact like fire sad | 👍 🔥 😢 | .addreact like fire sad 👍 🔥 😢)",ru_doc="- Добавить реакцию [имя | реакция] (например: .addreact like 👍 | .addreact like fire sad | 👍 🔥 😢 | .addreact like fire sad 👍 🔥 😢)")
    async def addreact(self, message: Message):
        raw_args = " ".join(utils.get_args(message))

        if not raw_args:
            await utils.answer(message, self.strings("incorrect_format"))
            return

        names, emojis = self._parse_addreact_args(message, raw_args)

        if not names or len(names) != len(emojis):
            await utils.answer(message, self.strings("incorrect_format"))
            return

        self.reactions.update(dict(zip(names, emojis)))
        self.set("reactions", self.reactions)

        await utils.answer(
            message,
            self.strings("reaction_added").format(", ".join(names), ", ".join(map(str, emojis))),
        )

    @loader.command(en_doc="- Remove reaction(s) [name1] [name2] ...\n",ru_doc="- Удалить реакцию(и) [имя1] [имя2] ...\n")
    async def delreact(self, message: Message):
        args = utils.get_args(message)

        if not args:
            await utils.answer(message, self.strings("incorrect_format"))
            return

        removed = []
        not_found = []

        for name in args:
            if name not in self.reactions:
                not_found.append(name)
                continue

            self.reactions.pop(name)
            removed.append(name)

        if removed:
            self.set("reactions", self.reactions)

        if not removed:
            await utils.answer(message, self.strings("not_found").format(", ".join(not_found)))
            return

        answer = self.strings("reaction_removed").format(", ".join(removed))

        if not_found:
            answer += "\n" + self.strings("not_found").format(", ".join(not_found))

        await utils.answer(message, answer)

    @loader.command(en_doc="- React to a message [name]", ru_doc="- Поставить реакции на сообщение [имя]")
    async def react(self, message: Message):
        args = utils.get_args(message)
        reply = await message.get_reply_message()

        if not args:
            await utils.answer(message, self.strings("incorrect_format"))
            return

        if not reply:
            await utils.answer(message, self.strings("no_reply"))
            return

        reactions = []

        for name in args[:3]:
            if name not in self.reactions:
                continue

            emoji = self.reactions[name]
            emoji = self._normalize_reaction_value(emoji)

            if isinstance(emoji, int):
                reactions.append(ReactionCustomEmoji(document_id=emoji))
            else:
                reactions.append(ReactionEmoji(emoticon=emoji))

        if not reactions:
            return

        await self._client(
            SendReactionRequest(
                peer=await self._client.get_input_entity(reply.peer_id),
                msg_id=reply.id,
                reaction=reactions
            )
        )

        if not self.config["silent"]:
            await utils.answer(message, self.strings("done"))

        await message.delete()


    @loader.command(en_doc="- List of available reactions", ru_doc="- Список доступных реакций")
    async def reactlist(self, message: Message):
        reactions_list = ''.join(f"<b>{k} |</b> {'<emoji document_id=' + str(v) + '>🙂</emoji>' if isinstance(v, int) else v}\n" for k, v in self.reactions.items()) if self.reactions else ''
        await utils.answer(message, self.strings("reactions_list").format(reactions_list))
