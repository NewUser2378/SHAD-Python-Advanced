def caesar_encrypt(message: str, n: int) -> str:
    """Encrypt message using Caesar cipher.

    :param message: message to encrypt
    :param n: shift
    :return: encrypted message
    """

    ans = []
    for ch in message:
        if ch.isalpha():
            base_code = ord('a') if ch.islower() else ord('A')
            # ord(ch) + shift получаем код нового смещенного символа, делаем - base_code
            # чтобы, получить что код > кода букв (если это например z)
            # или < кода букв, если сдвиг отриателен, получаем номер буквы сдвинутый на сдвиг,
            # поэтому берем по модулю алфавита получаем номер буквы и добавим базовый код для обратного преобразования
            ans.append(chr((ord(ch) + n - base_code) % 26 + base_code))
        else:
            ans.append(ch)
    return ''.join(ans)
