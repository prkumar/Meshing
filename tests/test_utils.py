# Standard-library imports
import io

# Package imports
from meshing import utils

# Third-party imports
import pytest

# == Flush tests == #


@pytest.mark.parametrize("iterable", [
    list(range(3)),
    []
])
def test_flush_without_count_arg_yields_everything(iterable):
    assert list(utils.flush(iterable)) == list(iterable)


@pytest.mark.parametrize("iterable", [
    list(range(3)),
])
def test_flush_with_count_arg_yields_expected_elements(iterable):
    iterator = iter(iterable)
    assert list(utils.flush(iterable, 2)) == [next(iterator) for _ in range(2)]


@pytest.mark.parametrize("iterable", [
    list(range(3)),
    []
])
def test_flush_raises_error_when_count_exceeds_remaining(iterable):
    with pytest.raises(utils.FlushError):
        list(utils.flush(iterable, len(iterable) + 1))

# == NoneEmptyLines tests == #

TEST_FILE_1 = u"""
non-empty line

dsads
"""


@pytest.mark.parametrize("content", [
    TEST_FILE_1
])
def test_reading_only_empty_lines(content):
    fobj = io.StringIO(content)
    obj = utils.NonEmptyLines(io.StringIO(content))
    assert [l for l in (s.rstrip() for s in fobj.readlines()) if l] == list(obj)


@pytest.mark.parametrize("content, expected_length", [
    (TEST_FILE_1, 4)
])
def test_reading_reads_through_lines(content, expected_length):
    obj = utils.NonEmptyLines(io.StringIO(content))
    list(obj)  # drain obj
    assert obj.line_no == expected_length


@pytest.mark.parametrize("content", [
    2
])
def test_reading_unaccepted_input_raise_error(content):
    with pytest.raises(utils.NonEmptyLines.ReadError):
        list(utils.NonEmptyLines(content))

