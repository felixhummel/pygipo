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


# Prerequisites
A Gitlab instance and `python-gitlab`
[configuration](http://python-gitlab.readthedocs.io/en/stable/cli.html#configuration)
for it, e.g.
```
cat <<'EOF' >> ~/.python-gitlab.cfg
[global]
default = git.example.org
ssl_verify = true
timeout = 15

[git.example.org]
url = https://git.example.org/
private_token = xxxxxxxxxxxxxxxxxxxx
api_version = 4
EOF
```

Python 3.6 and requirements:
```
pip install -r requirements.txt
```

Postgres running on `localhost:15432`:
```
cat docker-compose.yml
docker-compose up -d

vi +'/^DATABASES' project/settings.py
./manage.py migrate
```


# Memoization
Use `python-gitlab` to fetch JSON objects and
[memoize](https://en.wikipedia.org/wiki/Memoization) them in Postgres.

```
./manage.py shell
```

```python
import gitlab
from pygipo.models import memoize

gl = gitlab.Gitlab.from_config()

@memoize(entity='project')
def get_my_projects():
    return [p.attributes for p in gl.projects.list(all=True, owned=True)]

# this takes a while
projects = get_my_projects()
len(projects)

# this is waaay faster
projects = get_my_projects()
len(projects)
```

`memoize` created a `Dump` for you containing all Projects as `Record`s:
```python
from pygipo.models import Dump

latest_dump = Dump.objects.latest()
projects = [r.json for r in latest_dump.record_set.all()]
len(projects)
```


# View and Model Generation
Take `Records`s, make them views and generate some models for them:
```
./manage.py views  # make sure that we have `v_record`

./manage.py genviews project
./manage.py genmodels project > generated/project.py

./manage.py shell <<EOF
from generated.project import Project
p = Project.objects.first()

print(p.id)
print(p.name)
EOF
```


# Run Examples
```
export DJANGO_SETTINGS_MODULE=project.settings
export PYTHONPATH=.
./examples/load_projects_from_a_group.py --help
```


# Cleanup
```
./bin/DANGER_clean_dev_env.sh
```

