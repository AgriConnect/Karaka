from urllib.parse import urljoin

from logbook import Logger
from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from .consts import WEBHOOK_PATH, BASE_WEBHOOK_URL
from .conf import config
from .common import i18n_middleware
from .models import User


logger = Logger(__name__)
router = Router()
router.message.middleware(i18n_middleware)


@router.message()
async def salute(message: Message):
    user = message.from_user
    if not user:
        # Message from a channel, no need to reply.
        return
    logger.info('Got message from Telegram user {}.', user.username)
    mesg = _('Hello {name}. This is AgriConnect. '
             'From now on you will receive alarm about your farm condition.')
    await message.answer(mesg.format(name=user.first_name))
    # Store user info
    logger.info('Telegram username: {}, ID {}', user.username, user.id)
    if user.username:
        u, created = await User.get_or_create(username=user.username)
        u.telegram_id = user.id
    else:
        u, created = await User.get_or_create(telegram_id=user.id)
    u.first_name = user.first_name
    if user.last_name:
        u.last_name = user.last_name
    u.language_code = user.language_code or 'en-US'
    await u.save()


async def on_startup(bot: Bot):
    url = urljoin(BASE_WEBHOOK_URL, WEBHOOK_PATH)
    await bot.set_webhook(url, secret_token=config.WEBHOOK_SECRET)
    logger.info('Set webhook {} for bot', url)
