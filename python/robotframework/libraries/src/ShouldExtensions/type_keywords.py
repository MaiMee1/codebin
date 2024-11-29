from typing import Iterable, Mapping, Sequence


class TypeKeywords:
    def should_be_boolean(self, value):
        if not isinstance(value, bool):
            raise AssertionError(
                f"{value} should be a boolean, but was {value.__class__.__name__}."
            )

    def should_be_number(self, value):
        if not isinstance(value, (int, float)):
            raise AssertionError(
                f"{value} should be a number, but was {value.__class__.__name__}."
            )

    def should_be_integer(self, value):
        if not isinstance(value, int):
            raise AssertionError(
                f"{value} should be an integer, but was {value.__class__.__name__}."
            )

    def should_be_none(self, value):
        if not value is None:
            raise AssertionError(f"{value} should be None, but was {value}.")

    def should_not_be_none(self, value):
        if value is None:
            raise AssertionError(f"{value} should not be None, but was.")

    def should_be_iterable(self, value):
        if not isinstance(value, Iterable):
            raise AssertionError(
                f"{value} should be an Iterable, but was {value.__class__.__name__}."
            )

    def should_be_mapping(self, value):
        if not isinstance(value, Mapping):
            raise AssertionError(
                f"{value} should be a Mapping, but was {value.__class__.__name__}."
            )

    def should_be_sequence(self, value):
        if not isinstance(value, Sequence):
            raise AssertionError(
                f"{value} should be a Sequence, but was {value.__class__.__name__}."
            )
