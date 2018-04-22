from django.test import TestCase

from pygipo.models import memoize, Dump


class TestMemoize(TestCase):

    @staticmethod
    def _get_xs():
        return [
            {'a': 23},
            {'b': 12}
        ]

    def test(self):
        dump = Dump.create()

        @memoize(entity='fooentity', dump=dump)
        def get_xs():
            return self._get_xs()

        xs1 = get_xs()
        xs2 = get_xs()

        for x1, x2 in zip(xs1, xs2):
            self.assertDictEqual(x1, x2)

        for rec, x in zip(dump.records, xs1):
            self.assertDictEqual(rec.json, x)

    def test_latest_dump(self):
        @memoize('barentity')
        def bars():
            return self._get_xs()

        xs1 = bars()
        xs2 = bars()

        for x1, x2 in zip(xs1, xs2):
            self.assertDictEqual(x1, x2)

        dump = Dump.objects.latest()
        for rec, x in zip(dump.records, xs1):
            self.assertDictEqual(rec.json, x)

    def test_no_unpack(self):
        @memoize('barentity', unpack=False)
        def bars():
            return self._get_xs()

        xs1 = bars()
        xs2 = bars()

        for x1, x2 in zip(xs1, xs2):
            self.assertDictEqual(x1, x2)

        dump = Dump.objects.latest()
        rec = dump.record_set.first()
        self.assertEqual(rec.json, xs1)
