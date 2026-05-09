"""
API Routes - Core endpoints for the Kirana AI Platform.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from services.inference_pipeline import InferencePipeline

router = APIRouter()
pipeline = InferencePipeline()


class PredictRequest(BaseModel):
    product: str = "Sugar"
    category: str = "Staples"
    units_sold: float = 40
    current_stock: float = 120
    days_remaining: int = 3
    rain: bool = False
    salary_week: bool = False
    ipl_match: bool = False
    festival: Optional[str] = None
    area_type: str = "family"


@router.get("/api/health")
def health():
    """Health check endpoint for deployment probes."""
    return {"status": "healthy", "service": "kirana-ai-platform", "version": "1.0.0"}


@router.post("/api/predict")
def predict(payload: PredictRequest):
    """Run demand forecast prediction."""
    return pipeline.run(payload.model_dump())


@router.get("/api/festivals")
def get_festivals():
    """Return list of supported Indian festivals with multipliers."""
    return {
        "festivals": [
            {"name": "Diwali", "multiplier": 2.25, "category": "Major"},
            {"name": "Holi", "multiplier": 1.8, "category": "Major"},
            {"name": "Eid", "multiplier": 1.9, "category": "Major"},
            {"name": "Navratri", "multiplier": 1.7, "category": "Medium"},
            {"name": "Pongal", "multiplier": 1.6, "category": "Medium"},
            {"name": "Raksha Bandhan", "multiplier": 1.5, "category": "Medium"},
            {"name": "Ganesh Chaturthi", "multiplier": 1.65, "category": "Medium"},
            {"name": "Onam", "multiplier": 1.55, "category": "Medium"},
        ]
    }


@router.get("/api/products")
def get_products():
    """Return sample product catalog."""
    return {
        "products": [
            {"name": "Sugar", "category": "Staples", "base_units": 40},
            {"name": "Rice (5kg)", "category": "Staples", "base_units": 55},
            {"name": "Atta (10kg)", "category": "Staples", "base_units": 35},
            {"name": "Cooking Oil", "category": "Staples", "base_units": 30},
            {"name": "Milk (500ml)", "category": "Dairy", "base_units": 80},
            {"name": "Curd", "category": "Dairy", "base_units": 45},
            {"name": "Biscuits", "category": "Snacks", "base_units": 60},
            {"name": "Chips", "category": "Snacks", "base_units": 50},
            {"name": "Tea (250g)", "category": "Beverages", "base_units": 25},
            {"name": "Cold Drinks", "category": "Beverages", "base_units": 70},
        ]
    }
