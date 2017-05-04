from meshing import utils

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



