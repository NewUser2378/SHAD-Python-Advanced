from collections.abc import Callable
from typing import Any, TypeVar, Tuple, Dict, cast
from collections import OrderedDict
from functools import wraps

Function = TypeVar('Function', bound=Callable[..., Any])


def cache(max_size: int) -> Callable[[Function], Function]:
    def memoizing(func: Function) -> Function:
        cache_dict: OrderedDict[Tuple[Any, ...], Any] = OrderedDict()

        @wraps(func)
        def wrapper(*args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> Any:
            key = (args, frozenset(kwargs.items()))

            if key in cache_dict:
                cache_dict.move_to_end(key)
                return cache_dict[key]

            res = func(*args, **kwargs)
            cache_dict[key] = res

            if len(cache_dict) > max_size:
                cache_dict.popitem(last=False)

            return res

        return cast(Function, wrapper)

    return memoizing
