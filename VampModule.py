
from telethon import events, sync
from telethon.tl.functions.messages import ImportChatInviteRequest
import random
import asyncio

# Инициализация глобальных переменных
vamp_templates = []  # Список шаблонов для команды vamp
current_template = 0  # Текущий выбранный шаблон

# Команда .id - Получение ID чата
@client.on(events.NewMessage(pattern=r'\.id', outgoing=True))
async def send_chat_id(event):
    await event.reply(f"Chat ID: {event.chat_id}")

# Команда .vamp - Отправка рандомных сообщений
@client.on(events.NewMessage(pattern=r'\.vamp (\d+) (\d+) (.+)', outgoing=True))
async def vamp_command(event):
    chat_id, timing, header = event.pattern_match.groups()
    timing = int(timing)
    while True:
        message = header + "
" + random.choice(vamp_templates[current_template])
        await client.send_message(int(chat_id), message)
        await asyncio.sleep(timing)

# Команда .vampshb - Вывод шаблонов и выбор шаблона
@client.on(events.NewMessage(pattern=r'\.vampshb( \d+)?', outgoing=True))
async def vampshb_command(event):
    global current_template
    num = event.pattern_match.group(1)
    if num:
        current_template = int(num.strip()) - 1
        await event.reply(f"Шаблон номер {current_template + 1} выбран.")
    else:
        templates_list = "
".join([f"{i+1}. {tpl}" for i, tpl in enumerate(vamp_templates)])
        await event.reply(f"Шаблоны:
{templates_list}")

# Команда .vaddshab - Добавление шаблона
@client.on(events.NewMessage(pattern=r'\.vaddshab', outgoing=True))
async def vaddshab_command(event):
    if event.reply_to_msg_id:
        reply_msg = await event.get_reply_message()
        if reply_msg.file:
            content = await reply_msg.download_media(bytes)
            vamp_templates.append(content.decode('utf-8').split('
'))
            await event.reply("Шаблон добавлен.")
        else:
            await event.reply("Ответьте на текстовый файл.")
    else:
        await event.reply("Используйте команду в ответ на текстовый файл.")

# Команда .vamphelp - Вывод помощи по модулю
@client.on(events.NewMessage(pattern=r'\.vamphelp', outgoing=True))
async def vamphelp_command(event):
    help_message = "Тут будет красивый гид по командам модуля."
    await event.reply(help_message, file='path_to_premium_sticker')

# Команда .vphoto - Изменение фото в гиде
@client.on(events.NewMessage(pattern=r'\.vphoto', outgoing=True))
async def vphoto_command(event):
    if event.reply_to_msg_id:
        reply_msg = await event.get_reply_message()
        if reply_msg.photo:
            # Логика изменения фото в гиде
            pass
        else:
            await event.reply("Ответьте на сообщение с фото.")
    else:
        await event.reply("Используйте команду в ответ на сообщение с фото.")

# Автоподписка на канал разработчика при установке модуля
@client.on(events.NewMessage(pattern=r'\.start', outgoing=True))
async def start_command(event):
    try:
        await client(ImportChatInviteRequest('bzrkrshop'))
        await event.reply("Вы подписались на канал разработчика.")
    except Exception as e:
        await event.reply(str(e))

# Здесь может быть дополнительный код для управления модулем, обработки исключений и т.д.

