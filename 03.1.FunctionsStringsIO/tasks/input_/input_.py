import sys
import typing as tp


def input_(prompt: str | None = None,
           inp: tp.IO[str] | None = None,
           out: tp.IO[str] | None = None) -> str | None:
    """Read a string from `inp` stream. The trailing newline is stripped.

    The `prompt` string, if given, is printed to `out` stream without a
    trailing newline before reading input.

    If the user hits EOF (*nix: Ctrl-D, Windows: Ctrl-Z+Return), return None.

    `inp` and `out` arguments are optional and should default to `sys.stdin`
    and `sys.stdout` respectively.
    """
    if inp is None:
        inp = sys.stdin
    if out is None:
        out = sys.stdout
    if prompt is not None:
        out.write(prompt)  # записываем в поток вывода (но не сразу на экран тк буфер вывода еще не заполнен до конца)
        out.flush()  # заставляем вывести на экран все что было в буфере
    try:
        line = inp.readline()
        if line == '':
            return None
        return line.rstrip('\n')  # убираем только последний пробел, но с сохранением всех пробелов
    except EOFError:  # обрабатываем случай если пытаемся считать строку, но встречаем конец файла
        return None
