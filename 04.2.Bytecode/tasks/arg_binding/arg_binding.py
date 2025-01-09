from types import FunctionType
from typing import Any, Dict, List

# Константы для флагов функции
CO_VARARGS = 4
CO_VARKEYWORDS = 8

# Сообщения об ошибках
ERR_TOO_MANY_POS_ARGS = 'Слишком много позиционных аргументов'
ERR_TOO_MANY_KW_ARGS = 'Слишком много именованных аргументов'
ERR_MULT_VALUES_FOR_ARG = 'Несколько значений для аргумента'
ERR_MISSING_POS_ARGS = 'Отсутствуют позиционные аргументы'
ERR_MISSING_KWONLY_ARGS = 'Отсутствуют именованные аргументы'
ERR_POSONLY_PASSED_AS_KW = 'Позиционный аргумент передан как именованный'


def bind_args(func: FunctionType, *args: Any, **kwargs: Any) -> Dict[str, Any]:
    """Привязывает значения из `args` и `kwargs` к соответствующим аргументам функции `func`.

    :param func: функция, которую необходимо проанализировать
    :param args: позиционные аргументы для привязки
    :param kwargs: именованные аргументы для привязки
    :return: `dict[argument_name] = argument_value`, если привязка прошла успешно,
             вызывает TypeError с одним из описаний ошибки ERR_* в противном случае
    """
    # Получаем объект кода функции
    code = func.__code__

    # Получаем имена параметров функции
    params = code.co_varnames[:code.co_argcount]

    # Количество аргументов, которые можно передать только позиционно
    posonly_count = code.co_posonlyargcount

    # Получаем значения по умолчанию для параметров
    defaults = func.__defaults__ or ()
    defaults_offset = len(params) - len(defaults)  # Смещение для значений по умолчанию

    # Количество именованных аргументов
    kwonlyargcount = code.co_kwonlyargcount
    kwonly_params = code.co_varnames[code.co_argcount:code.co_argcount + kwonlyargcount]
    kwonly_defaults = func.__kwdefaults__ or {}

    # Словарь для привязанных аргументов
    bound_dict: Dict[str, Any] = {}
    pos_args_count = len(params)  # Общее количество позиционных аргументов

    # Проверка на слишком много позиционных аргументов для функций без *args
    if len(args) > pos_args_count and not (code.co_flags & CO_VARARGS):
        raise TypeError(ERR_TOO_MANY_POS_ARGS)

    # Привязываем позиционные аргументы (включая позиционные-only)
    for i, param in enumerate(params):
        # Проверяем, что позиционный-only аргумент не передан как именованный
        if i < posonly_count and param in kwargs and not (code.co_flags & CO_VARKEYWORDS):
            raise TypeError(ERR_POSONLY_PASSED_AS_KW)

        # Если есть переданный позиционный аргумент
        if i < len(args):
            bound_dict[param] = args[i]  # Привязываем аргумент из args
            if i >= posonly_count and param in kwargs:
                raise TypeError(ERR_MULT_VALUES_FOR_ARG)  # Проверка на множественные значения для одного аргумента
        # Если аргумент передан через kwargs
        elif param in kwargs and i >= posonly_count:
            bound_dict[param] = kwargs[param]  # Привязываем значение из kwargs
            kwargs.pop(param)  # Убираем привязанный аргумент из kwargs
        elif i >= defaults_offset:
            # Привязываем аргументы по умолчанию
            bound_dict[param] = defaults[i - defaults_offset]
        else:
            raise TypeError(ERR_MISSING_POS_ARGS)  # Не хватает обязательных позиционных аргументов

    # Привязываем именованные аргументы
    keys_to_pop: List[str] = []
    for kw, value in kwargs.items():
        if kw in kwonly_params:
            bound_dict[kw] = value  # Привязываем именованный аргумент
            keys_to_pop.append(kw)  # Запоминаем ключ для удаления
        elif not (code.co_flags & CO_VARKEYWORDS):
            raise TypeError(ERR_TOO_MANY_KW_ARGS)  # Слишком много именованных аргументов, если нет **kwargs

    for key in keys_to_pop:
        kwargs.pop(key)  # Убираем привязанные именованные аргументы из kwargs

    # Проверяем наличие обязательных позиционных аргументов
    missing_args = [p for p in params[:defaults_offset] if p not in bound_dict]
    if missing_args:
        raise TypeError(ERR_MISSING_POS_ARGS)

    # Проверяем, все ли обязательные именованные аргументы переданы
    for param in kwonly_params:
        if param not in bound_dict:
            if param in kwonly_defaults:
                bound_dict[param] = kwonly_defaults[param]  # Привязываем значение по умолчанию
            else:
                raise TypeError(ERR_MISSING_KWONLY_ARGS)  # Отсутствует обязательный именованный аргумент

    # Привязываем переменные позиционные аргументы (*args)
    if code.co_flags & CO_VARARGS:
        # Используем имя, объявленное в функции для *args
        var_args_name = code.co_varnames[pos_args_count + kwonlyargcount] if pos_args_count < len(
            code.co_varnames) else '*args'
        bound_dict[var_args_name] = args[pos_args_count:] if pos_args_count < len(args) else ()

    # Проверка и добавление **kwargs
    if code.co_flags & CO_VARKEYWORDS:
        var_kwarg_name = code.co_varnames[-1]  # Получаем имя для **kwargs
        bound_dict[var_kwarg_name] = kwargs  # Добавляем словарь для **kwargs

    return bound_dict  # Возвращаем привязанные аргументы
