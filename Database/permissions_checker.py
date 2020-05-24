from telebot.types import Message
from Database import get_user


class InvalidParams(Exception):
    pass


class EmptyArgsParams(Exception):
    pass


class EmptyKwArgsParams(Exception):
    pass


class PermissionChecker:
    def __call__(self, *args, **kwargs):
        if len(args):
            if len(kwargs):
                if isinstance(args[0], int):
                    user = get_user(args[0])
                    if user is not None:
                        result = list()
                        for kwarg in kwargs:
                            result.append(getattr(user, kwarg) == kwargs[kwarg])
                        return len(kwargs) == sum(result)
                    return False
                elif isinstance(args[0], Message):
                    user = get_user(args[0].chat.id)
                    if user is not None:
                        result = list()
                        for kwarg in kwargs:
                            result.append(getattr(user, kwarg) == kwargs[kwarg])
                        return min(result)
                    return False
                raise InvalidParams(f'incorrect params | got type: {type(args[0])}')
            raise EmptyKwArgsParams("you don't given kwargs in function")
        raise EmptyArgsParams("you don't given args in function")
