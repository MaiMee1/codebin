import operator
from itertools import islice
from typing import Iterable, Mapping, TypeVar, Union

def _batched(iterable, n, *, strict=False):
    if n < 1:
        raise ValueError("n must be at least one")
    iterator = iter(iterable)
    while batch := tuple(islice(iterator, n)):
        if strict and len(batch) != n:
            raise ValueError("batched(): incomplete batch")
        yield batch


K = TypeVar("K")
V = TypeVar("V")


class FunctionalKeywords:
    @staticmethod
    def pluck(
        it: Iterable[Union[Iterable[V], Mapping[K, V]]], key: Union[int, K]
    ) -> list[V]:
        """Shorthand for ``list(map(lambda x: x[key], it))``"""
        return list(map(operator.itemgetter(key), it))

    @staticmethod
    def batch(iterable: Iterable[V], n: int, *, strict=False) -> tuple[list[V], ...]:
        """Batch data from the ``iterable`` into tuples of length ``n``. The last batch may be shorter than ``n``."""
        return _batched(iterable, n, strict=strict)
