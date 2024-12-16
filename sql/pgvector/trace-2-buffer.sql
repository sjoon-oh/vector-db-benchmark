SELECT
    count(*) AS total_buffers,
    sum(CASE WHEN isdirty THEN 1 ELSE 0 END) AS dirty_buffers,
    sum(CASE WHEN relname = 'postgres' THEN 1 ELSE 0 END) AS table_buffers
FROM pg_buffercache;