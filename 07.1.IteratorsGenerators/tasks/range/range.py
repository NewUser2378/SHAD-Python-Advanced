from collections.abc import Iterable, Iterator, Sized


class RangeIterator(Iterator[int]):
    """The iterator class for Range"""

    def __init__(self, range_: 'Range') -> None:
        self.cur = range_.start
        self.stop = range_.stop
        self.step = range_.step

    def __iter__(self) -> 'RangeIterator':
        return self

    def __next__(self) -> int:
        if (self.step > 0 and self.cur >= self.stop) or (self.step < 0 and self.cur <= self.stop):
            raise StopIteration
        cur_val = self.cur
        self.cur += self.step
        return cur_val


class Range(Sized, Iterable[int]):
    """The range-like type, which represents an immutable sequence of numbers"""

    def __init__(self, *args: int) -> None:
        """
        :param args: either it's a single `stop` argument
            or sequence of `start, stop[, step]` arguments.
        If the `step` argument is omitted, it defaults to 1.
        If the `start` argument is omitted, it defaults to 0.
        If `step` is zero, ValueError is raised.
        """
        if len(args) == 0:
            raise TypeError("should be at least 1 arg")
        elif len(args) == 1:
            self.start = 0
            self.stop = args[0]
            self.step = 1
        elif len(args) == 2:
            self.start = args[0]
            self.stop = args[1]
            self.step = 1
        elif len(args) == 3:
            self.start = args[0]
            self.stop = args[1]
            self.step = args[2]
            if self.step == 0:
                raise ValueError("Step cant be 0")
        else:
            raise TypeError("expected 1-3 arguments")

    def __iter__(self) -> 'RangeIterator':
        return RangeIterator(self)

    def __repr__(self) -> str:
        if self.step == 1:
            return f"range({self.start}, {self.stop})"
        else:
            return f"range({self.start}, {self.stop}, {self.step})"

    def __str__(self) -> str:
        if self.step == 1:
            return f"range({self.start}, {self.stop})"
        else:
            return f"range({self.start}, {self.stop}, {self.step})"

    def __contains__(self, key: int) -> bool:
        dont_missed = (key - self.start) % self.step == 0
        if self.step > 0:
            return self.start <= key < self.stop and dont_missed
        else:
            return self.start >= key > self.stop and dont_missed

    def __getitem__(self, key: int) -> int:
        if key < 0:
            key += self.__len__()
        if key < 0 or key >= self.__len__():
            raise IndexError("Index out of range")
        val = self.start + key * self.step
        if (self.step > 0 and val >= self.stop) or (self.step < 0 and val <= self.stop):
            raise IndexError("Index out of range")
        return val

    def __len__(self) -> int:
        if self.step > 0:
            return max(0, (self.stop - self.start + self.step - 1) // self.step)
        elif self.step < 0:
            return max(0, (self.start - self.stop - self.step - 1) // -self.step)
        else:
            return 0
