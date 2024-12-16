import pgvector.psycopg
import psycopg

from benchmark.dataset import Dataset
from engine.base_client import IncompatibilityError
from engine.base_client.configure import BaseConfigurator
from engine.base_client.distances import Distance
from engine.clients.pgvector.config import get_db_config


class PgVectorConfigurator(BaseConfigurator):
    def __init__(self, host, collection_params: dict, connection_params: dict):
        super().__init__(host, collection_params, connection_params)
        self.conn = psycopg.connect(**get_db_config(host, connection_params))
        print("configure connection created")
        self.conn.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        pgvector.psycopg.register_vector(self.conn)

        # 
        # Start of the configuration for system trace
        cur = self.conn.cursor()

        cur.execute("SHOW shared_buffers")
        shared_buffers_out = cur.fetchall()

        cur.execute("SHOW work_mem")
        work_mem_out = cur.fetchall()
        
        cur.execute("SHOW maintenance_work_mem")
        maintenance_work_mem_out = cur.fetchall()

        # 
        cur.execute(f"CREATE EXTENSION IF NOT EXISTS pg_buffercache")
        cur.execute(f"CREATE EXTENSION IF NOT EXISTS pg_stat_statements")
        # cur.execute(f"CREATE EXTENSION IF NOT EXISTS pg_stat_io")

        cur.execute(f"SELECT pg_stat_statements_reset()")

        cur.execute(f"SET track_counts = on")
        cur.execute(f"SET track_io_timing = on")
        

    def clean(self):
        self.conn.execute(
            "DROP TABLE IF EXISTS items CASCADE;",
        )

    def recreate(self, dataset: Dataset, collection_params):
        if dataset.config.distance == Distance.DOT:
            raise IncompatibilityError

        self.conn.execute(
            f"""CREATE TABLE items (
                id SERIAL PRIMARY KEY,
                embedding vector({dataset.config.vector_size}) NOT NULL
            );"""
        )
        self.conn.execute("ALTER TABLE items ALTER COLUMN embedding SET STORAGE PLAIN")
        self.conn.close()

    def delete_client(self):
        self.conn.close()
