import unittest

from pygipo.models import memoize


class TestMemoize(unittest.TestCase):

    def test(self):
        @memoize
        def get_xs():
            return [
                {'a': 23},
                {'b': 12}
            ]

        xs1 = get_xs()
        xs2 = get_xs()

        for x1, x2 in zip(xs1, xs2):
            self.assertDictEqual(x1, x2)
