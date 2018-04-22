# vim: set fileencoding=utf-8 filetype=python :
import django
from django.core.management.base import BaseCommand
from django.db import connection

EXPECTED_EXCEPTIONS = [
    'Name does not resolve',
    'the database system is starting up',
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            # this tries to run a statement using the credentials in settings.py
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
        except django.db.utils.OperationalError as e:
            for exp in EXPECTED_EXCEPTIONS:
                if exp in str(e):
                    raise SystemExit(1)
