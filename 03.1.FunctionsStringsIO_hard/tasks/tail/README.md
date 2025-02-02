## tail -n

`file stream` `io` `seek` `tell` `chunk` `interview`

### Условие

Напишите функцию `tail`, которая выводит в поток `output` последние `lines_amount` строк из файла большого размера.

Файл может быть настолько большим, что читать его сначала - плохая затея.
Здесь вам пригодится знание о том, что файл можно читать
[непоследовательно (например, с конца)](https://docs.python.org/3/library/io.html?highlight=seek#io.IOBase.seek)
и [небольшими кусочками (чанками)](https://docs.python.org/3/library/io.html?highlight=seek#io.BufferedIOBase.read).

Не забудьте, что в одном чанке может оказаться как больше строк, чем требуется, так и не оказаться вовсе (если строка
очень длинная).

Попробуйте также не хранить строки в памяти, для этого вам понадобятся:
- буфер для чтения ([`bytearray`](https://docs.python.org/3/library/stdtypes.html#bytearray))
- файловый метод [`readinto`](https://docs.python.org/3/library/io.html?highlight=seek#io.BufferedIOBase.readinto)
- [`memoryview`](https://docs.python.org/3/library/stdtypes.html#memoryview),
чтобы не копировать байты при взятии части буфера
- в [`sys.stdout`](https://docs.python.org/3.10/library/sys.html?highlight=sys%20stdout#sys.stdout) 
можно писать bytes без декодирования

Перечисленные выше методы помогут вам не только при чтении файла, но и при выводе в output.


### Примеры
```python
>>> tail(filename='access.log', lines_amount=10)
[28/Sep/2019:15:47:35 +0000] py.manytask.org 85.89.127.36 "GET /static/favicon.png HTTP/1.1" 200 0.004 1825 "0.004"
[28/Sep/2019:15:48:08 +0000] py.manytask.org 84.201.135.190 "POST /api/report HTTP/1.1" 200 4.605 161 "4.604"
[28/Sep/2019:15:49:09 +0000] py.manytask.org 85.89.127.36 "GET / HTTP/1.1" 200 0.164 8347 "0.164"
[28/Sep/2019:15:49:10 +0000] py.manytask.org 85.89.127.36 "GET /static/favicon.png HTTP/1.1" 200 0.004 1825 "0.004"
[28/Sep/2019:15:51:41 +0000] py.manytask.org 83.149.45.23 "GET / HTTP/1.1" 200 0.190 8356 "0.188"
[28/Sep/2019:15:53:12 +0000] py.manytask.org 46.188.125.56 "GET / HTTP/1.1" 200 0.200 8367 "0.196"
[28/Sep/2019:15:55:28 +0000] py.manytask.org 35.204.45.179 "POST /api/report HTTP/1.1" 200 4.567 161 "4.564"
[28/Sep/2019:15:56:41 +0000] py.manytask.org 91.228.178.70 "GET / HTTP/1.1" 200 0.171 8337 "0.172"
[28/Sep/2019:15:56:41 +0000] py.manytask.org 91.228.178.70 "GET /static/favicon.png HTTP/1.1" 200 0.004 1824 "0.004"
[28/Sep/2019:15:57:03 +0000] py.manytask.org 91.228.178.70 "GET / HTTP/1.1" 200 0.130 8337 "0.128"
```

### Про задачу

За довольно простой формулировкой скрывается сразу 2 идеи: знание о том, что обычные файлы можно читать с любого места,
и что эффективнее читать чанками, а не отдельными байтами.

Эту задачу у нас дают на собеседовании (без требования писать в специальный поток `output`),
и как показывает практика - с ней плохо справляются.


### Про подсветку

Ваша IDE может ругаться на отсутствие некоторых методов у объектов, возвращаемых стандартными функциями, 
или неподходящих типов аргументов в функциях. 
Существует несколько способов добавить подсказки для статического анализатора:
- `var = tp.cast(type, var)` - применяется, когда делается присваивание или при передаче аргумента в функцию
- `var: type` - на случай, когда не подходит первый вариант; пишется на отдельной строке