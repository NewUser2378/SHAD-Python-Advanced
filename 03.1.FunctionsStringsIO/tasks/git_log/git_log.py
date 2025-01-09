import typing as tp


def reformat_git_log(inp: tp.IO[str], out: tp.IO[str]) -> None:
    """Reads git log from `inp` stream, reformats it and prints to `out` stream

    Expected input format: `<sha-1>\t<date>\t<author>\t<email>\t<message>`
    Output format: `<first 7 symbols of sha-1>.....<message>`
    """

    logs = inp.readlines()
    for log in logs:
        normed = log.strip().split("\t")
        sha_first7 = normed[0][:7]
        new_message = normed[-1]
        new_log = sha_first7 + '.' * (80 - len(sha_first7) - len(new_message)) + new_message + '\n'
        out.write(new_log)
