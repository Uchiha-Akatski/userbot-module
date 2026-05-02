from .. import loader

# meta developer: @Itachi_Uchiha_sss

@loader.tds
class Postal2(loader.Module):
    """Войс пак с игры Postal2(от @Itachi_Uchiha_sss)"""

    strings = {"name": " Postal2"}

    async def петицияcmd(self, message):
        """| Вы не могли бы подписать мою петицию?"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/403",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def петиция2cmd(self, message):
        """| Подпиши мою петицию, чёрт возьми!"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/404",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def петиция3cmd(self, message):
        """| Послушай, просто подпиши эту дурацкую петицию. Времени мало у меня, понимаешь?"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/405",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def петиция4cmd(self, message):
        """| Подпиши эту петицию, или я пойду к тебе домой и убью твою собаку!"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/406",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def петиция5cmd(self, message):
        """| Ты подпишешь эту петицию, или это придется делать выжившим членам твоей семьи?"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/407",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def мамочкаcmd(self, message):
        """| Ой, мамочка!"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/408",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def головаcmd(self, message):
        """| Ой, моя голова"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/409",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def божеcmd(self, message):
        """| (Смех) Боже"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/410",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def не2cmd(self, message):
        """| А я так не думаю"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/411",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def деньгиcmd(self, message):
        """| Вот всегда мне не хватает денег"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/412",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def чампиcmd(self, message):
        """| О, вот он. Сюда, Чампи. Ко мне"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/413",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def деньги2cmd(self, message):
        """| Давайте мне деньги"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/414",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def одинcmd(self, message):
        """| И ещё один"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/415",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def не3cmd(self, message):
        """| И почему это меня не удивляет?"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/416",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def извиниcmd(self, message):
        """| Извини"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/417",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def извинитеcmd(self, message):
        """| Извините, у меня что-то с нервами. Сегодня не в порядке"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/418",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def радостьcmd(self, message):
        """| Радость"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/419",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def хочетсяcmd(self, message):
        """| Как же хочется отлить"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/420",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def привет2cmd(self, message):
        """| Привет"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/421",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def тычёcmd(self, message):
        """| Ты что, опять сохраняешься?"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/422",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def тюрьмаcmd(self, message):
        """| Ах, тюрьма. Небольшой рай, запятнанный мочой. Рай для гомосексуалистов"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/423",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def праваcmd(self, message):
        """| У меня есть право на продажу прав на свои книги, у меня есть право на продажу прав на свои видео, у меня есть право на агента"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/424",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def закон2cmd(self, message):
        """| Я закон"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/425",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def закон3cmd(self, message):
        """| Я верю, что закон будет на моей стороне, и меня освободят"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/426",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def зналcmd(self, message):
        """| Я знал"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/427",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def купитьcmd(self, message):
        """| Я могу купить это"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/428",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def грешник2cmd(self, message):
        """| Благослови меня, отче, я сильно согрешил, очень сильно. Не, я не шучу, я большой грешник, да"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/429",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def бомжcmd(self, message):
        """| Ой, бог мой, я стал бомжом"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/430",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def кретинcmd(self, message):
        """| Какой кретин придумал это?"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/431",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def круто2cmd(self, message):
        """| Эх, круто!"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/432",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def готоваcmd(self, message):
        """| Готова"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/433",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def делоcmd(self, message):
        """| И еще одно дело сделано"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/434",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def ломкаcmd(self, message):
        """| Ай! Как я не люблю ломку!"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/435",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def дерьмуcmd(self, message):
        """| Ах! К этому дерьму так быстро привыкаешь!"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/436",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def ещеcmd(self, message):
        """| Мне определенно нужно еще"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/437",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def ломка2cmd(self, message):
        """| Ооо! Какая ломка!"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/438",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def куритьcmd(self, message):
        """| Я знал, что не стоило курить. Это дерьмо"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/439",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def дерьмовоcmd(self, message):
        """| Я чувствую себя дерьмово"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/440",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def шутишьcmd(self, message):
        """| Ты, должно быть, вот так неудачно шутишь, да?"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/441",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
