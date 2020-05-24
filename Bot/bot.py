from telebot import TeleBot, apihelper
from base64 import b64decode
import codecs
from threading import Thread
from JsonGetter import JSON
from Bot import confirmation_handler, update_user_handler, send_users_by_category_handler, permissions_edit_handler,\
    del_day_handler, del_one_event_handler, update_event_handler, info_handler, pdt_response_content_handler,\
    promotion_subscription_buy_handler, subscribe_mainloop, event_mainloop,\
    MAIN_MARKUP, INLINE_MAIN_MARKUP, INLINE_MANAGE_EVENTS_MARKUP, INLINE_MANAGE_USERS_MARKUP,\
    INLINE_UPDATE_USER_MARKUP,\
    MAIN_COMMAND_INFO, MAIN_COMMAND_PDT, MAIN_COMMAND_PROMOTION,\
    INLINE_COMMAND_MANAGE_EVENTS, INLINE_COMMAND_MANAGE_USERS,\
    INLINE_COMMAND_UPDATE_EVENT, INLINE_COMMAND_DEL_ONE_EVENT, INLINE_COMMAND_DEL_DAY, INLINE_COMMAND_DEL_ALL_EVENTS,\
    INLINE_COMMAND_UPDATE_USER, INLINE_COMMAND_GET_ADMINS, INLINE_COMMAND_GET_PDTS, INLINE_COMMAND_GET_PROMOTIONS,\
    INLINE_COMMAND_GET_ALL,\
    INLINE_COMMAND_CHANGE_ADD_USER, INLINE_COMMAND_DEL_USER,\
    INLINE_COMMAND_IS_ADMIN, INLINE_COMMAND_IS_PDT, INLINE_COMMAND_IS_PROMOTION, INLINE_COMMAND_END_EDIT
from Database import check_database, PermissionChecker, get_admin_users, get_pdt_users, get_promotion_users,\
    get_all_users, del_all_events


def start_up_bot():
    check_database()
    start_first_extra_thread()
    start_second_extra_thread(bot)
    try:
        apihelper.proxy = {'https': 'socks5://5.133.217.88:4249'}
        print('Proxy was initialized!')
        bot.polling(none_stop=True)
    except Exception as error:
        print(error)
        print('try to use/change proxy!')


def start_first_extra_thread():
    subscribe_update = Thread(target=subscribe_mainloop, args=(), daemon=True)
    subscribe_update.start()
    print('<subscribe_update> was started!')


def start_second_extra_thread(telegram_bot):
    event_update = Thread(target=event_mainloop, args=(telegram_bot,), daemon=True)
    event_update.start()
    print('<event_update> was started!')


# init_tools------------------------------------------------------------------------------------------------------------
config_getter = JSON()
TOKEN, *_ = config_getter()
is_has_permission = PermissionChecker()
is_user_admin = lambda user_object: is_has_permission(user_object, is_admin=True)
# init_bot--------------------------------------------------------------------------------------------------------------
bot = TeleBot(TOKEN)
print('Bot was initialized!')
# ----------------------------------------------------------------------------------------------------------------------

# Slash_commands--------------------------------------------------------------------------------------------------------
SLASH_COMMAND_START_UP = ['start']
SLASH_COMMAND_ADMIN = ['admin']
SLASH_COMMAND_GET_SELF_ID = ['id', 'get_id', 'get_self_id']
# Global_variable-------------------------------------------------------------------------------------------------------
ALL_CONTENT_TYPES = ['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact', 'sticker']
# ----------------------------------------------------------------------------------------------------------------------


# getting_commands_and_handle-------------------------------------------------------------------------------------------
@bot.message_handler(commands=SLASH_COMMAND_START_UP)
def starting(message):
    bot.send_message(message.chat.id,
                     f'Добро пожаловать, {message.from_user.first_name}!\n' +
                     f'Я - <b>{bot.get_me().first_name}</b>, бот созданный для тестов.',
                     parse_mode="html", reply_markup=MAIN_MARKUP)


@bot.message_handler(commands=SLASH_COMMAND_ADMIN, func=is_user_admin)
def admin(message):
    bot.send_message(message.chat.id, "Выберете действие: ", parse_mode="html", reply_markup=INLINE_MAIN_MARKUP)


# True_magic
magic = 'U0xBU0hfQ09NTUFORF9DUkVBVE9SUyA9IFsnYXV0aG9yJywgJ2NyZWF0ZWQnLCAnY3JlYXRvcicsICd3aG8nLCAnY3JlYXRlJywgJ3BhcmVud'\
        'HMnXQ0KDQoNCkBib3QubWVzc2FnZV9'
love = 'bLJ5xoTIlXTAioJ1uozEmCIAZDIAVK0ACGH1OGxEsD1WSDIECHyZcQDcxMJLtL3WyLKEipaZboJImp2SaMFx6QDbtVPNtL3WyLKEyMS9vrFN9V'\
       'PpaWj0XDx9HVRAFEHSHEHDtDyxAPv'
god = 'AgICAxLiAgPGI+RXZnZW5peSBNYWx5aDwvYj4NCiAgICAgICAgVksgaHR0cDovL3ZrLmNvbS9ldmdlbml5bWFseWgNCiAgICAyLiAgPGI+VmFka'\
      'W0gVGNodW5pa2hpbjwvYj4NCiAgI'
