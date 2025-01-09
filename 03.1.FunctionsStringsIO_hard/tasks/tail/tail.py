import sys
import typing as tp
from pathlib import Path


def tail(filename: Path, lines_amount: int = 10, output: tp.IO[bytes] | None = None) -> None:
    """
    :param filename: file to read lines from (the file can be very large)
    :param lines_amount: number of lines to read
    :param output: stream to write requested amount of last lines from file
                   (if nothing specified stdout will be used)
    """
    if output is None:
        output = sys.stdout.buffer  # Используем byte stream для вывода

    buffer = bytearray()
    lines = []

    with open(filename, 'rb') as file:
        file.seek(0, 2)  # перемещаем указатель в конец файла
        pointer_place = file.tell()
        for i in range(pointer_place, -1, -1):
            file.seek(i)
            new_byte = file.read(1)  # перемещаем указатль на позицию i (от начала файла)
            if not new_byte:  # если это не символ конца файла
                continue
            elif new_byte == b'\n':
                if buffer:
                    lines.append(buffer[::-1].decode())
                    buffer.clear()
                if len(lines) == lines_amount:
                    break
            else:
                buffer.append(new_byte[0])

        if buffer:  # случай если пришли в начало то достаем все что было
            lines.append(buffer[::-1].decode())
        for el in reversed(lines):
            output.write(el.encode() + b'\n')

    output.flush()
