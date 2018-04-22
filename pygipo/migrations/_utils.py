# vim: set fileencoding=utf-8 filetype=python :
"""
This module contains helper functions for Django migrations.

It is marked as private (underscore-prefixed), so Django does not choke on it
when collecting migration files.
"""
from glob import glob
import logging

import os
from django.conf import settings

log = logging.getLogger(__name__)

HERE = os.path.abspath(os.path.dirname(__file__))


def runfile(schema_editor, path):
    """
    Helper function to run a plain SQL file in migrations.

    See also https://docs.djangoproject.com/en/1.8/ref/migration-operations/#writing-your-own
    """
    abspath = os.path.join(settings.PROJECT_ROOT, path)
    contents = open(abspath).read()
    schema_editor.execute(contents)


def runviews():
    """
    Run all views that are present in the `views` directory next to this module.

    By convention view names start with numbers, so they get executed in the right order, e.g.::

        001_v_foo.sql
        002_v_bar.sql
        ...
    """
    from django.db import connection
    cursor = connection.cursor()
    paths = sorted(glob(os.path.join(HERE, 'views/*.sql')))
    for path in paths:
        log.info(path)
        with open(path, encoding='utf-8') as f:
            content = f.read().replace('%', '%%')
            cursor.execute(content)
