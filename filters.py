from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from config import Config


class AdminFilter(BoundFilter):
    async def check(self, message: types.Message):
        member = str(message.from_user.id)
        return member in Config.SUPER_USER_IDS
