#!/usr/bin/env python
# encoding: utf-8

import django
import gitlab

django.setup()
from pygipo.models import Dump

dump = Dump.create()

gl = gitlab.Gitlab.from_config()

for p in gl.projects.list(owned=True):
    print('.', end='')
    dump.add('project', p.attributes)
print()
