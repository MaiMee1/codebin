from typing import TypeVar

K = TypeVar("K")
V = TypeVar("V")


class DictKeywords:
    @staticmethod
    def select_from_dictionary(dct: dict[K, V], *keys: K) -> dict[K, V]:
        """Returns a dictionary containing keys from ``keys`` and values from ``dct``."""
        d = dict()
        for k in keys:
            if k in dct:
                d[k] = dct[k]
        return d
