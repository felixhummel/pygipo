import os

from django.test import TestCase

from pygipo import models
from pygipo.mapper import Mapper, ColDef, Dump, Record
from pygipo.migrations._utils import runviews
from . import TestFile

here = os.path.dirname(__file__)


class TestMapper(TestCase):

    @classmethod
    def setUpTestData(cls):
        runviews()

    def setUp(self):
        from . import dummy
        self.dump = models.Dump.create()
        self.dump.add('project', dummy.project.attributes)

    def test_coldef(self):
        c = ColDef('foo', 23)
        self.assertEqual(c.render(), "(json ->> 'foo') :: INT AS foo")
        c = ColDef('bar', 'xxx')
        self.assertEqual(c.render(), "(json ->> 'bar') :: TEXT AS bar")
        c = ColDef('baz', {'i am': 'a dict'})
        self.assertEqual(c.render(), "(json -> 'baz') :: JSONB AS baz")

    def test_select(self):
        with open(os.path.join(here, 'expected/select.sql')) as f:
            expected = f.read()
        vg = Mapper('project')
        actual = vg.select()
        with open(os.path.join(here, 'actual/select.sql'), 'w') as f:
            f.write(actual)
        self.assertEqual(expected, actual)

    def test_view(self):
        with open(os.path.join(here, 'expected/view.sql')) as f:
            expected = f.read()
        vg = Mapper('project')
        actual = vg.view()
        with open(os.path.join(here, 'actual/view.sql'), 'w') as f:
            f.write(actual)
        self.assertEqual(expected, actual)

    def test_apply(self):
        vg = Mapper('project')
        vg.apply()

    def test_model(self):
        tf = TestFile('model.py')
        d = Dump.create()
        j = {'id': 1, 'name': 'foo', 'flag': True, 'x': {'something': 'completely different'}}
        rec = Record(dump=d, entity='foo', json=j)
        rec.save()
        mapper = Mapper('foo')
        model = mapper.model()
        tf.write_actual(model)
        self.assertEqual(model, tf.expected)
