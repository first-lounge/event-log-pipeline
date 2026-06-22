from psycopg2.extras import execute_values
import psycopg2
import sys

def insert_events(DB: dict):
    conn = psycopg2.connect(**DB)
    data = None

    try:
        with conn.cursor() as cur:
            cur.execute(""" SELECT payload FROM raw_events WHERE processed_at IS NULL""")
            data = cur.fetchall()

        cnts = {}
        events_rows = []
        click_rows = []
        purchase_rows = []
        error_rows = []
        
        for d in data:
            p = d[0]
            events_rows.append((p["event_id"], p["event_type"], p["user_id"], p["event_time"], p["page_name"], p["device"]))

            et = p["event_type"]
            if et == "click":
                click_rows.append((p["event_id"], p["element_type"], p["click_event_name"]))
            elif et == "purchase":
                purchase_rows.append((p["event_id"], p["price"], p["payment_method"], p["product_id"], p["product_name"], p["product_category"]))
            elif et == "error":
                error_rows.append((p["event_id"], p["error_level"], p["error_code"], p["error_msg"]))
        
        cnts["events"] = len(events_rows)
        cnts["click"] = len(click_rows)
        cnts["purchase"] = len(purchase_rows)
        cnts["error"] = len(error_rows)
        
        # 쿼리문
        insert_events_query = """
                INSERT INTO events (event_id, event_type, user_id, event_time, page_name, device)
                VALUES %s
                ON CONFLICT (event_id)
                DO NOTHING
                """
        
        insert_click_query = """
                INSERT INTO click (event_id, element_type, click_event_name)
                VALUES %s
                ON CONFLICT (event_id)
                DO NOTHING
                """
        
        insert_purchase_query = """
                INSERT INTO purchase (event_id, price, payment_method, product_id, product_name, product_category)
                VALUES %s
                ON CONFLICT (event_id)
                DO NOTHING
                """
        
        insert_error_query = """
                INSERT INTO error (event_id, error_level, error_code, error_msg)
                VALUES %s
                ON CONFLICT (event_id)
                DO NOTHING
                """

        update_raw_query = """
                UPDATE raw_events
                SET processed_at = now()
                where processed_at is NULL
                """
        
        with conn.cursor() as cur:
            # INSERT events table 
            execute_values(cur, insert_events_query, events_rows, page_size=1000)
            
            # INSERT click table => 쿼리 수정
            execute_values(cur, insert_click_query, click_rows, page_size=1000)

            # INSERT purchase table => 쿼리 수정
            execute_values(cur, insert_purchase_query, purchase_rows, page_size=1000)

            # INSERT error table => 쿼리 수정
            execute_values(cur, insert_error_query, error_rows, page_size=1000)
            
            # UPDATE raw_events 테이블 
            cur.execute(update_raw_query)
            conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        print(e, file=sys.stderr)
        return None
    finally:
        conn.close()

    return cnts