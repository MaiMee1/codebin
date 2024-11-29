import re
from typing import Any, Callable, Generator, Iterable, Mapping

from robot.api.logger import debug
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.Collections import NOT_SET

_builtin = BuiltIn()

# matches $variable syntax
variable_re = re.compile(r"\$([a-zA-Z_][a-zA-Z_0-9]*)\\?")


def yield_helper(value: str) -> Generator[tuple[slice, str], None, None]:
    """

    >>> list(yield_helper('$id'))
    [(slice(0, 3, None), 'id')]
    >>> list(yield_helper('{"id": $id}'))
    [(slice(7, 10, None), 'id')]
    >>> list(yield_helper('$id\\\\_ref_for_$id2'))
    [(slice(13, 17, None), 'id2'), (slice(0, 4, None), 'id')]
    """
    assert isinstance(value, str)
    for match in reversed(list(variable_re.finditer(value))):
        yield slice(match.start(0), match.end(0)), match.group(1)


def substitute_variables(value: Any, get_variable_value: Callable[[str], Any]) -> Any:
    if isinstance(value, str):
        for slc, name in yield_helper(value):
            val = get_variable_value(f"${{{name}}}")
            if val is NOT_SET:
                continue
            if slc.start == 0 and slc.stop == len(value):
                value = val
            else:
                value = value[: slc.start] + str(val) + value[slc.stop :]
        return value
    if isinstance(value, Mapping):
        for k, v in list(value.items()):
            v = substitute_variables(v, get_variable_value)
            k = substitute_variables(k, get_variable_value)
            value[k] = v
        return value
    if isinstance(value, Iterable):
        value[:] = [substitute_variables(e, get_variable_value) for e in value]
        return value
    # default
    return value


def _test_get_variable_value(name: str):
    dct = {
        "${id}": 1002,
    }
    return dct.get(name, NOT_SET)


def _get_variable_value(name: str):
    return _builtin.get_variable_value(name, NOT_SET)


class VariablesKeywords:
    """

    >>> substitude_variables('$id', _test_get_variable_value)
    1002
    >>> substitude_variables('$id2', _test_get_variable_value)
    '$id2'
    >>> dct = {'id': '$id'}
    >>> substitude_variables(dct, _test_get_variable_value)
    {'id': 1002}
    >>> dct
    {'id': 1002}
    >>> lst = ['$id', '$id2']
    >>> substitude_variables(lst, _test_get_variable_value)
    [1002, '$id2']
    >>> lst
    [1002, '$id2']
    >>> substitude_variables('{"id": $id}', _test_get_variable_value)
    '{"id": 1002}'
    >>> substitude_variables('$id\\\\_ref_for_$id2', _test_get_variable_value)
    '1002_ref_for_$id2'
    """

    def substitute_variables(self, value: Any) -> Any:
        """Returns the given value with variable strings in $varname syntax substituded with its current value.

        When the given value is a dict or a list, edits the given value in place.
        """
        return substitute_variables(value, _get_variable_value)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
