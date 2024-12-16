SELECT
    sum(blk_read_time) AS total_read_time_ms,
    sum(blk_write_time) AS total_write_time_ms,
    sum(shared_blks_read) AS total_shared_blocks_read,
    sum(shared_blks_written) AS total_shared_blocks_written
FROM pg_stat_statements;