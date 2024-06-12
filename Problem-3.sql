-- New Data Model (DDL):
-- SQL

CREATE TABLE yearly_weather_summary (
    station_id TEXT NOT NULL,
    year SMALLINT NOT NULL,
    avg_max_temp DECIMAL(5,2),  -- Average max temp in degrees Celsius
    avg_min_temp DECIMAL(5,2),  -- Average min temp in degrees Celsius
    total_precip DECIMAL(8,2),  -- Total precipitation in centimeters

    PRIMARY KEY (station_id, year)
);


-- SQL Query to Calculate Statistics:
-- SQL

INSERT INTO yearly_weather_summary (station_id, year, avg_max_temp, avg_min_temp, total_precip)
SELECT 
    station_id,
    EXTRACT(YEAR FROM date) AS year,
    AVG(max_temperature) / 10.0 AS avg_max_temp,
    AVG(min_temperature) / 10.0 AS avg_min_temp,
    SUM(precipitation) / 100.0 AS total_precip
FROM weather_data
WHERE max_temperature != -9999 AND min_temperature != -9999 AND precipitation != -9999
GROUP BY station_id, year;


-- Python Code to Execute Query:

import psycopg2 

DB_HOST = 'database_host'
DB_NAME = 'database_name'
DB_USER = 'database_user'
DB_PASSWORD = 'database_password'

try:
    with psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO yearly_weather_summary (station_id, year, avg_max_temp, avg_min_temp, total_precip)
                SELECT 
                    station_id,
                    EXTRACT(YEAR FROM date) AS year,
                    AVG(max_temperature) / 10.0 AS avg_max_temp,
                    AVG(min_temperature) / 10.0 AS avg_min_temp,
                    SUM(precipitation) / 100.0 AS total_precip
                FROM weather_data
                WHERE max_temperature != -9999 AND min_temperature != -9999 AND precipitation != -9999
                GROUP BY station_id, year;
                """
            )
            conn.commit()
            print("Yearly weather summary calculated and inserted successfully!")
except psycopg2.Error as e:
    print(f"Database error: {e}")


