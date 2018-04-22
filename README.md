Python Gitlab and Postgres
==========================
Wrap
[python-gitlab](http://python-gitlab.readthedocs.io/en/stable/index.html)
with
[Django Models](https://docs.djangoproject.com/en/2.0/topics/db/models/)
pointing to
[Postgres views](https://www.postgresql.org/docs/current/static/sql-createview.html)
using
[JSONB](https://www.postgresql.org/docs/current/static/datatype-json.html).

# Workflow
Use `python-gitlab` to fetch JSON objects and
[memoize](https://en.wikipedia.org/wiki/Memoization) them in Postgres.

```python
import gitlab
from pygipo import memoize

gl = gitlab.Gitlab.from_config()

@memoize(entity='project')
def get_all_projects():
    return gl.projects.list(all=True)

# this takes a while
projects = get_all_projects()
len(projects)

# this is waaay faster
projects = get_all_projects()
len(projects)
```

`memoize` created a `Dump` for you containing all Projects as `Record`s:
```python
from pygipo.models import Dump

latest_dump = Dump.objects.latest()
projects = [rr.json for r in latest_dump.record_set.all()]
len(projects)
```
