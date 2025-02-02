## ARG BINDING

`__code__ ` `__defaults__` `__kwdefaults__` `co_flags` `co_varnames` `co_argcount` `co_kwonlyargcount`

### Условие

Допустим, есть функция `def foo(a, b, c=None, *args, **kwargs): ...`.
При вызове функции, например `foo(10, 20, verbose=True)`, интерпретатору необходимо связать переданные аргументы `(10, 20, verbose=True)`с именами аргументов из сигнатуры функции.
Этот процесс называется байндингом (binding) аргументов.
В данном примере интерпретатор поймёт, что аргумент `a` равен 10, аргумент `b` равен 20, агрумент `c` не задан при вызове,
но у него есть значение по умолчанию `None`, а аргумент `verbose` поместит в словарь `kwargs`.
Получится такой словарь:
```python
{
    'a': 10,
    'b': 20,
    'c': None,
    args: (),
    kwargs: {
        'verbose': True,
    },
}
```
Ваша задача - написать функцию `bind_args(func, *args, **kwargs)`, которая связывает переданные в `*args` и `**kwargs` значения с соответствующими именами из сигнатуры функции `func` и возвращает полученный словарь, или бросает исключение `TypeError` если байндинг не удался.
По сути задача сводится к тому, чтобы правильно разложить имена из `co_varnames` на кучки и склеить их с значениями из `*args`, `**kwargs`, `__defaults__` и `__kwdefaults__`, а всё остальное разложить в аргументы со звёздочками, если они заданы.
В деталях вам нужно разобраться самостоятельно.

### Примечания

* В одну строчку (почти-)решение выглядит примерно так: `inspect.signature(func).bind(*args, **kwargs)`.
* Но вам, конечно же, нельзя пользоваться модулем `inspect`.
* Но [документацию](https://docs.python.org/3/library/inspect.html) стоит почитать.
* Константы `CO_VARARGS` и `CO_VARKEYWORDS` пригодятся, чтобы парсить флаги `co_flags`.
* А строки `ERR_*` нужны для сообщений в исключениях.
* Бросать исключения надо, например, так: `raise TypeError(ERR_TOO_MANY_POS_ARGS)`.

### Про задачу

Эта задача - маленькая, но важная часть первой большой домашки, мы её выделили чтобы вам было проще.

### Теория

Одна из особенностей питона -- поддержка интроспекции объектов в рантайме.
Это делает язык гибким и позволяет делать много интересных вещей, вроде итерирования по атрибутам объекта, вызова функций/методов по имени-строке, вычисленному в рантайме, и так далее.
А функции в питоне -- это тоже объекты, и из них можно вытащить много интересного (например, их сигнатуру).
Рассмотрим некоторые интересные атрибуты функций.

**`func.__code__`**

Это объект типа `code object`, представляющий собой скомпилированный код функции.
В этом задании вам пригодятся следующие атрибуты:

* `func.__code__.co_flags` -- битовая маска флагов, описывающих функцию, например является ли она генератором, есть ли у неё аргументы со звёздочками, и т.д.
* `func.__code__.co_varnames` -- tuple с именами аргументов функции и локальных переменных.
* `func.__code__.co_argcount` -- количество аргументов функции, не включая аргументы со звёздочками и аргументы, которые можно передавать только по имени.
* `func.__code__.co_posonlyargcount` -- количество аргументов функции, которые можно передавать только позиционно.
* `func.__code__.co_kwonlyargcount` -- количество аргументов функции, которые можно передавать только по имени.

Посмотреть на `code object` можно с помощью модуля `dis`:

```python
In [1]: import dis

In [2]: def f(a, b, c, *args):
   ...:     pass
   ...:

In [3]: dis.show_code(f)
Name:              f
Filename:          <ipython-input-1-246c3e476442>
Argument count:    3
Positional-only arguments: 0
Kw-only arguments: 0
Number of locals:  4
Stack size:        1
Flags:             OPTIMIZED, NEWLOCALS, VARARGS, NOFREE
Constants:
   0: None
Variable names:
   0: a
   1: b
   2: c
   3: args
```

**`func.__defaults__`**

Tuple с значениями по умолчанию позиционных аргументов функции.
Заметьте, что в сигнатуре функции после аргументов по умолчанию не может быть аргументов без значения по умолчанию;
после них могут идти только `*`, `*args`, `**kwargs`, либо аргументы, которые можно передавать только по имени.

**`func.__kwdefaults__`**

Словарь значений по умолчанию аргументов функции, которые можно передавать только по имени.