
# Standard-library imports
import types


def is_generator(obj):
    return isinstance(obj, types.GeneratorType)


class NonEmptyLines(object):
    """
    File-like object that ignores lines containing only white-space.

    TODO:
        * Add support for ignoring comments.
    """

    @staticmethod
    def read(f):
        with (f if is_generator(f) else open(f)) as stream:
            for line_no, line in enumerate(stream):
                if line:
                    yield line_no + 1, line

    def __init__(self, filename_or_file):
        self._generator = self.read(filename_or_file)
        self._line_no = 0

    @property
    def line_no(self):
        return self._line_no

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        self._line_no, line = next(self._generator)
        return line


class FlushError(Exception):

    def __init__(self, expected, actual):
        self.expected = expected
        self.actual = actual


def flush(iterator, count=-1):
    remaining = count
    for item in iterator:
        if not remaining:
            break
        yield item
        remaining -= 1
    if remaining > 0:
        raise FlushError(count, remaining)
