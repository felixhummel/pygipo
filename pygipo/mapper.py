#!/usr/bin/env python
# encoding: utf-8
import os

import django
from django.db import connection
from django.template.loader import render_to_string

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gl2pg.settings')
django.setup()

from pygipo.models import *


# class as namespace
class PG:
    INT = 'INT'
    STR = 'TEXT'
    BOOL = 'BOOLEAN'
    JSONB = 'JSONB'


class ColDef:
    """
    Column definition inferred from a key/value pair in Python.
    """
    PG_TYPE_MAP = {
        int: PG.INT,
        str: PG.STR,
        bool: PG.BOOL,
    }
    DJANGO_TYPE_MAP = {
        int: 'models.IntegerField',
        str: 'models.TextField',
        bool: 'models.BooleanField'
    }

    DEFAULT_TYPE = PG.JSONB
    DJANGO_DEFAULT = 'django.contrib.postgres.fields.JSONField'

    def __init__(self, key, value):
        self.name = key
        self.python_type = type(value)
        self.pg_type = self.PG_TYPE_MAP.get(self.python_type, self.DEFAULT_TYPE)
        self.dj_type = self.DJANGO_TYPE_MAP.get(self.python_type, self.DJANGO_DEFAULT)

    def render(self):
        operator = '->>'
        if self.pg_type == ColDef.DEFAULT_TYPE:
            operator = '->'
        column_context = dict(
            operator=operator,
            name=self.name,
            pg_type=self.pg_type
        )
        return render_to_string('column.sql', column_context)


class Mapper:
    BASE_VIEW = 'v_record'
    PREFIX = 'vg_'

    def __init__(self, entity_name, name=None):
        self.entity_name = entity_name
        self.entity = Record.objects.filter(entity=entity_name).first()
        if name is not None:
            self.name = name
        else:
            self.name = f'{self.PREFIX}{entity_name}'
        self.coldefs = [ColDef(key, value) for key, value in self.entity.json.items()]

    def select(self):
        cols = [
            'v_record.id AS _record_id',
            'v_record._dump_id',
            'v_record._dump_uuid',
            'v_record.parent_id AS _record_parent_id',
            'v_record.json as _record_json'
        ]
        cols.extend([
            col.render() for col in self.coldefs
        ])
        column_definition = '    ' + ',\n    '.join(cols)
        view_context = {
            'view_name': self.BASE_VIEW,
            'entity': self.entity_name,
            'column_definition': column_definition
        }
        return render_to_string('select.sql', view_context)

    def view(self):
        return render_to_string('view.sql',
                                dict(view=self.name, select=self.select()))

    def apply(self):
        with connection.cursor() as cursor:
            cursor.execute(self.view())

    def model(self):
        fields = []
        for col in self.coldefs:
            fields.append(f'{col.name} = {col.dj_type}()')
        field_definition = '\n    '.join(fields)
        return render_to_string('model.py', dict(
            name=self.entity_name.capitalize(),
            field_definition=field_definition,
            table_name=self.name,
            app_label='pypigo_generated'
        ))
