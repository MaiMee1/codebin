from typing import Generator, TypeVar

T = TypeVar("T")


def split(lst: list[T], sep: T) -> Generator[list[T], None, None]:
    seg = list()
    for e in lst:
        if e == sep:
            yield seg
            seg = list()
        else:
            seg.append(e)
    yield seg


def split_n(lst: list[T], sep: T, n: int) -> Generator[list[T], None, None]:
    counter = 0
    for l in split(lst, sep):
        yield l
        counter += 1
        if counter == n:
            return
    if n > 0 and counter < n:
        for _ in range(n - counter):
            yield list()


class ListKeywords:
    @staticmethod
    def split_from_list(lst: list[T], sep: T, n: int = -1) -> tuple[list[T], ...]:
        """Returns ``n`` lists split from ``lst`` using element seperator ``sep``."""
        return tuple(split_n(lst, sep, n))

    @staticmethod
    def with_values_removed_from_list(lst: list[T], *args: T) -> list[T]:
        """Returns a new list with given values removed from ``lst``."""
        l2 = list()
        for e in lst:
            if e in args:
                continue
            else:
                l2.append(e)
        return l2
