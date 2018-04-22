from django.test import TestCase

from pygipo.models import Dump, Record


class TestModels(TestCase):
    """
    test shortcut methods
    """

    def test_dump(self):
        dump = Dump.create()
        dump.add('foo', {'a': 23})
        self.assertEqual(len(dump.records), 1)

    def test_parent(self):
        dump = Dump.create()
        foo = dump.add('foo', {'a': 23})
        dump.add('bar', {'b': 12}, parent=foo)
        bar = Record.objects.get(parent__isnull=False)
        self.assertEqual(bar.json['b'], 12)
