SELECT
    query,
    calls,
    total_exec_time / calls AS avg_exec_time_ms,
    shared_blks_hit,
    shared_blks_read,
    blk_read_time,
    blk_write_time
FROM pg_stat_statements
WHERE query LIKE '%SELECT id, embedding %'
ORDER BY total_exec_time DESC;