import asyncio
import datetime

from config import Config
import logging
import sqlite3
from contextlib import suppress
from aiogram.dispatcher.filters import CommandStart, BoundFilter, Command
from aiogram.types import BotCommandScopeDefault, BotCommand, InlineKeyboardButton, \
    InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from filters import AdminFilter
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from random import randint
import re
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import BadRequest

bot = Bot(token=Config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())


class AdminFilter(BoundFilter):
    async def check(self, message: types.Message):
        member = await message.chat.get_member(message.from_user.id)
        return member.is_chat_admin()


class IsGroup(BoundFilter):
    async def check(self, message: types.Message):
        return message.chat.type in (
            types.ChatType.GROUP,
            types.ChatType.SUPERGROUP,
        )


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        BotCommand('ro', 'Mode Read Only'),
        BotCommand('unro', 'Off RO'),
        BotCommand('ban', 'Ban user'),
        BotCommand('unban', 'Unban user')
    ])


@dp.message_handler(IsGroup(), Command('ban', prefixes='!/'), AdminFilter())
async def ban_user(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id
    await message.chat.kick(user_id=member_id)
    await message.reply(f'User {member.full_name} banned')


@dp.message_handler(IsGroup(), Command('unban', prefixes='!/'), AdminFilter())
async def unban_user(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id
    await message.chat.unban(user_id=member_id)
    await message.reply(f'User {member.full_name} was unbanned')
    servise_message = await message.reply('The message will be deleted after 5 seconds')
    await asyncio.sleep(5)
    await message.delete()
    await servise_message.delete()


@dp.message_handler(IsGroup(), Command('unro', prefixes='!/'), AdminFilter())
async def undo_read_only_mode(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id
    User_Allowed = types.ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_polls=True,
        can_pin_messages=False,
        can_invite_users=True,
        can_change_info=False,
        can_add_web_page_previews=True,
    )
    await message.chat.restrict(user_id=member_id, permissions=User_Allowed, until_date=0)
    await message.reply(f'User {member.full_name} was unbanned')
    servise_message = await message.reply('The message will be deleted after 5 seconds')
    await asyncio.sleep(5)
    await message.delete()
    await servise_message.delete()


@dp.message_handler(IsGroup(), Command('ro', prefixes='!/'), AdminFilter())
async def read_only_mode(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id
    command_parse = re.compile(r'(!ro|/ro)?(\d+)??([a-zA-Z])+?')
    print(message.text)
    parsed = command_parse.match(message.text)
    time = parsed.group(2)
    comment = parsed.group(3)
    if not time:
        time = 5
    else:
        time = int(time)
    until_date = datetime.datetime.now() + datetime.timedelta(minutes=time)
    ReadOnlyPermission = types.ChatPermissions(
        can_send_messages=False,
        can_send_media_messages=False,
        can_send_polls=False,
        can_pin_messages=False,
        can_invite_users=True,
        can_change_info=False,
        can_add_web_page_previews=False,
    )
    try:
        await bot.restrict_chat_member(chat_id, user_id=member_id, permissions=ReadOnlyPermission,
                                       until_date=until_date)
        await message.answer(f'To the user{member.get_mention(as_html=True)} '
                             f'it is forbidden to write for {time} minutes because of {comment}')
    except BadRequest:
        await message.answer('The user is an administrator')
        servise_message = await message.reply('The message will be deleted after 5 seconds')
        await asyncio.sleep(5)
        await message.delete()
        await servise_message.delete()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=set_default_commands)
