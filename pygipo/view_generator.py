#!/usr/bin/env python
# encoding: utf-8
import os

import django
from django.db import connection
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gl2pg.settings')
django.setup()

from pygipo.models import *


# class as namespace
class PG:
    INT = 'INT'
    STR = 'TEXT'
    BOOL = 'BOOLEAN'
    JSONB = 'JSONB'
    DEFAULT = JSONB


PG_TYPE_MAP = {
    int: PG.INT,
    str: PG.STR,
    bool: PG.BOOL,
}


def _mark_safe_dict_values(d):
    for k in d:
        d[k] = mark_safe(d[k])
    return d


class ViewGenerator:
    VIEW_NAME = 'v_record'

    def __init__(self, entity_name, name=None):
        self.entity_name = entity_name
        self.entity = Record.objects.filter(entity=entity_name).first()
        if name is not None:
            self.name = name
        else:
            self.name = f'v_{entity_name}'

    def select(self):
        cols = [
            'v_record.id AS _record_id',
            'v_record._dump_id',
            'v_record._dump_uuid',
            'v_record.parent_id AS _record_parent_id',
            'v_record.json as _record_json'
        ]
        for key, value in self.entity.json.items():
            pg_type = PG_TYPE_MAP.get(type(value), PG.DEFAULT)
            operator = '->>'
            if pg_type == PG.DEFAULT:
                operator = '->'
            column_context = dict(
                operator=operator,
                key=key,
                type=pg_type
            )
            coldef = render_to_string(
                'column.sql',
                _mark_safe_dict_values(column_context)
            )
            cols.append(coldef)
        column_definition = '    ' + ',\n    '.join(cols)
        view_context = {
            'view_name': self.VIEW_NAME,
            'entity': self.entity_name,
            'column_definition': column_definition
        }
        return render_to_string(
            'select.sql',
            _mark_safe_dict_values(view_context)
        )

    def view(self):
        return render_to_string('view.sql',
                                dict(view=self.name, select=self.select()))

    def apply(self):
        with connection.cursor() as cursor:
            cursor.execute(self.view())


if __name__ == '__main__':
    vg = ViewGenerator('project')
    print(vg.view(), end='')
