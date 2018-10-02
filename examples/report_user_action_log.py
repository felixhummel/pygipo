#!/usr/bin/env python
# encoding: utf-8
import csv
import logging
import sys

import click
import django

django.setup()
from django.db import connection

log = logging.getLogger('pygipo')


@click.command()
@click.argument('from_date')
@click.argument('to_date')
def main(from_date, to_date):
    """
    Dumps user actions as CSV between `from_date` (inclusive)
    and `to_date` (exclusive).

    Example Usage:

    ./examples/report_user_action_log.py 2018-05-10 2018-05-18
    """
    cursor = connection.cursor()
    query = f"""
SELECT * FROM report_user_action_log
WHERE created_at BETWEEN '{from_date}' AND '{to_date}'
"""
    cursor.execute(query)
    writer = csv.writer(sys.stdout)

    col_names = [i[0] for i in cursor.description]
    writer.writerow(col_names)
    writer.writerows(cursor.fetchall())


if __name__ == '__main__':
    main()
