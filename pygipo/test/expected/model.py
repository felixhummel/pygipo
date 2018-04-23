import django.contrib.postgres.fields
from django.db import models


class Foo(models.Model):
    class Meta:
        managed = False
        db_table = 'vg_foo'
        app_label = 'pypigo_generated'

    x = django.contrib.postgres.fields.JSONField()
    id = models.IntegerField()
    flag = models.BooleanField()
    name = models.TextField()
