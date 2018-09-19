# vim: set fileencoding=utf-8 filetype=python :
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'List entities that could potentially be mapped by genmodels'

    def handle(self, *args, **options):
        from pygipo.models import Record
        entities = Record.objects.all().distinct('entity').order_by(
            'entity').values_list(
            'entity', flat=True)
        print('\n'.join(entities))
