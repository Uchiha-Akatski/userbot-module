from .. import loader

# meta developer: @Itachi_Uchiha_sss

@loader.tds
class Memprikol2(loader.Module):
    """Голосовые сообщения  Mempack№2"""

    strings = {"name": " Memprikol2"}

    async def счастливыеcmd(self, message):
        """| Счастливые? Счастливые мрази"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/186",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def хуевоcmd(self, message):
        """| Хуево денег нет"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/187",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def ещёразcmd(self, message):
        """| Ещё раз позвонишь"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/189",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def тычтоcmd(self, message):
        """| Ты что творишь?"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/203",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def агаcmd(self, message):
        """| Ага так и поверил"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/204",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def гг2cmd(self, message):
        """| Гг мы вьебали"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/205",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def ауеcmd(self, message):
        """| Утро в хату мужики"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/206",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def анлакcmd(self, message):
        """| Анлак анлак"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/207",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def факаcmd(self, message):
        """| Факамазафака"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/208",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def мотивацияcmd(self, message):
        """| Мотивация должен быть всегда"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/209",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def чиназаcmd(self, message):
        """| Чиназес нах"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/210",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def плакиcmd(self, message):
        """| Плаки плаки"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/211",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def помогcmd(self, message):
        """| Эх, если б кто помог"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/212",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def отсосиcmd(self, message):
        """| Магическое заклинание"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/213",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def силаcmd(self, message):
        """| Ахх Египетская сила"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/214",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def блятьcmd(self, message):
        """| Блять ебать мой хуй"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/215",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def смех3cmd(self, message):
        """| Смех"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/216",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def конченаяcmd(self, message):
        """| Вы шо конченая"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/217",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def шашлындосcmd(self, message):
        """| Шашлындос"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/218",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def ахуеюcmd(self, message):
        """| Ахуею жестко"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/219",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def наебаловоcmd(self, message):
        """| Эта круговое наебалово"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/220",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def нахерcmd(self, message):
        """| А нахер ты все это помнишь?"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/221",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def томозcmd(self, message):
        """| Томоз"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/222",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def порноcmd(self, message):
        """| Там что порно?"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/223",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def дорогойcmd(self, message):
        """| ДОРОГОЙ ГДЕ ТЫ БЫЛ?"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/224",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def заёбываюcmd(self, message):
        """| Я людей заёбываю"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/225",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def опятьcmd(self, message):
        """| ШО опять?"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/226",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def виталяcmd(self, message):
        """| Виталя"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/227",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def жратьcmd(self, message):
        """| Хочу жрать"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/228",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def хлебcmd(self, message):
        """| ГАЛЯ ХЛЕБ"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/229",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def жрать2cmd(self, message):
        """| Нужно нажраться"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/230",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def тыменяcmd(self, message):
        """| Ты меня даже не слушаешь"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/231",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def чтозаcmd(self, message):
        """| Ну что ты за человек такой"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/232",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def малышcmd(self, message):
        """| Ну чё малыш атакуй"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/233",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def долбаёбcmd(self, message):
        """| Ты долбаёб"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/234",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def побухаемcmd(self, message):
        """| Чё может побухаем?"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/235",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def осуждаюcmd(self, message):
        """| Да я осуждаю"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/236",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def закройтеcmd(self, message):
        """| Закройте хлебало чтобы не поддувало"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/237",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def мать3cmd(self, message):
        """| Хорошая женщина"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/238",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def житьcmd(self, message):
        """| Пожить пожить"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/239",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def геддауннcmd(self, message):
        """| Узнаете"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/240",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def кометcmd(self, message):
        """| 100 комет мне в жопу"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/241",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def водаcmd(self, message):
        """| Пошла вода горячая"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/242",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def нахуй4cmd(self, message):
        """| Пошёл нахуй(ver Zubarev)"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/243",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def шансcmd(self, message):
        """| Это наш шанс это наш наш"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/244",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def проебалиcmd(self, message):
        """| АААААААААА всё проебали"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/245",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def рыбаcmd(self, message):
        """| Я рыба"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/246",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
    
    async def химияcmd(self, message):
        """| Очень крутая химия"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/273",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def бэмcmd(self, message):
        """| бэм бэм бэм"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/329",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def даданетнетcmd(self, message):
        """| Да да нет нет да будет свет"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/341",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def изибриджиcmd(self, message):
        """| Изи бриджи изи бриджи"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/331",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def пенисыcmd(self, message):
        """| не буду я смотреть на ваши ПЕНИСЫЫЫЫЫЫ"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/332",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def инфузорияcmd(self, message):
        """| ТЫ БЕЗМОЗГЛАЯ ИНФУЗОРИЯ РАЗДУДОТОЕ САМОМНЕНИЕМ"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/333",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def фуфуфуcmd(self, message):
        """| Эта опять он? Фу фу фу"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/gachi_mych/334",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
