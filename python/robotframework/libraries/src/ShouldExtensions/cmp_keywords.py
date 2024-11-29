from typing import Iterable, Mapping, Union


class CmpKeywords:
    def should_be_greather_than(self, value, bound):
        if not value > bound:
            raise AssertionError(
                f"value should be greater than {bound}, but was {value}."
            )

    def should_be_greather_than_or_equal_to(self, value, bound):
        if not value >= bound:
            raise AssertionError(
                f"value should be greater than or equal to {bound}, but was {value}."
            )

    def should_be_less_than(self, value, bound):
        if not value < bound:
            raise AssertionError(f"value should be less than {bound}, but was {value}.")

    def should_be_less_than_or_equal_to(self, value, bound):
        if not value <= bound:
            raise AssertionError(
                f"value should be less than or equal to {bound}, but was {value}."
            )

    def should_be_in_range(self, value, from_, to):
        if not from_ <= value <= to:
            raise AssertionError(
                f"value should be in range [{from_}, {to}], but was {value}"
            )

    def should_not_be_in_range(self, value, from_, to):
        if from_ <= value <= to:
            raise AssertionError(
                f"value should not be in range [{from_}, {to}], but was {value}"
            )

    def should_contain_substring(self, value: Iterable, expected: str):
        if isinstance(value, Mapping):
            raise AssertionError(f"value should be an Iterable, but was Mapping.")
        elif isinstance(value, Iterable):
            for elem in value:
                if expected in elem:
                    return
            raise AssertionError(
                f"value should contain an element with substring '{expected}', but not found"
            )
        else:
            raise AssertionError(
                f"{value} should be an Iterable, but was {value.__class__.__name__}."
            )

    def should_contain_mapping(self, value: Union[Iterable, Mapping], expected: dict):
        if isinstance(value, Mapping):
            self._mapping_should_contain_subset(value, expected)
        elif isinstance(value, Iterable):
            for elem in value:
                if self._mapping_should_contain_subset(elem, expected) is None:
                    return
            raise AssertionError(
                f"value should have superset of mapping {expected}, but not found"
            )
        else:
            raise AssertionError(
                f"{value} should be an Iterable, but was {value.__class__.__name__}."
            )

    def _mapping_should_contain_subset(
        self, value: Mapping, expected: dict
    ) -> Union[Exception, None]:
        for k, v in expected.items():
            if k not in value:
                return AssertionError(
                    f"value should have key '{k}', but key was not found"
                )
            if value[k] != v:
                return AssertionError(
                    f"value should have key:value '{k}':{v}, but value was {value[k]}"
                )
        return None
