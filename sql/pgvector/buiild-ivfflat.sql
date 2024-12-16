SET max_parallel_workers = 32;
SET max_parallel_maintenance_workers = 32;

CREATE INDEX CONCURRENTLY items_ivfflat_idx 
ON items 
USING ivfflat (embedding vector_l2_ops) 
WITH (lists = 32768);