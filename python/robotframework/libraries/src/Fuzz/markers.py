import re

from robot.api.logger import debug

# matches ALLCAPS between [] without preceding \[ (requires an extra token in the front).
marker_re = re.compile(r"\[(?<=[^\\]\[)[A-Z]+]")


def parse_marker_string(value: str) -> tuple[str, list[str]]:
    """

    >>> parse_marker_string('[HI]')
    ('', ['[HI]'])
    >>> parse_marker_string('\\\\[ESCAPED]')
    ('[ESCAPED]', [])
    >>> parse_marker_string('{sdvsdf[[COMPLEX]}[MATCH]!\\\\[sdf[s\\\\]')
    ('{sdvsdf[}![sdf[s\\\\]', ['[COMPLEX]', '[MATCH]'])
    >>> parse_marker_string('[MARKERS][IN][ORDER][NO][MARKERS][DUPE]')
    ('', ['[MARKERS]', '[IN]', '[ORDER]', '[NO]', '[DUPE]'])
    >>> parse_marker_string('[MARKERS][IN][ORDER][NO][MARKERS][DUPE]')
    ('', ['[MARKERS]', '[IN]', '[ORDER]', '[NO]', '[DUPE]'])
    """
    assert isinstance(value, str)
    value = " " + value
    markers = [match.group(0) for match in marker_re.finditer(value)]
    value, n = marker_re.subn("", value)
    assert n == len(markers)
    value = value.replace(r"\[", "[")
    value = value[1:]
    return value, list(dict.fromkeys(markers))


class MarkersKeywords:
    """

    Examples:
    >>> MarkersKeywords().must_parse_only_markers('[WORDS]', '[WORDS][NUMBER][DATE][TIME][DATETIME]')
    ['[WORDS]']
    """

    def parse_marker_string(self, value: str) -> tuple[str, list[str]]:
        """Returns the unescaped string with markers removed, along with the removed markerset.

        Markers are in the format ``[ALLCAPS]`` and prepending a backslash like so: ``\\[ISESCAPED]`` escapes the value.
        """
        return parse_marker_string(value)

    def must_parse_only_markers(self, value: str, totalset: str = None) -> list[str]:
        """Returns a unique list of markers from the ``value`` markerset string"""
        v, markers = parse_marker_string(value)
        assert v == "", f"value must contain only markers, got extra '{v}'"
        if len(markers) == 0:
            raise AssertionError("value must contain at least one marker, got 0")
        if totalset:
            v, total = parse_marker_string(totalset)
            assert v == ""
            if len(set(markers).difference(total)) > 0:
                raise AssertionError(
                    f"value must have markers within {total}, but has {list(set(markers).difference(total))}"
                )
        return markers


if __name__ == "__main__":
    import doctest

    doctest.testmod()
