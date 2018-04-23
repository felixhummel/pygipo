# vim: set fileencoding=utf-8 filetype=python :
from django.core.management.base import BaseCommand

from pygipo.mapper import Mapper


class Command(BaseCommand):
    help = 'Generates a Django model for an entity'

    def add_arguments(self, parser):
        parser.add_argument('entity', nargs='+')

    def handle(self, *args, **options):
        entities = options['entity']
        xs = []
        for entity in entities:
            mapper = Mapper(entity)
            xs.append(mapper.model())
        print('\n\n'.join(xs))
