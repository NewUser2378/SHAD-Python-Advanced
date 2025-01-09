from typing import Any, Optional

PROMPT: str = '>>> '


def run_calc(context: Optional[dict[str, Any]] = None) -> None:
    """Run interactive calculator session in specified namespace."""
    if context is None:
        context = {}  # Если контекст не задан, используем пустой словарь
    try:
        while True:
            print(PROMPT, end='')
            toeval = input()
            print(eval(toeval, {'__builtins__': {}}, context))
    except EOFError:  # Обрабатываем случай, если пытаемся считать строку, но встречаем конец
        print()
        return
