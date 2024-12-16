COPY (
    SELECT
        clock_timestamp() AS log_time,
        query,
        total_exec_time / NULLIF(calls, 0) AS avg_exec_time_ms,
        shared_blks_hit,
        shared_blks_read,
        blk_read_time,
        blk_write_time,
        (SELECT count(*) FROM pg_buffercache) AS total_buffers,
        (SELECT sum(CASE WHEN isdirty THEN 1 ELSE 0 END) FROM pg_buffercache) AS dirty_buffers,
        -- Buffer statistics for 'items'
        (SELECT count(*) 
         FROM pg_buffercache b
         JOIN pg_class c ON b.relfilenode = pg_relation_filenode(c.oid)
         WHERE c.relname = 'items') AS items_buffers,
        (SELECT count(*) * current_setting('block_size')::int / 1024 
         FROM pg_buffercache b
         JOIN pg_class c ON b.relfilenode = pg_relation_filenode(c.oid)
         WHERE c.relname = 'items') AS items_buffer_size_kb,
        -- Buffer statistics for 'items_embedding_idx'
        (SELECT count(*) 
         FROM pg_buffercache b
         JOIN pg_class c ON b.relfilenode = pg_relation_filenode(c.oid)
         WHERE c.relname = 'items_embedding_idx') AS items_embedding_idx_buffers,
        (SELECT count(*) * current_setting('block_size')::int / 1024 
         FROM pg_buffercache b
         JOIN pg_class c ON b.relfilenode = pg_relation_filenode(c.oid)
         WHERE c.relname = 'items_embedding_idx') AS items_embedding_idx_buffer_size_kb
    FROM pg_stat_statements
    WHERE query LIKE '%SELECT id, embedding %'
) TO STDOUT WITH CSV HEADER;