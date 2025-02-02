## LIFE GAME

`class` `game-of-life`

В это задаче нужно реализовать версию классической [Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).

### Предисловие

Океан представляется двумерным массивом ячеек. 

Каждая ячейка может быть:
* пустой
* со скалой
* с рыбой
* с креветкой


Ячейки являются соседними, если имеют хотя бы по одной общей точке с данной ячейкой.
Все ячейки за границами игрового поля считаются пустыми. 

Правила обновления ячеек:
* ячейки со скалами не меняются во времени
* если какой̆-то рыбе слишком тесно (от 4 и более соседей̆-рыб), то рыба погибает
* если рыбе слишком одиноко (0 или 1 соседей̆-рыб), то рыба погибает
* если у рыбы 2 или 3 соседа-рыбы, то она просто продолжает жить
* соседи-скалы и соседи-креветки никак не влияют на жизнь рыб
* креветки существуют по аналогичным правилам (учитывая только соседей креветок)
* если какая-то ячейка океана была пуста и имела ровно 3-х соседей рыб, то в следующий момент времени в ней рождается рыба.
Иначе если у ячейки было ровно три соседа-креветки, в ней рождается креветка
* изменение всех ячеек океана происходит одновременно, учитывая только состояния ячеек в предыдущий момент времени

В каждый̆ квант времени ячейки последовательно обрабатываются.

### Условие

Вам нужно в файле `life_game.py` реализовать класс `LifeGame`.
* Инициализируется начальным состоянием океана - прямоугольным списком списков (формируя тем самым матрицу), каждый элемент которого это число. 
0 - если ячейка пустая, 1 - со скалой, 2 - с рыбой, 3 - с креветкой
* Содержит метод `get_next_generation`, который обновляет состояние океана и возвращает его содержимое
* `get_next_generation` должен быть единственный публичным методом в классе
* Вам нужно подумать, как поделить все на небольшие логические методы, которые, 
в отличие от `get_next_generation` пометить "приватными", то есть через underscore. 

Например, вы хотите создать метод, который извлекает соседей для клетки
```python
class LifeGame(object):
    ...
    def _get_neighbours(self, i: int, j: int):
        pass
```
Это не настоящее сокрытие реализации. Это способ оповестить пользователя о том, что у него нет никаких гарантий на этот метод.

## Пример

```python
>>> life_game = LifeGame([[1, 1], [1, 1]])
>>> life_game.get_next_generation()
[[1, 1], [1, 1]]
```
