DROP VIEW IF EXISTS v_project;
CREATE VIEW v_project AS
SELECT
    v_record.id AS _record_id,
    v_record._dump_id,
    v_record._dump_uuid,
    v_record.parent_id AS _record_parent_id,
    v_record.json as _record_json,
    (json ->> 'id') :: INT AS id,
    (json ->> 'name') :: TEXT AS name,
    (json ->> 'path') :: TEXT AS path,
    (json -> 'owner') :: JSONB AS owner,
    (json -> '_links') :: JSONB AS _links,
    (json ->> 'web_url') :: TEXT AS web_url,
    (json ->> 'archived') :: BOOLEAN AS archived,
    (json -> 'tag_list') :: JSONB AS tag_list,
    (json -> 'namespace') :: JSONB AS namespace,
    (json -> 'avatar_url') :: JSONB AS avatar_url,
    (json ->> 'created_at') :: TEXT AS created_at,
    (json ->> 'creator_id') :: INT AS creator_id,
    (json ->> 'star_count') :: INT AS star_count,
    (json ->> 'visibility') :: TEXT AS visibility,
    (json ->> 'description') :: TEXT AS description,
    (json ->> 'forks_count') :: INT AS forks_count,
    (json ->> 'lfs_enabled') :: BOOLEAN AS lfs_enabled,
    (json -> 'permissions') :: JSONB AS permissions,
    (json ->> 'public_jobs') :: BOOLEAN AS public_jobs,
    (json ->> 'jobs_enabled') :: BOOLEAN AS jobs_enabled,
    (json ->> 'merge_method') :: TEXT AS merge_method,
    (json ->> 'wiki_enabled') :: BOOLEAN AS wiki_enabled,
    (json ->> 'import_status') :: TEXT AS import_status,
    (json -> 'ci_config_path') :: JSONB AS ci_config_path,
    (json ->> 'default_branch') :: TEXT AS default_branch,
    (json ->> 'issues_enabled') :: BOOLEAN AS issues_enabled,
    (json ->> 'ssh_url_to_repo') :: TEXT AS ssh_url_to_repo,
    (json ->> 'http_url_to_repo') :: TEXT AS http_url_to_repo,
    (json ->> 'last_activity_at') :: TEXT AS last_activity_at,
    (json ->> 'snippets_enabled') :: BOOLEAN AS snippets_enabled,
    (json ->> 'open_issues_count') :: INT AS open_issues_count,
    (json -> 'shared_with_groups') :: JSONB AS shared_with_groups,
    (json -> 'forked_from_project') :: JSONB AS forked_from_project,
    (json ->> 'name_with_namespace') :: TEXT AS name_with_namespace,
    (json ->> 'path_with_namespace') :: TEXT AS path_with_namespace,
    (json ->> 'approvals_before_merge') :: INT AS approvals_before_merge,
    (json ->> 'merge_requests_enabled') :: BOOLEAN AS merge_requests_enabled,
    (json ->> 'request_access_enabled') :: BOOLEAN AS request_access_enabled,
    (json ->> 'shared_runners_enabled') :: BOOLEAN AS shared_runners_enabled,
    (json ->> 'container_registry_enabled') :: BOOLEAN AS container_registry_enabled,
    (json -> 'resolve_outdated_diff_discussions') :: JSONB AS resolve_outdated_diff_discussions,
    (json ->> 'printing_merge_request_link_enabled') :: BOOLEAN AS printing_merge_request_link_enabled,
    (json ->> 'only_allow_merge_if_pipeline_succeeds') :: BOOLEAN AS only_allow_merge_if_pipeline_succeeds,
    (json ->> 'only_allow_merge_if_all_discussions_are_resolved') :: BOOLEAN AS only_allow_merge_if_all_discussions_are_resolved
FROM v_record
WHERE entity = 'project';
