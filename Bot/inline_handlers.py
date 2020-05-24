from telebot.types import CallbackQuery
from JsonGetter import JSON
from re import search
from Database import get_user, update_user, del_user, PermissionChecker, del_events_for_a_day, del_event, get_event,\
    update_event
from Bot import ExistChecker, is_confirmed, true_weekday, INLINE_SUPERUSER_MARKUP, INLINE_ADMIN_MARKUP
from Unix import UnixTimeConverter


config_getter = JSON()
_, SUPERUSER_ID, *_ = config_getter()
is_exist = ExistChecker()
is_has_permission = PermissionChecker()
unix_converter = UnixTimeConverter()


# checked---------------------------------------------------------------------------------------------------------------
def update_event_handler(bot, call):
    def update_one_event_text_next_step_handler(unix, weekday, groups, content):
        for_admins, for_pdts, for_promotions = False, False, False
        if 'admin' in groups:
            for_admins = True
        if 'pdt' in groups:
            for_pdts = True
        if 'promotion' in groups:
            for_promotions = True
        update_event(unix, weekday, content.chat.id, content.message_id, for_admins, for_pdts, for_promotions)
        bot.reply_to(content, f"Событие на {weekday} обновлено/добавлено.\n"
                              f"Событие предназначено для групп:\n"
                              f"Admins: {for_admins}\n"
                              f"PDTs: {for_pdts}\n"
                              f"Subscriptions: {for_promotions}", parse_mode="html")

    def update_one_event_group_next_step_handler(unix, weekday, groups):
        groups = groups.text.lower()
        if 'admin' in groups or 'pdt' in groups or 'promotion' in groups:
            get_content_msg = bot.send_message(call.message.chat.id, f"Отправьте контент:",
                                               parse_mode="html")
            bot.register_next_step_handler(get_content_msg,
                                           lambda content: update_one_event_text_next_step_handler(unix, weekday,
                                                                                                   groups, content))
        else:
            bot.send_message(call.message.chat.id, "Групп(а/ы) пользователей указаны некоректно!", parse_mode="html")

    def update_one_event_time_next_step_handler(time, weekday):
        unix = unix_converter(time.text, without_exceptions=True)
        if unix is not None:
            get_group_msg = bot.send_message(call.message.chat.id, f"Выберите группу для данного события:\n"
                                                                   f"Пример:\n"
                                                                   f"admin/pdt/promotion",
                                             parse_mode="html")
            bot.register_next_step_handler(get_group_msg,
                                           lambda group: update_one_event_group_next_step_handler(unix, weekday, group))
        else:
            bot.send_message(call.message.chat.id, "Время указано некоректно!", parse_mode="html")

    def update_one_event_next_step_handler(weekday):
        weekday = true_weekday(weekday.text)
        if weekday is not None:
            update_time_msg = bot.send_message(call.message.chat.id, "Введите время события:",
                                               parse_mode="html")
            bot.register_next_step_handler(update_time_msg,
                                           lambda time: update_one_event_time_next_step_handler(time, weekday))
        else:
            bot.send_message(call.message.chat.id, "Некорректно указан день недели!", parse_mode="html")

    update_day_msg = bot.send_message(call.message.chat.id,
                                      "Введите день недели для создания/обновления события в нем:",
                                      parse_mode="html")
    bot.register_next_step_handler(update_day_msg, update_one_event_next_step_handler)


# checked---------------------------------------------------------------------------------------------------------------
def del_one_event_handler(bot, call):
    def del_one_event_time_next_step_handler(time, weekday):
        unix = unix_converter(time.text, without_exceptions=True)
        if unix is not None:
            event = get_event(unix, weekday)
            if event is None:
                bot.send_message(call.message.chat.id, f"Событие запланированное на {time.text} {weekday} не найдено!",
                                 parse_mode="html")
            else:
                del_event(unix, weekday)
                bot.send_message(call.message.chat.id, f"Событие запланированное на {time.text} {weekday} удалено!",
                                 parse_mode="html")
        else:
            bot.send_message(call.message.chat.id, "Время указано некоректно!", parse_mode="html")

    def del_one_event_next_step_handler(weekday):
        weekday = true_weekday(weekday.text)
        if weekday is not None:
            del_time_msg = bot.send_message(call.message.chat.id, "Введите время события которое хотите удалить:",
                                            parse_mode="html")
            bot.register_next_step_handler(del_time_msg, lambda time: del_one_event_time_next_step_handler(time,
                                                                                                           weekday))
        else:
            bot.send_message(call.message.chat.id, "Некорректно указан день недели!", parse_mode="html")

    del_day_msg = bot.send_message(call.message.chat.id, "Введите день недели для удаления события в нем:",
                                   parse_mode="html")
    bot.register_next_step_handler(del_day_msg, del_one_event_next_step_handler)


