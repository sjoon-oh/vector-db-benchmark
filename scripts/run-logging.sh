#!/bin/bash

# PGPASSWORD=passwd psql -h localhost -p 5432 -U postgres -c "\COPY vector_query_metrics TO '${output_file}' CSV HEADER"

time_stamp=$(date +"%Y-%m-%d_%H-%M-%S")
output_file="./log-${time_stamp}.csv"

run_task() {

    PGPASSWORD=passwd psql -h localhost -p 5432 -U postgres -c "SELECT pg_stat_statements(true)" \
        | grep "AS _score FROM items ORDER BY _score LIMIT" \
        > "/tmp/temporary-log.csv"

    log_string="$(cat /tmp/temporary-log.csv)"
    append_string="$(date +"%H:%M:%S"),$log_string"
    echo "$append_string" >> ./log-${time_stamp}-statement.csv

    PGPASSWORD=passwd psql -h localhost -p 5432 -U postgres -c "SELECT pg_buffercache_summary()" \
        >> "./log-${time_stamp}-buffercache-summary.csv"  

    # buffers_used int4
    #     Number of used shared buffers

    # buffers_unused int4
    #     Number of unused shared buffers

    # buffers_dirty int4
    #     Number of dirty shared buffers

    # buffers_pinned int4
    #     Number of pinned shared buffers

    # usagecount_avg float8
    #     Average usage count of used shared buffers

    PGPASSWORD=passwd psql -h localhost -p 5432 -U postgres -c "SELECT pg_buffercache_usage_counts()" \
        >> "./log-${time_stamp}-buffercache-usecnt.csv"

    # usage_count int4
    #     A possible buffer usage count

    # buffers int4
    #     Number of buffers with the usage count

    # dirty int4
    #     Number of dirty buffers with the usage count

    # pinned int4
    #     Number of pinned buffers with the usage count


stop_script=false

# clear_table_if_exists
while true; do

    run_task
    sleep 0.5
done

