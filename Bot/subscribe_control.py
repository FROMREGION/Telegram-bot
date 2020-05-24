from time import sleep
from Database import update_subscription_days


def subscribe_mainloop():
    try:
        while True:
            update_subscription_days()
            sleep(86400)
    except Exception as error:
        print(error)
