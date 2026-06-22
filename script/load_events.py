from psycopg2.extras import execute_values
import psycopg2
import json
import sys
import timeit

def insert_raw(data):
    DB = dict(host="localhost", port=5432, dbname="events", user="master", password="master")    
    conn = psycopg2.connect(**DB)
    query = """
            INSERT INTO raw_events (event_id, payload)
            VALUES %s
            ON CONFLICT (event_id)
            DO NOTHING
            """
    argslist = [(d["event_id"], json.dumps(d)) for d in data]
    cnt = len(data)

    try:
        with conn.cursor() as cur:
            execute_values(cur, query, argslist, template="(%s, %s::jsonb)", page_size=1000)
            conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        print(e, file=sys.stderr)
        return None
    finally:
        conn.close()

    return cnt
