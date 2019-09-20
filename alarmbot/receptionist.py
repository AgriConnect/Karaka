from logbook import Logger
from aiogram import types

from .common import bot, dp, i18n
from .models import User


logger = Logger(__name__)
_ = i18n.gettext


@dp.message_handler()
async def salute(message: types.Message):
    user = message.from_user
    mesg = _('Hello {name}. This is AgriConnect. '
             'From now on you will receive alarm about your farm condition.')
    await bot.send_message(message.chat.id, mesg.format(name=user.first_name))
    # Store user info
    logger.info('Telegram username: {}, ID {}', user.username, user.id)
    if user.username:
        u, created = await User.get_or_create(username=user.username)
        u.telegram_id = user.id
    else:
        u, created = await User.get_or_create(telegram_id=user.id)
    u.first_name = user.first_name
    u.last_name = user.last_name
    u.language_code = user.language_code
    await u.save()
