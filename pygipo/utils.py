# vim: set fileencoding=utf-8 filetype=python :
"""
This module contains helper functions for Django migrations.
"""
import logging
from pathlib import Path

from django.apps import apps
from django.db import connection

log = logging.getLogger(__name__)


def runviews():
    """
    Run all views that are present in the `views` directory next to this module.

    By convention view names start with numbers, so they get executed in the
    right order, e.g.::

        001_v_foo.sql
        002_v_bar.sql
        ...
    """
    app_path = Path(apps.get_app_config('pygipo').path)
    views_dir = app_path / 'migrations' / 'views'
    cursor = connection.cursor()
    for path in views_dir.glob('*.sql'):
        log.info(path)
        with path.open(encoding='utf-8') as f:
            content = f.read().replace('%', '%%')  # poor man's escaping
            cursor.execute(content)
