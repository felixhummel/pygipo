CREATE OR REPLACE VIEW report_user_action_log AS
  -- for each project: heading + user list
  WITH p2u AS (SELECT p.name as project_name,
                      p.id   as project_id,
                      u.name as user_name,
                      u.id   as user_id
               FROM vg_user u
                      INNER JOIN vg_project p
                        ON u._record_parent_id = p._record_id
      -- students only
               WHERE u.identities -> 0 ->> 'extern_uid' LIKE '%ou=studenten%'
               ORDER BY p.name, u.name)
  -- events per user for time slice
  SELECT p2u.project_name,
         p2u.user_name,
         created_at,
         target_type,
         action_name,
         target_title,
         note ->> 'body'          as note_body,
         note ->> 'noteable_type' as noteable_type
  FROM vg_event e
         INNER JOIN p2u ON e.author_id = p2u.user_id
  ORDER BY p2u.project_name,
           p2u.user_name,
           created_at;
