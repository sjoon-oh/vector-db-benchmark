SET max_parallel_workers = 32;
SET max_parallel_maintenance_workers = 32;

CREATE INDEX CONCURRENTLY items_hnsw_idx 
ON items 
USING hnsw (embedding vector_l2_ops) 
WITH (m = 16, ef_construction = 256);