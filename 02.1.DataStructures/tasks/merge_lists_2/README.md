## MERGE LISTS 2

`control flow` `heapq` `list` `job interview extra question`

### Условие

Написать функцию, которая берет на вход k сортированных списков и получает на выходе объединенный сортированный список

* Используйте только итерацию
* Не изменяйте входные списки внутри функции
* Оцените сложность по времени и памяти
* Используйте `heapq` для реализации. Использовать встроенную функцию `heapq.merge` для реализации нельзя, иначе б смысла не было)

```
Пускай
k - число списков
ni - число элементов у списка i
n - max(n1,..., nk) максимальное число элементов списка

У вас должно получится:
- по времени: О(nklogk)
- по памяти: O(nk)
```

### Пример

```python
>>> merge([[1, 2], [3, 4], [0, 5]])
[0, 1, 2, 3, 4, 5]
```

### Про задачу

Продолжение задачи `MERGE LISTS`. На собеседованиях часто просят сказать, как сделать алгоритмически, не требуя написать.

Разница здесь в том, что нужно управлять большим число указателей и брать минимум каждый раз. 
Для этого вам надо использовать `heapq`. Когда я писала каноническую реализацию, то осознала, 
что это общее решение пишется гораздо проще, чем классическое для двух списков.


Эта модификация вам пригодится в задаче `BANNER SEARCH SYSTEM`.
