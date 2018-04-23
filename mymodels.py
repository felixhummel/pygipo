import django.contrib.postgres.fields
from django.db import models


class Project(models.Model):
    class Meta:
        managed = False
        db_table = 'vg_project'
        app_label = 'pypigo_generated'

    id = models.IntegerField()
    name = models.TextField()
    path = models.TextField()
    _links = django.contrib.postgres.fields.JSONField()
    web_url = models.TextField()
    archived = models.BooleanField()
    tag_list = django.contrib.postgres.fields.JSONField()
    namespace = django.contrib.postgres.fields.JSONField()
    avatar_url = django.contrib.postgres.fields.JSONField()
    created_at = models.TextField()
    creator_id = models.IntegerField()
    star_count = models.IntegerField()
    visibility = models.TextField()
    description = models.TextField()
    forks_count = models.IntegerField()
    lfs_enabled = models.BooleanField()
    permissions = django.contrib.postgres.fields.JSONField()
    public_jobs = models.BooleanField()
    jobs_enabled = models.BooleanField()
    wiki_enabled = models.BooleanField()
    import_status = models.TextField()
    ci_config_path = django.contrib.postgres.fields.JSONField()
    default_branch = models.TextField()
    issues_enabled = models.BooleanField()
    ssh_url_to_repo = models.TextField()
    http_url_to_repo = models.TextField()
    last_activity_at = models.TextField()
    snippets_enabled = models.BooleanField()
    open_issues_count = models.IntegerField()
    shared_with_groups = django.contrib.postgres.fields.JSONField()
    name_with_namespace = models.TextField()
    path_with_namespace = models.TextField()
    merge_requests_enabled = models.BooleanField()
    request_access_enabled = models.BooleanField()
    shared_runners_enabled = models.BooleanField()
    container_registry_enabled = models.BooleanField()
    resolve_outdated_diff_discussions = models.BooleanField()
    printing_merge_request_link_enabled = models.BooleanField()
    only_allow_merge_if_pipeline_succeeds = models.BooleanField()
    only_allow_merge_if_all_discussions_are_resolved = models.BooleanField()

