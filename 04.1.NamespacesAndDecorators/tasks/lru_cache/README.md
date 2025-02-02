## LRU cache

`decorators` `functools` `type casts` `OrderedDict`

### Условие

Бывает полезно оптимизировать вызовы "тяжёлых" функций с помощью кеширования.

Кеширование – это сохранение результатов выполнения функций для предотвращения повторных вычислений.
Перед вызовом функции проверяется есть ли уже вычисленный результат. Если есть – функция не вызывается,
а возвращается сохранённое значение.

Реализуйте декоратор для Least Recently Used (LRU) Cache. Пользователь указывает размер кеша
`N`, и в кеше сохраняются значения для `N` наборов входных параметров функции, причем вытесняется из кеша сначала то,
что использовалось давней всего.

Для решения задачи мы рекомендуем использовать `OrderedDict`.

Декоратор назовите `@cache`, он должен принимать один параметр – размер кеша. Поддержите как
можно более широкий класс функций (функции многих аргументов, функции с именоваными параметрами,
принимающие сложные типы и т.д.).

Декоратор не должен затирать документацию функции.

Естественно, вам нельзя пользоваться дефолтным `functools.lru_cache`, а также **не понадобится** `setrecursionlimit`
для прохождения тестов.

### Пример
Следующий код
```python
def foo(value):
    print('calculate foo for {}'.format(value))
    return value

foo(1)
foo(2)
foo(1)
foo(2)
foo(3)
foo(1)
```

производит вот такой вывод:
```
calculate foo for 1
calculate foo for 2
calculate foo for 3
```

### Typehints
Правильно описать типы внутри декоратора в терминах mypy поможет [этот
пример](https://mypy.readthedocs.io/en/latest/generics.html#declaring-decorators) из документации.
