# vim: set fileencoding=utf-8 filetype=python :
"""
Loads all views in Python's default sort order.

See runviews in app.migrations._utils for more.
"""

from django.core.management.base import BaseCommand

# noinspection PyProtectedMember
from pygipo.migrations._utils import runviews


class Command(BaseCommand):
    help = 'Load views defined in <app_dir>/migrations/views/*.sql'

    def handle(self, *args, **options):
        runviews()
