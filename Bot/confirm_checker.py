def is_confirmed(text: str):
    text = text.lower()
    confirm_list = ('✅', 'y', 'yes', 'да', 'согласен', 'подтверждаю', 'подтвердить')
    return text in confirm_list
