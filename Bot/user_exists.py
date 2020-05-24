from telebot import TeleBot
from telebot.types import Message


class IncorrectBotObject(Exception):
    pass


class IncorrectUserObject(Exception):
    pass


class ExistChecker:
    def __call__(self, bot, user_object):
        if isinstance(bot, TeleBot):
            if isinstance(user_object, int):
                try:
                    user = bot.get_chat_member(user_object, user_object).user
                    if user is not None:
                        return True
                except Exception:
                    pass
                return False
            elif isinstance(user_object, Message):
                try:
                    user = bot.get_chat_member(user_object.chat.id, user_object.chat.id).user
                    if user is not None:
                        return True
                except Exception:
                    pass
                return False
            else:
                raise IncorrectUserObject(f'user_object must be <int> or <Message> got: {type(user_object)}')
        else:
            raise IncorrectBotObject(f'bot must be <TeleBot> got: {type(bot)}')
