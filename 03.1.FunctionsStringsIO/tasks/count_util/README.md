## COUNT UTIL

`argparse` `split` `interview`

### Условие

Ваша задача — реализовать аналог консольной утилиты __wc__ на python в виде функции `count_util`, которая принимает
на вход текст и набор флагов в текстовом виде, в зависимости от которых функция возвращает:
* `-m` - число символов;
* `-l` - число строк;
* `-L` - длину самой длинной строки;
* `-w` - количество слов.

Если не передан ни один ключ, то считается, что указан полный набор: `-m -l -L -w`.

Также ключи могут передаваться вместе: `-lmL` и в любом порядке.

Число строк на вход может меняться от 0 до 100.

Функция возвращает словарь, где в зависимости от переданных флагов присутствуют следующие ключи (и соотв. значения):
* `chars` - кол-во символов;
* `lines` - кол-во строк;
* `longest_line` - наибольшая длина строки;
* `words` - кол-во слов.

Естественно, пользоваться консольной утилитой __wc__ в этой задаче запрещено (да и не сильно упростит задачу).

NB: Согласно документации __wc__: _A line is defined as a string of characters delimited by a <newline>
character. A word is defined as a string of characters delimited by white space characters_.
Т.е. **нужно правильно учесть** последний перенос строки.

### Пример
```python
>>> text = '''\
there is one
    more
example for
 problem
'''
>>> count_utils(text, flags=None)
{'lines': 4, 'words': 7, 'chars': 43, 'longest_line': 12}
```

### Про задачу
Простенькая задачка на работу со строками и парсинг аргументов командной строки.
Такую вполне могут дать на собеседовании.

Самым 'классическим' для создания cli считается стандартный модуль [argparse](https://docs.python.org/3/library/argparse.html).  
Но он однозначно не является самым удобным. Предлагаем вам рассмотреть библиотечку [click](https://click.palletsprojects.com/en/latest/), которая позволяет создавать cli гораздо быстрее и удобнее.

С этим вам нужно разобраться самостоятельно.


