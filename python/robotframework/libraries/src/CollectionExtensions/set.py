from typing import Iterable


class SetKeywords:
    @staticmethod
    def create_tuple(*items):
        """Returns a tuple containing given items."""
        return items

    @staticmethod
    def create_set(*items):
        """Returns a set containing given items."""
        return set(items)

    @staticmethod
    def convert_to_set(iterable: Iterable):
        """Converts the given ``iterable`` to a set."""
        return set(iterable)

    @staticmethod
    def add_to_set(set_: set, *values):
        """Adds ``values`` to ``set_``."""
        for value in values:
            set_.add(value)

    @staticmethod
    def set_union_of(*sets: set):
        """Return a new set with elements from the set and all others.."""
        return set.union(*sets)

    @staticmethod
    def remove_from_set(set_: set, *values):
        """Removes ``values`` from ``set_``."""
        for value in values:
            set_.remove(value)

    def set_should_contain(self, set_: set, value, msg=None):
        if not value in set_:
            raise AssertionError(
                msg or f"set should contain {value} but was actually {set_}"
            )
