from .. import loader

# meta developer: @Itachi_Uchiha_sss

@loader.tds
class StariyBog(loader.Module):
    """Голосовые сообщения StariyBog"""

    strings = {"name": "StariyBog"}

    async def кулизеcmd(self, message):
        """| Привет Лизе, королево кого, чего?"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/299",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def сыншлюхиcmd(self, message):
        """| Бля походу я сын шлюхи"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/300",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def вахуеcmd(self, message):
        """| Та я в ахуе"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/301",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def закройсяcmd(self, message):
        """| Та закрой своё ебало"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/302",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def яйцаcmd(self, message):
        """| Ты видишь какие у меня огромные яйца? ЙОУ"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/303",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def вовчикcmd(self, message):
        """| Та какой вовчик ну нахуя"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/304",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def старыйбогcmd(self, message):
        """| СТАРЫЙ БОГ"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/305",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def питонаcmd(self, message):
        """| Старый бог ебал питона"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/306",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def СУПcmd(self, message):
        """| Супа нет вкуснее борща старый бог ебал...."""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/307",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def анекдотcmd(self, message):
        """| Анекдот от Старого Бога"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/308",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def старыйбог2cmd(self, message):
        """| Старый бог2"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/309",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def языкбогаcmd(self, message):
        """| Язык старого бога"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/310",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def крик3cmd(self, message):
        """| Крик от старого бога"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/311",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def йоуcmd(self, message):
        """| ЙОУ"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/312",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def лошадьcmd(self, message):
        """| Ебаная лошадь"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/313",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def шлюхаcmd(self, message):
        """| Ладно у него просто мать шлюха"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/314",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return 
    async def небудетcmd(self, message):
        """| Не будет лазеров из глаз, громов над головой"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/342",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    async def птичкиcmd(self, message):
        """| Что ты сказал? Зверя нет сильнее птички, старый бог сломал яички"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/374",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return   
    async def соситcmd(self, message):
        """|  Зверя нет сильнее китайца, старый бог с осином яйца"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/375",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return   
    async def натураcmd(self, message):
        """| Натура от старого бога"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/376",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return   
    async def завались4cmd(self, message):
        """| Ебало завали(Старый кок)"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/377",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return   