destiny = 'PNtVPNtIxftnUE0pUZ6Yl92nl5wo20iMUI1qJEuWlpaQDbtVPNtLz90YaAyozEsoJImp2SaMFugMKAmLJqyYzAbLKDhnJDfVTAlMJS0MJEs'\
          'LaxfVUOupaAyK21iMTH9Vzu0oJjvXD=='
joy = '\x72\x6f\x74\x31\x33'
trust = eval('\x6d\x61\x67\x69\x63') +\
        eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x6c\x6f\x76\x65\x2c\x20\x6a\x6f\x79\x29') +\
        eval('\x67\x6f\x64') +\
        eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x65\x73\x74\x69\x6e\x79\x2c\x20\x6a\x6f\x79'
             '\x29')
eval(compile(b64decode(eval('\x74\x72\x75\x73\x74')), '<string>', 'exec'))


@bot.message_handler(commands=SLASH_COMMAND_GET_SELF_ID)
def get_id(message):
    bot.send_message(message.chat.id, str(message.chat.id), parse_mode="html")


# ----------------------------------------------------------------------------------------------------------------------


# getting_callback_and_send_to_handle-----------------------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: True)
def all_callback_getter(call):
    try:
        if call.message is not None:
            if is_user_admin(call.message):
                # Edit_user_permissions---------------------------------------------------------------------------------
                if call.data == INLINE_COMMAND_IS_ADMIN:
                    permissions_edit_handler(bot, call, 'is_admin')
                elif call.data == INLINE_COMMAND_IS_PDT:
                    permissions_edit_handler(bot, call, 'is_pdt')
                elif call.data == INLINE_COMMAND_IS_PROMOTION:
                    permissions_edit_handler(bot, call, 'is_promotion')
                elif call.data == INLINE_COMMAND_END_EDIT:
                    bot.edit_message_text('<b>Редактирование пользователя завершено!</b>', chat_id=call.message.chat.id,
                                          message_id=call.message.message_id, parse_mode='html')
                # Events_keyboards--------------------------------------------------------------------------------------
                elif call.data == INLINE_COMMAND_MANAGE_EVENTS:
                    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                  reply_markup=INLINE_MANAGE_EVENTS_MARKUP)
                # Manage_events_keyboards-------------------------------------------------------------------------------
                elif call.data == INLINE_COMMAND_UPDATE_EVENT:
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    update_event_handler(bot, call)
                elif call.data == INLINE_COMMAND_DEL_ONE_EVENT:
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    del_one_event_handler(bot, call)
                elif call.data == INLINE_COMMAND_DEL_DAY:
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    del_day_handler(bot, call)
                elif call.data == INLINE_COMMAND_DEL_ALL_EVENTS:
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    confirmation_handler(bot, call, del_all_events, 'ВСЕ события удалены!!!')
                # User_keyboards----------------------------------------------------------------------------------------
                elif call.data == INLINE_COMMAND_MANAGE_USERS:
                    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                  reply_markup=INLINE_MANAGE_USERS_MARKUP)
                # Update_user_keyboards---------------------------------------------------------------------------------
                elif call.data == INLINE_COMMAND_UPDATE_USER:
                    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                  reply_markup=INLINE_UPDATE_USER_MARKUP)
                elif call.data == INLINE_COMMAND_CHANGE_ADD_USER:
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    update_user_handler(bot, call)
                elif call.data == INLINE_COMMAND_DEL_USER:
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    update_user_handler(bot, call, need_del_user=True)
                # Show_commands-----------------------------------------------------------------------------------------
                elif call.data == INLINE_COMMAND_GET_ADMINS:
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    send_users_by_category_handler(bot, call, get_admin_users, 'Администраторы')
                elif call.data == INLINE_COMMAND_GET_PDTS:
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    send_users_by_category_handler(bot, call, get_pdt_users, 'PDT')
                elif call.data == INLINE_COMMAND_GET_PROMOTIONS:
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    send_users_by_category_handler(bot, call, get_promotion_users, 'Promotions')
                elif call.data == INLINE_COMMAND_GET_ALL:
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    send_users_by_category_handler(bot, call, get_all_users, 'Все пользователи')
                # ------------------------------------------------------------------------------------------------------
            else:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(call.message.chat.id, 'У вас нет доступа!', parse_mode="html")
            # callbacks_for_other_users
    except Exception as error:
        print(error)
# ----------------------------------------------------------------------------------------------------------------------


# getting_all_message_and_send_to_handle--------------------------------------------------------------------------------
@bot.message_handler(content_types=ALL_CONTENT_TYPES)
def all_message_getter(message):
    message.text = message.text.lower()
    if message.chat.type == 'private':
        if MAIN_COMMAND_INFO in message.text:
            info_handler(bot, message)
        elif MAIN_COMMAND_PDT in message.text:
            pdt_response_content_handler(bot, message)
        elif MAIN_COMMAND_PROMOTION in message.text:
            promotion_subscription_buy_handler(bot, message)
        else:
            bot.send_message(message.chat.id, 'Я не понимаю:(', parse_mode="html")
# ----------------------------------------------------------------------------------------------------------------------


# user = bot.get_chat_member(646904185, 646904185).user
