#!/usr/bin/env python
# encoding: utf-8
import logging
import sys

import django
import gitlab

log = logging.getLogger('pygipo')

django.setup()
from pygipo.models import Dump


def main(group_name):
    dump = Dump.create()
    gl = gitlab.Gitlab.from_config()

    log.info(f'Fetching projects from group {group_name}')

    gl_group = gl.groups.get(id=group_name)
    group_projects = gl_group.projects.list(all=True)
    gl_projects = [gl.projects.get(id=p.id) for p in group_projects]

    for gl_project in gl_projects:
        project = dump.add('project', gl_project.attributes)
        log.debug(project)
        # get project events
        # ==================
        gl_events = gl_project.events.list(all=True)
        log.info(f'  events: {len(gl_events)}')
        for gl_event in gl_events:
            dump.add('event', gl_event.attributes, parent=project)
        # get users
        # =========
        # project users (returned by gl_project.users.list) are different
        # to "normal" users returned from gl.users.list
        gl_users = [gl.users.get(id=project_user.id) for project_user in
                    gl_project.users.list(all=True)]
        log.info(f'  users: {len(gl_users)}')
        for gl_user in gl_users:
            user = dump.add('user', gl_user.attributes, parent=project)
            project2user_record = {'project_id': gl_project.id,
                                   'user_id': gl_user.id}
            dump.add('project2user', project2user_record)


if __name__ == '__main__':
    main(sys.argv[1])