# checked---------------------------------------------------------------------------------------------------------------
def del_day_handler(bot, call):
    def del_day_next_step_handler(weekday):
        weekday = true_weekday(weekday.text)
        if weekday is not None:
            confirmation_handler(bot, call, lambda: del_events_for_a_day(weekday),
                                 f'<b>Все события на {weekday} удалены!</b>')
        else:
            bot.send_message(call.message.chat.id, "Некорректно указан день недели!", parse_mode="html")

    del_day_msg = bot.send_message(call.message.chat.id, "Введите день недели для удаления всех событий в нем:",
                                   parse_mode="html")
    bot.register_next_step_handler(del_day_msg, del_day_next_step_handler)


# checked---------------------------------------------------------------------------------------------------------------
def confirmation_handler(bot, call, func, confirmed_title: str):
    def confirmation_next_step_handler(confirm_message):
        if is_confirmed(confirm_message.text):
            func()
            bot.send_message(call.chat.id, confirmed_title, parse_mode="html")
        else:
            bot.send_message(call.chat.id, "Действие отменено", parse_mode="html")

    if isinstance(call, CallbackQuery):
        call = call.message
    confirm_msg = bot.send_message(call.chat.id, "Вы уверены??? [Y/N]", parse_mode="html")
    bot.register_next_step_handler(confirm_msg, confirmation_next_step_handler)


# checked---------------------------------------------------------------------------------------------------------------
def update_user_handler(bot, call, need_del_user=False):
    def update_user_next_step_handler(user_id_message):
        user_id = search(r'\d+', user_id_message.text)
        if user_id is not None:
            user_id = int(user_id.group())
            if is_exist(bot, user_id):
                user = get_user(user_id)
                if user is None:
                    update_user(user_id, False, False, False, 0)
                    user = get_user(user_id)
                    bot.send_message(call.message.chat.id, 'Пользователь успешко добавлен в БД!!!', parse_mode="html")
                user_name = bot.get_chat_member(user_id, user_id).user.first_name
                if call.message.chat.id == SUPERUSER_ID:
                    if user_id == SUPERUSER_ID:
                        bot.send_message(call.message.chat.id, f'<b>Суперпользователь не может редактировать свои '
                                                               f'права</b>\n'
                                                               f'(они обновляются при запуске бота!!!)',
                                         parse_mode="html")
                    else:
                        bot.send_message(call.message.chat.id, f'Отредактируйте права доступа пользователя:\n'
                                                               f'Имя пользователя: {user_name}\n'
                                                               f'ID пользователя: {user_id}\n'
                                                               f'<b>Действующие права сейчас:</b>\n'
                                                               f'Admin: {user.is_admin}\n'
                                                               f'PDT: {user.is_pdt}\n'
                                                               f'Subscription: {user.is_promotion}\n'
                                                               f'Subscription days left: {user.subscription}',
                                         reply_markup=INLINE_SUPERUSER_MARKUP,
                                         parse_mode="html")
                else:
                    bot.send_message(call.message.chat.id, f'Отредактируйте права доступа пользователя:\n'
                                                           f'Имя пользователя: {user_name}\n'
                                                           f'ID пользователя: {user_id}\n'
                                                           f'<b>Действующие права сейчас:</b>\n'
                                                           f'PDT: {user.is_pdt}\n'
                                                           f'Subscription: {user.is_promotion}\n'
                                                           f'Subscription days left: {user.subscription}',
                                     reply_markup=INLINE_ADMIN_MARKUP,
                                     parse_mode="html")
            else:
                bot.send_message(call.message.chat.id, 'Пользователя с таким ID не существует во всем Телеграме!!!',
                                 parse_mode="html")
        else:
            bot.send_message(call.message.chat.id, 'Некорректное ID пользователя!!!', parse_mode="html")

    def del_user_next_step_handler(user_id_message):
        user_id = search(r'\d+', user_id_message.text)
        if user_id is not None:
            user_id = int(user_id.group())
            user = get_user(user_id)
            if user is None:
                bot.send_message(call.message.chat.id, 'Пользователя с данным ID нет в БД!!!', parse_mode="html")
            else:
                if call.message.chat.id == user_id:
                    bot.send_message(call.message.chat.id, 'Вы не можете удалить себя!!!', parse_mode="html")
                elif call.message.chat.id == SUPERUSER_ID:
                    confirmation_handler(bot, call, lambda: del_user(user.user_id), 'Пользователь удален!!!')
                elif user_id == SUPERUSER_ID:
                    bot.send_message(call.message.chat.id, 'Вы не можете удалить суперпользователя!!!',
                                     parse_mode="html")
                elif is_has_permission(user_id, is_admin=True):
                    bot.send_message(call.message.chat.id, 'Будучи администратором, '
                                                           'вы не можете удалить другого администратора!!!',
                                     parse_mode="html")
                else:
                    confirmation_handler(bot, call, lambda: del_user(user.user_id), 'Пользователь удален!!!')
        else:
            bot.send_message(call.message.chat.id, 'Некорректное ID пользователя!!!', parse_mode="html")

    next_handler = del_user_next_step_handler if need_del_user else update_user_next_step_handler
    get_user_id_msg = bot.send_message(call.message.chat.id, 'Введите ID пользователя:', parse_mode="html")
    bot.register_next_step_handler(get_user_id_msg, next_handler)


