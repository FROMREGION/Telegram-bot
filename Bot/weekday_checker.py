def true_weekday(text):
    text = str(text).lower()
    weekday_dict = {
        'monday': 'monday', 'понедельник': 'monday', 'пн': 'monday', '1': 'monday',
        'tuesday': 'tuesday', 'вторник': 'tuesday', 'вт': 'tuesday', '2': 'tuesday',
        'wednesday': 'wednesday', 'среда': 'wednesday', 'ср': 'wednesday', '3': 'wednesday',
        'thursday': 'thursday', 'четверг': 'thursday', 'чт': 'thursday', '4': 'thursday',
        'friday': 'friday', 'пятница': 'friday', 'пт': 'friday', '5': 'friday',
        'saturday': "saturday", 'суббота': 'saturday', 'сб': 'saturday', '6': 'saturday',
        'sunday': 'sunday', 'воскресенье': 'sunday', 'вс': 'sunday', '7': 'sunday'}
    return weekday_dict.get(text)
