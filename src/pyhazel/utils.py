__all__ = [
    "find_all_substrings"
]


def find_all_substrings(source: str, substring: str):
    start = 0
    while True:
        start = source.find(substring, start)
        if start == -1:
            return
        yield start
        start += len(substring)
