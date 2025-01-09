def count_util(text: str, flags: str | None = None) -> dict[str, int]:
    """
    :param text: text to count entities
    :param flags: flags in command-like format - can be:
        * -m stands for counting characters
        * -l stands for counting lines
        * -L stands for getting length of the longest line
        * -w stands for counting words
    More than one flag can be passed at the same time, for example:
        * "-l -m"
        * "-lLw"
    Ommiting flags or passing empty string is equivalent to "-mlLw"
    :return: mapping from string keys to corresponding counter, where
    keys are selected according to the received flags:
        * "chars" - amount of characters
        * "lines" - amount of lines
        * "longest_line" - the longest line length
        * "words" - amount of words
    """

    if (flags):
        sort_flags = set(flags.replace(" ", "").replace("-", ""))
    else:
        sort_flags = {'L', 'l', 'm', 'w'}
    text_chars = len(text)
    lines_count = text.count('\n')
    splited_lines = text.split('\n')
    max_line_len = 0
    for one_line in splited_lines:
        max_line_len = max(max_line_len, len(one_line))
    word_count = len(text.split())
    dictr = {}
    for flg in sort_flags:
        if flg == 'l':
            dictr["lines"] = lines_count
        elif flg == 'w':
            dictr["words"] = word_count
        elif flg == 'L':
            dictr["longest_line"] = max_line_len
        elif flg == 'm':
            dictr["chars"] = text_chars
    return dictr
