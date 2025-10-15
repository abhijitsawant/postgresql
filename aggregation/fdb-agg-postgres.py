import os
import json
import logging
import time
import psycopg2
from psycopg2.extras import execute_values
from multiprocessing import Pool

OUTPUT_DIR = "output2"
LOG_FILE = "log/fdb_postgres.log"

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 5432,
    "dbname": "flowdb",
    "user": "flowuser",
    "password": "flowpass"
}

# -----------------------------
# Logging setup
# -----------------------------
if not os.path.exists("log"):
    os.makedirs("log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(process)d] %(levelname)s: %(message)s"
)

# -----------------------------
# DB connection
# -----------------------------
def get_conn():
    return psycopg2.connect(**DB_CONFIG)

# -----------------------------
# Process a single JSON file
# -----------------------------
def process_file(filepath):
    conn = get_conn()
    cursor = conn.cursor()
    total_flows = 0

    with open(filepath, 'r') as f:
        data_json = json.load(f)
    
    flow_data = data_json.get("data", {})

    for record_key, record in flow_data.items():
        # UPSERT: INSERT or UPDATE
        query = """
        INSERT INTO flow_records 
            (key_bin, b_in, b_out, p_in, p_out, t_bytes, cnt, dev, src_ip, dst_ip, dst_port)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (key_bin)
        DO UPDATE SET
            b_in = flow_records.b_in + EXCLUDED.b_in,
            b_out = flow_records.b_out + EXCLUDED.b_out,
            p_in = flow_records.p_in + EXCLUDED.p_in,
            p_out = flow_records.p_out + EXCLUDED.p_out,
            t_bytes = flow_records.t_bytes + EXCLUDED.t_bytes,
            cnt = flow_records.cnt + EXCLUDED.cnt,
            dev = EXCLUDED.dev,
            src_ip = EXCLUDED.src_ip,
            dst_ip = EXCLUDED.dst_ip,
            dst_port = EXCLUDED.dst_port;
        """
        values = (
            record_key,
            record['bytes_in'],
            record['bytes_out'],
            record['packets_in'],
            record['packets_out'],
            record['total_bytes'],
            record['count'],
            record['device'],
            record['source_ip'],
            record['destination_ip'],
            int(record['destination_port'])
        )
        cursor.execute(query, values)
        total_flows += 1
    
    conn.commit()
    cursor.close()
    conn.close()
    os.remove(filepath)
    return total_flows

# -----------------------------
# Main entry
# -----------------------------
if __name__ == "__main__":
    start_time = time.time()
    files = [os.path.join(OUTPUT_DIR, f) for f in os.listdir(OUTPUT_DIR) if f.endswith(".json")]

    pool = Pool(processes=4)
    flow_counts = pool.map(process_file, files)
    pool.close()
    pool.join()

    total_flows = sum(flow_counts)
    duration = time.time() - start_time
    performance = total_flows/duration if total_flows else 0

    logging.info(f"Indexing finished, total_flows={total_flows}, time_taken={duration:.2f}s, performance={performance:.2f} flows/s")
