from time import sleep
from datetime import datetime, timezone, timedelta
from Database import get_event, get_all_users, del_event
from Unix import UnixTimeConverter


unix_converter = UnixTimeConverter()


def event_mainloop(bot):
    try:
        while True:
            UTC = timezone(timedelta(hours=+3))
            time = datetime.now(UTC)
            unix = unix_converter(f'{time.hour}:{time.minute}')
            weekday = time.strftime('%A').lower()
            event = get_event(unix, weekday)
            if event is not None:
                all_users = get_all_users()
                admins = tuple(filter(lambda user: user.is_admin, all_users))
                pdts = tuple(filter(lambda user: user.is_pdt, all_users))
                promotions = tuple(filter(lambda user: user.is_promotion, all_users))
                if event.for_admins:
                    for admin in admins:
                        bot.forward_message(admin.user_id, event.chat_id, event.message_id)
                if event.for_pdts:
                    for pdt in pdts:
                        bot.forward_message(pdt.user_id, event.chat_id, event.message_id)
                if event.for_promotions:
                    for promotion in promotions:
                        bot.forward_message(promotion.user_id, event.chat_id, event.message_id)
                del_event(unix, weekday)
            sleep(60)
    except Exception as error:
        print(error)