# checked---------------------------------------------------------------------------------------------------------------
def permissions_edit_handler(bot, call, role):
    user_id = search(r'(?<=ID пользователя: )\d+', call.message.text)
    user_id = int(user_id.group())
    user = get_user(user_id)
    if user is not None:
        user_name = bot.get_chat_member(user_id, user_id).user.first_name
        setattr(user, role, not getattr(user, role))
        subscription = user.subscription
        if role == 'is_promotion':
            subscription = 30 if user.is_promotion else 0
        update_user(user.user_id, user.is_admin, user.is_pdt, user.is_promotion, subscription)
        if call.message.chat.id == SUPERUSER_ID:
            bot.edit_message_text(f'Отредактируйте права доступа пользователя:\n'
                                  f'Имя пользователя: {user_name}\n'
                                  f'ID пользователя: {user_id}\n'
                                  f'<b>Действующие права сейчас:</b>\n'
                                  f'Admin: {user.is_admin}\n'
                                  f'PDT: {user.is_pdt}\n'
                                  f'Subscription: {user.is_promotion}\n'
                                  f'Subscription days left: {subscription}',
                                  chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="html",
                                  reply_markup=INLINE_SUPERUSER_MARKUP)
        else:
            bot.edit_message_text(f'Отредактируйте права доступа пользователя:\n'
                                  f'Имя пользователя: {user_name}\n'
                                  f'ID пользователя: {user_id}\n'
                                  f'<b>Действующие права сейчас:</b>\n'
                                  f'PDT: {user.is_pdt}\n'
                                  f'Subscription: {user.is_promotion}\n'
                                  f'Subscription days left: {subscription}',
                                  chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="html",
                                  reply_markup=INLINE_ADMIN_MARKUP)
    else:
        bot.send_message(call.message.chat.id, 'Данного пользователя уже не существует в БД!!!', parse_mode="html")


# checked---------------------------------------------------------------------------------------------------------------
def send_users_by_category_handler(bot, call, func, title: str):
    users = func()
    if len(users):
        users_str = f'<b>{title}:</b>\n'
        users_str += '\n'.join([f'NAME: '
                                f'{bot.get_chat_member(user.user_id, user.user_id).user.first_name} '
                                f'ID: {user.user_id}' for user in users])
        bot.send_message(call.message.chat.id, users_str, parse_mode="html")
    else:
        bot.send_message(call.message.chat.id, "У вас нет ни одного пользователя в этой категории!",
                         parse_mode="html")
