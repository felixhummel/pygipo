# vim: set fileencoding=utf-8 filetype=python :
from django.core.management.base import BaseCommand

from pygipo.mapper import Mapper


class Command(BaseCommand):
    help = 'Generate a postgres view for an entity'

    def add_arguments(self, parser):
        parser.add_argument('entity', nargs='+')

    def handle(self, *args, **options):
        entities = options['entity']
        for entity in entities:
            vg = Mapper(entity)
            vg.apply()
            print(vg.name)
