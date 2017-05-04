
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


class NonEmptyLines(object):
    """
    File-like object that ignores lines containing only white-space.

    TODO:
        * Add support for ignoring comments.
    """

    class ReadError(TypeError):
        def __init__(self, f):
            self.message = "Failed to read: " \
                           "expected filename or context manager, got " \
                           "%s." % (type(f))

    @staticmethod
    def read(f):
        try:
            with (open(f) if isinstance(f, str) else f) as stream:
                for line_no, line in enumerate((l.rstrip() for l in stream)):
                    if line:
                        yield line_no + 1, line
        except (TypeError, AttributeError):
            raise NonEmptyLines.ReadError(f)

    def __init__(self, f):
        self._generator = self.read(f)
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
