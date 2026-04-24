from .. import loader

# meta developer: @Itachi_Uchiha_sss

@loader.tds
class Sasavotpack(loader.Module):
    """Голосовые от Sasavota"""

    strings = {"name": "Sasavotpack"}

    async def вернитоликаcmd(self, message):
        """| Верни мне толика"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/325",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def похуйcmd(self, message):
        """| ОХУЕТЬ ЕБАТЬ ВСЕМ ПОХУЙ"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/326",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def занятонахcmd(self, message):
        """| ЗАНЯТО НАХУЙ"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/327",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def осуждаю2cmd(self, message):
        """| Осуждаю от Sasavota"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/328",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
        
    async def танецcmd(self, message):
        """| Курский танцор"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/394",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
