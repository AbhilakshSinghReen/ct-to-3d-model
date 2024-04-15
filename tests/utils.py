from sys import stdout


def print_inline(string):
    print(string, end="")
    stdout.flush()
