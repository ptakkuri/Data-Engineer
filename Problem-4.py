# Project Structure:
'''
weather_api/
├── main.py       
├── models.py
├── crud.py
├── database.py
└── tests/
    └── test_main.py
'''


# main.py

from fastapi import FastAPI, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional

from models import WeatherData, YearlyWeatherSummary
from crud import get_weather_data, get_weather_stats, get_db
from database import engine, Base

# Create database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/api/weather", response_model=List[WeatherData])
def read_weather(
    skip: int = 0,
    limit: int = 100,
    station_id: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    weather_data = get_weather_data(db, skip=skip, limit=limit, station_id=station_id, start_date=start_date, end_date=end_date)
    return weather_data

@app.get("/api/weather/stats", response_model=List[YearlyWeatherSummary])
def read_weather_stats(
    skip: int = 0,
    limit: int = 100,
    station_id: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    weather_stats = get_weather_stats(db, skip=skip, limit=limit, station_id=station_id, year=year)
    return weather_stats

@app.get("/", response_class=JSONResponse)
def redirect_to_docs():
    return JSONResponse({"message": "Please navigate to /docs to view the API documentation."})


# models.py

from sqlalchemy import Column, Integer, String, Date, Float
from database import Base

class WeatherData(Base):
    __tablename__ = "weather_data"

    station_id = Column(String, primary_key=True)
    date = Column(Date, primary_key=True)
    max_temperature = Column(Integer)
    min_temperature = Column(Integer)
    precipitation = Column(Integer)

class YearlyWeatherSummary(Base):
    __tablename__ = "yearly_weather_summary"

    station_id = Column(String, primary_key=True)
    year = Column(Integer, primary_key=True)
    avg_max_temp = Column(Float)
    avg_min_temp = Column(Float)
    total_precip = Column(Float)


