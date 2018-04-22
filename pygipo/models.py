from uuid import uuid4

from django.contrib.postgres.fields import JSONField
from django.db import models


class Dump(models.Model):
    class Meta:
        db_table = 'dump'

    dt = models.DateTimeField(auto_now=True, editable=False)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)

    @classmethod
    def create(cls):
        self = cls()
        self.save()
        return self

    def add(self, entity, json_data, parent=None):
        record = Record(dump=self, entity=entity, json=json_data,
                        parent=parent)
        record.save()
        return record

    @property
    def records(self):
        return list(self.record_set.all())

    def __repr__(self):
        return '<Dump {0}>'.format(self.dt.strftime('%m-%d %H:%M:%S'))


class Record(models.Model):
    NUM_HEAD_CHARS = 40

    class Meta:
        db_table = 'record'
        ordering = ['dt']

    dump = models.ForeignKey('Dump', on_delete=models.CASCADE)
    dt = models.DateTimeField(auto_now=True, editable=False)
    entity = models.TextField()
    json = JSONField()
    parent = models.ForeignKey('Record', null=True, on_delete=models.CASCADE)

    def __repr__(self):
        return '<Record {0}: {1}...>'.format(
            self.dt.strftime('%Y-%m-%d_%H-%M-%S'),
            str(self.json)[:self.NUM_HEAD_CHARS])
