def get_fizz_buzz(n: int) -> list[int | str]:
    """
    If value divided by 3 - "Fizz",
       value divided by 5 - "Buzz",
       value divided by 15 - "FizzBuzz",
    else - value.
    :param n: size of sequence
    :return: list of values.
    """
    ans: list[int | str] = []
    for i in range(1, n + 1):
        ost = i % 15
        if ost == 0:
            ans.append("FizzBuzz")
        elif ost % 3 == 0:
            ans.append("Fizz")
        elif ost % 5 == 0:
            ans.append("Buzz")
        else:
            ans.append(i)

    return ans
