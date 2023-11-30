
from .. import loader, utils
import asyncio
import random
import json

def register(cb):
    cb(VampModule())

class VampModule(loader.Module):
    """Vamp Userbot Module"""
    strings = {"name": "VampModule"}

    async def client_ready(self, client, db):
        self.db = db
        self.client = client
        self.vamp_templates = db.get("VampModule", "templates", [])

    async def idcmd(self, message):
        """Получить ID текущего чата."""
        await utils.answer(message, f"ID этого чата: {message.chat_id}")

    async def vampcmd(self, message):
        """Активирует режим вампира."""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "Неверные аргументы.")
            return
        try:
            chat_id, timing, header = args.split(maxsplit=2)
            timing = int(timing) * 60
        except ValueError:
            await utils.answer(message, "Ошибка в аргументах.")
            return

        while True:
            message = random.choice(self.vamp_templates)
            await self.client.send_message(chat_id, f"{header}\n\n{message}")
            await asyncio.sleep(timing)

    async def vampshbcmd(self, message):
        """Показать список доступных шаблонов или установить шаблон."""
        args = utils.get_args_raw(message)
        if args:
            try:
                selected_index = int(args) - 1
                if 0 <= selected_index < len(self.vamp_templates):
                    await utils.answer(message, f"Шаблон {selected_index + 1} выбран.")
                else:
                    await utils.answer(message, "Неверный номер шаблона.")
            except ValueError:
                await utils.answer(message, "Неверный формат номера шаблона.")
        else:
            response = "\n".join(f"{i+1}. {template}" for i, template in enumerate(self.vamp_templates))
            await utils.answer(message, response or "Список шаблонов пуст.")

    async def vaddshabcmd(self, message):
        """Добавить новые шаблоны."""
        reply = await message.get_reply_message()
        if reply and reply.file and reply.file.mime_type == 'text/plain':
            try:
                content = await reply.download_media(bytes)
                new_templates = content.decode('utf-8').split('\n')
                self.vamp_templates.extend(new_templates)
                self.db.set("VampModule", "templates", self.vamp_templates)
                await utils.answer(message, "Шаблоны добавлены.")
            except Exception as e:
                await utils.answer(message, f"Ошибка при добавлении шаблонов: {e}")

    async def vamphelpcmd(self, message):
        """Показать справку по модулю."""
        help_text = """
<b>Vamp Userbot Help Guide</b>
<i>Here's what I can do:</i>

<b>.id</b>
- Получить ID текущего чата.

<b>.vamp [chat_id] [timing] [header]</b>
- Активирует режим вампира...

<b>.vampshb [номер]</b>
- Показать список доступных шаблонов...

<b>.vaddshab</b>
- Добавить новые шаблоны...

<i>Разработчик:</i> @vampUB
<i>Поддержите разработку, подписавшись на канал:</i> https://t.me/bzrkrshop
"""
        await utils.answer(message, help_text)
