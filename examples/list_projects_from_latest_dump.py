#!/usr/bin/env python
# encoding: utf-8

import django

django.setup()

from pygipo.models import Dump

dump = Dump.objects.last()

for r in dump.record_set.all():
    print(r.json['name'])
