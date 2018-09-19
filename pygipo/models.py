from functools import wraps
from uuid import uuid4

from django.contrib.postgres.fields import JSONField
from django.db import models

from pygipo import log


class Dump(models.Model):
    class Meta:
        db_table = 'dump'
        get_latest_by = 'dt'

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

    def addmany(self, entity, json_records, parent=None):
        assert isinstance(json_records, list), 'Please pass a list of things'
        return [self.add(entity, x, parent) for x in json_records]

    @property
    def records(self):
        return list(self.record_set.all())

    def __repr__(self):
        return '<Dump {0}>'.format(self.dt.strftime('%m-%d %H:%M:%S'))


class Record(models.Model):
    NUM_HEAD_CHARS = 40

    class Meta:
        db_table = 'record'
        ordering = ['dt', 'id']

    dump = models.ForeignKey('Dump', on_delete=models.CASCADE)
    dt = models.DateTimeField(auto_now=True, editable=False)
    entity = models.TextField()
    json = JSONField()
    parent = models.ForeignKey('Record', null=True, on_delete=models.CASCADE)

    def __repr__(self):
        return '<Record {0}: {1}...>'.format(
            self.dt.strftime('%Y-%m-%d_%H-%M-%S'),
            str(self.json)[:self.NUM_HEAD_CHARS])

    def __str__(self):
        return f'{self.entity} id={self.id}'

    @classmethod
    def list_entities(cls):
        """List all entity names"""
        entities = cls.objects.all().distinct('entity').order_by(
            'entity').values_list(
            'entity', flat=True)
        return list(entities)


def memoize(entity, dump=None, unpack=True):
    """
    :param unpack: set to False to save a list into the json field
    :param entity:
    :param dump: defaults to latest, creates new if it does not exist
    :return:
    """

    def memoize_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # get around UnboundLocalError. Direct assignment of dump does not work...
            d = dump
            if dump is None:
                try:
                    d = Dump.objects.latest()
                except Dump.DoesNotExist:
                    d = Dump.create()
            # return cached result if there are any hits for this entity
            count_existing = d.record_set.filter(entity=entity).count()
            if count_existing == 1:
                record = d.record_set.filter(entity=entity).first()
                return record.json
            elif count_existing >= 1:
                return [r.json for r in d.record_set.all()]
            else:
                log.debug(f'appending to dump {d.uuid}')
                result = f(*args, **kwargs)
                if isinstance(result, list) and unpack:
                    d.addmany(entity, result)
                else:
                    d.add(entity, result)
                return result

        return wrapper

    return memoize_decorator
