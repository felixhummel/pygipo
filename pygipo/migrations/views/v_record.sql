DROP VIEW IF EXISTS v_record CASCADE;

CREATE OR REPLACE VIEW v_record AS
  SELECT
    dump.id   AS _dump_id,
    dump.uuid AS _dump_uuid,
    dump.dt   AS _dump_dt,
    record.id,
    entity,
    json,
    parent_id,
    record.dt
  FROM record
    join dump ON record.dump_id = dump.id
  WHERE dump_id = (SELECT id
                   FROM dump
                   ORDER BY dt desc
                   limit 1

  );

-- SELECT *
-- FROM v_record;
