import psycopg2
import os
import time
from datetime import datetime

# Database Configuration
DB_HOST = 'database_host'
DB_NAME = 'database_name'
DB_USER = 'database_user'
DB_PASSWORD = 'database_password'

# Data Directory
DATA_DIR = 'wx_data'

def ingest_data(cursor, file_path):
    station_id = os.path.basename(file_path).split('.')[0]
    rows_inserted = 0

    with open(file_path, 'r') as file:
        for line in file:
            date, max_temp, min_temp, precip = line.strip().split('\t')
            if '-9999' in (max_temp, min_temp, precip):
                continue  # Skip rows with missing data

            try:
                cursor.execute(
                    """
                    INSERT INTO weather_data (station_id, date, max_temperature, min_temperature, precipitation)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (station_id, date) DO NOTHING;  
                    """,
                    (station_id, date, int(max_temp), int(min_temp), int(precip))
                )
                rows_inserted += 1
            except psycopg2.Error as e:
                print(f"Error inserting data from {file_path}: {e}")
    
    return rows_inserted


if __name__ == "__main__":
    start_time = datetime.now()
    print(f"Ingestion started at: {start_time}")

    try:
        with psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cur:
                total_rows_inserted = 0
                for filename in os.listdir(DATA_DIR):
                    if filename.endswith('.txt'):
                        file_path = os.path.join(DATA_DIR, filename)
                        rows_inserted = ingest_data(cur, file_path)
                        total_rows_inserted += rows_inserted
                        print(f"Ingested {rows_inserted} rows from {filename}")

    except psycopg2.Error as e:
        print(f"Database error: {e}")
    finally:
        end_time = datetime.now()
        print(f"Ingestion completed at: {end_time}")
        print(f"Total rows ingested: {total_rows_inserted}")
        print(f"Total time elapsed: {end_time - start_time}")
