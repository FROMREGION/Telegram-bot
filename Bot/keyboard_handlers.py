from Bot import ExistChecker, confirmation_handler
from Database import get_user, update_user, PermissionChecker, get_admin_users
from JsonGetter import JSON

from telebot.types import LabeledPrice, PreCheckoutQuery
from re import search

is_has_permission = PermissionChecker()
is_exist = ExistChecker()

config_getter = JSON()
_, _, PAYMENTS_PROVIDER_TOKEN, PROMOTION_SUBSCRIPTION_TITLE, PROMOTION_SUBSCRIPTION_DESCRIPTION, PRICE = config_getter()
PROMOTION_SUBSCRIPTION_PRICE = LabeledPrice(label='Promotion subscribe price', amount=PRICE)
REFFERAL_DICT = dict()

def info_handler(bot, message):
    with open('info_message.txt', 'r', encoding='UTF-8') as file:
        info = file.read()
    bot.send_message(message.chat.id, info, parse_mode="html")

# ----------------------------------------------------------------------------------------------------------------------


def pdt_response_content_handler(bot, message):
    def pdt_response_content_next_step_handler(content):
        def send_to_admins(content_message):
            for admin in get_admin_users():
                bot.forward_message(admin.user_id, content_message.chat.id, content_message.message_id)

        confirmation_handler(bot, content, lambda: send_to_admins(content), 'Ответ отправлен!')

    if is_has_permission(message.chat.id, is_pdt=True) or is_has_permission(message.chat.id, is_admin=True):
        get_response_msg = bot.send_message(message.chat.id, 'Отправьте работу:', parse_mode="html")
        bot.register_next_step_handler(get_response_msg, pdt_response_content_next_step_handler)
    else:
        bot.send_message(message.chat.id, 'У вас нет доступа!', parse_mode="html")


# ----------------------------------------------------------------------------------------------------------------------


def promotion_subscription_buy_handler(bot, message):

    @bot.pre_checkout_query_handler(func=lambda query: True)
    def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
        bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

    @bot.message_handler(content_types=['successful_payment'])
    def successful_payment(message):
        bot.send_message(message.chat.id, 'Ваш платеж успешно дошел, спасибо за оплату подписки!')
        user_id = message.chat.id
        user = get_user(user_id)
        if user is None:
            subscription_message = '<b>Подписка активирована.</b>'
            update_user(user_id, False, False, True, 30)
        else:
            subscription_message = '<b>Подписка продлена.</b>'
            update_user(user_id, user.is_admin, user.is_pdt, True, 30)
        bot.send_message(user_id, f'{subscription_message} \nДо окончания подписки: 30 дней', parse_mode="html")

        who_user = bot.get_chat_member(user_id, user_id).user
        if REFFERAL_DICT.get(user_id) is None:
            for admin in get_admin_users():
                bot.send_message(admin.user_id, 
                                 f'<b>После перезапуска бота не удалось получить информацию: </b>\n'
                                 f'<b>Пользователь:</b>\n'
                                 f'ID: {user_id}\n'
                                 f'Username: {who_user.username}\n'
                                 '--------------------\n'
                                 f'<b>Пришел от:</b> \n'
                                 f'ID: [undefined] \n'
                                 f'Username: [undefined]',
                                 parse_mode="html")
        else:
            reff_user = bot.get_chat_member(REFFERAL_DICT[user_id], REFFERAL_DICT[user_id]).user
            for admin in get_admin_users():
                bot.send_message(admin.user_id, f'<b>Пользователь:</b>\n'
                                                f'ID: {user_id}\n'
                                                f'Username: {who_user.username}\n'
                                                '--------------------\n'
                                                f'<b>Пришел от:</b> \n'
                                                f'ID: {REFFERAL_DICT.get(user_id)} \n'
                                                f'Username: {reff_user.username}',
                                 parse_mode="html")
            del REFFERAL_DICT[user_id]
    # ----------------------------------------------------------------------------------------------------------

    def promotion_subscribe_buy_next_step_handler(reff_id_message, message):
        reff_id = search(r'\d+', reff_id_message.text)
        if reff_id is not None:
            reff_id = int(reff_id.group())
            if is_exist(bot, reff_id):
                if reff_id == reff_id_message.chat.id:
                    bot.send_message(reff_id_message.chat.id, 'Вы не можете указать себя в качестве реферала!',
                                     parse_mode="html")
                else:
                    bot.send_invoice(chat_id=message.chat.id,
                                     title=PROMOTION_SUBSCRIPTION_TITLE,
                                     description=PROMOTION_SUBSCRIPTION_DESCRIPTION,
                                     invoice_payload='successful',
                                     provider_token=PAYMENTS_PROVIDER_TOKEN,
                                     start_parameter='payment-promotion-subscribe',
                                     currency='RUB',
                                     prices=[PROMOTION_SUBSCRIPTION_PRICE]
                                     )
                    REFFERAL_DICT[message.chat.id] = reff_id
            else:
                bot.send_message(reff_id_message.chat.id, 'Пользователя с таким ID не существует во всем Телеграме!!!',
                                 parse_mode="html")
        else:
            bot.send_message(reff_id_message.chat.id, 'Некорректное ID пользователя!!!', parse_mode="html")

    if is_has_permission(message.chat.id, is_promotion=True):
        user = get_user(message.chat.id)
        bot.send_message(message.chat.id, f'<b>У вас уже есть подписка.</b> \nДо окончания, '
                                          f'осталось дней: {user.subscription}', parse_mode="html")
    else:
        get_promotion_reff_msg = bot.send_message(message.chat.id, 'Укажите ID пользователя от которого вы пришли',
                                                  parse_mode="html")
        bot.register_next_step_handler(get_promotion_reff_msg,
                                       lambda reff_id: promotion_subscribe_buy_next_step_handler(reff_id, message))
