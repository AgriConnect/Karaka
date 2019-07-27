from logbook import Logger
from aiogram import types

from .common import bot, dp
from .models import User


logger = Logger(__name__)


@dp.message_handler(commands=['chao'])
async def salute(message: types.Message):
    user = message.from_user
    bot.send_message(message.chat.id, f'Xin chao {user.username}')


@dp.message_handler(regexp='(^cat[s]?$|puss)')
async def cats(message: types.Message):
    with open('data/cats.jpg', 'rb') as photo:
        await bot.send_photo(message.chat.id, photo, caption='Cats is here 😺',
                             reply_to_message_id=message.message_id)


@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.chat.id, message.text)
    user = message.from_user
    logger.info('{} {}', user.username, user.id)
    u, created = await User.get_or_create(tg_userid=user.id)
    u.tg_username = user.username
    await u.save()
    logger.info('{}', list(await User.all()))
    await bot.send_message('323686876', f'You are {user.full_name}?')
