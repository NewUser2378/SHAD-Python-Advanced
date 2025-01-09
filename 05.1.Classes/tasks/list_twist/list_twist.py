from collections import UserList
import typing as tp


class ListTwist(UserList[tp.Any]):
    """
    List-like class with additional attributes:
        * reversed, R - return reversed list
        * first, F - insert or retrieve first element;
                     Undefined for empty list
        * last, L -  insert or retrieve last element;
                     Undefined for empty list
        * size, S -  set or retrieve size of list;
                     If size less than list length - truncate to size;
                     If size greater than list length - pad with Nones
    """

    def __getattr__(self, name: str) -> tp.Any:
        if name == 'reversed' or name == 'R':
            return self[::-1]
        elif name == 'first' or name == 'F':
            if not self.data:
                raise IndexError("List is empty, cannot access 'first'")
            return self.data[0]
        elif name == 'last' or name == 'L':
            if not self.data:
                raise IndexError("List is empty, cannot access 'last'")
            return self.data[-1]
        elif name == 'size' or name == 'S':
            return len(self.data)
        else:
            raise AttributeError(f"'ListTwist' object has no attribute '{name}'")

    def __setattr__(self, name: str, value: tp.Any) -> None:
        if name == 'first' or name == 'F':
            if not self.data:
                raise IndexError("List is empty, cannot set 'first'")
            self.data[0] = value
        elif name == 'last' or name == 'L':
            if not self.data:
                raise IndexError("List is empty, cannot set 'last'")
            self.data[-1] = value
        elif name == 'size' or name == 'S':
            if value < 0:
                raise ValueError("Size cannot be negative")
            current_size = len(self.data)
            if value > current_size:
                self.data.extend([None] * (value - current_size))
            elif value < current_size:
                del self.data[value:]
        else:
            super().__setattr__(name, value)
