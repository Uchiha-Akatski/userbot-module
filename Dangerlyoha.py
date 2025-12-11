from .. import loader

# meta developer: @Itachi_Uchiha_sss

@loader.tds
class Dangerlyoha(loader.Module):
    """Голосовые сообщения от Dangerlyoha"""

    strings = {"name": "Dangerlyoha"}

    async def долбаёб2cmd(self, message):
        """| По моим под счётом ты долбаёб"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/294",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def кенгуруcmd(self, message):
        """| Кенгуру ебучие"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/295",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def неcmd(self, message):
        """| Не говори ничего про маму"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/296",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def кенгуру2cmd(self, message):
        """| Маму за уши и получался кенгуру"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/297",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def варинтыcmd(self, message):
        """| 4 варианта"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/298",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return