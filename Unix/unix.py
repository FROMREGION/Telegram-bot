from re import search
from datetime import datetime


class ConversionError(Exception):
    pass


class UnixTimeConverter:
    def __call__(self, *args, **kwargs):
        if len(args) == 1:
            if isinstance(args[0], int):
                return args[0] // 60, args[0] % 60
            elif isinstance(args[0], str):
                if args[0].isdigit():
                    value = int(args[0])
                    return value // 60, value % 60
                else:
                    time = search(r'^(([0,1]?[0-9])|(2?[0-3])):[0-5]?[0-9]', args[0])
                    if time is not None:
                        time = time.group().split(':')
                        return int(time[0]) * 60 + int(time[1])
        elif len(args) >= 2:
            result = self.__handler_for_two_arguments(args[0], args[1])
            if result is not None:
                return result
        elif len(kwargs) == 1:
            value = kwargs.get('unix')
            if value is not None:
                if isinstance(value, int):
                    return value // 60, value % 60
                elif isinstance(value, str):
                    if value.isdigit():
                        value = int(value)
                        return value // 60, value % 60
            else:
                value = kwargs.get('time')
                if value is not None:
                    time = search(r'^(([0,1]?[0-9])|(2?[0-3])):[0-5]?[0-9]', str(value))
                    if time is not None:
                        time = time.group().split(':')
                        return int(time[0]) * 60 + int(time[1])
        elif len(kwargs) >= 2:
            hours = kwargs.get('hour')
            minutes = kwargs.get('min')
            if hours is not None and minutes is not None:
                result = self.__handler_for_two_arguments(hours, minutes)
                if result is not None:
                    return result
        # exception handling
        if kwargs.get('without_exceptions'):
            return None
        raise ConversionError('failed to convert')

    # handler-----------------------------------------------------------------------------------------------------------
    @staticmethod
    def __handler_for_two_arguments(hours, minutes):
        if isinstance(hours, int) and isinstance(minutes, int):
            if 0 <= hours < 24 and 0 <= minutes < 60:
                return hours * 60 + minutes
        elif isinstance(hours, str) and isinstance(minutes, int):
            if hours.isdigit():
                hours = int(hours)
                if 0 <= hours < 24 and 0 <= minutes < 60:
                    return hours * 60 + minutes
        elif isinstance(hours, int) and isinstance(minutes, str):
            if minutes.isdigit():
                minutes = int(minutes)
                if 0 <= hours < 24 and 0 <= minutes < 60:
                    return hours * 60 + minutes
        elif isinstance(hours, str) and isinstance(minutes, str):
            if hours.isdigit() and minutes.isdigit():
                hours = int(hours)
                minutes = int(minutes)
                if 0 <= hours < 24 and 0 <= minutes < 60:
                    return hours * 60 + minutes


if __name__ == '__main__':
    obj = UnixTimeConverter()
    time = datetime.now()
    unix = obj(time.hour, time.minute)
    time_ = obj(unix)
    if time.hour == time_[0] and time.minute == time_[1]:
        print('test complete')
    else:
        raise Exception('Unit test was failed')
