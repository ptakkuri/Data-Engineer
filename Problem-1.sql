-- Create the weather_data table
CREATE TABLE weather_data (
    station_id TEXT NOT NULL,             -- Identifier for the weather station (e.g., 'NE_OMAHA')
    date DATE NOT NULL,                   -- Date in YYYY-MM-DD format
    max_temperature SMALLINT,            -- Max temperature in tenths of a degree Celsius
    min_temperature SMALLINT,            -- Min temperature in tenths of a degree Celsius
    precipitation SMALLINT,               -- Precipitation in tenths of a millimeter

    PRIMARY KEY (station_id, date)         -- Ensure uniqueness per station per day
);

-- Create an index on the date for efficient querying by date range
CREATE INDEX idx_weather_data_date ON weather_data (date);
