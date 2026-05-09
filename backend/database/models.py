
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class Forecast(Base):

    __tablename__ = "forecasts"

    id = Column(Integer, primary_key=True)
    product_name = Column(String)
    forecast_qty = Column(Float)
    stockout_risk = Column(String)
