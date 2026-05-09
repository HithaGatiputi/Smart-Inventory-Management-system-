"""
Inference Pipeline - Core forecasting logic for Kirana demand prediction.
Handles festival multipliers, weather impact, area-type adjustments, and stockout risk.
"""

import math
from datetime import datetime


FESTIVAL_MULTIPLIERS = {
    "Diwali": 2.25,
    "Holi": 1.8,
    "Eid": 1.9,
    "Navratri": 1.7,
    "Pongal": 1.6,
    "Raksha Bandhan": 1.5,
    "Ganesh Chaturthi": 1.65,
    "Onam": 1.55,
}

AREA_MULTIPLIERS = {
    "family": 1.0,
    "commercial": 1.3,
    "student": 0.85,
    "rural": 0.9,
}

CATEGORY_WEATHER_IMPACT = {
    "Staples": 1.4,
    "Dairy": 0.9,
    "Snacks": 1.2,
    "Beverages": 1.5,
}


class InferencePipeline:

    def run(self, payload: dict) -> dict:
        base = payload.get("units_sold", 40)
        festival = payload.get("festival")
        rain = payload.get("rain", False)
        salary_week = payload.get("salary_week", False)
        ipl_match = payload.get("ipl_match", False)
        area_type = payload.get("area_type", "family")
        category = payload.get("category", "Staples")
        current_stock = payload.get("current_stock", 120)
        days_remaining = payload.get("days_remaining", 3)

        # Calculate multipliers
        festival_mult = FESTIVAL_MULTIPLIERS.get(festival, 1.0)
        weather_mult = CATEGORY_WEATHER_IMPACT.get(category, 1.0) if rain else 1.0
        area_mult = AREA_MULTIPLIERS.get(area_type, 1.0)
        salary_mult = 1.25 if salary_week else 1.0
        ipl_mult = 1.15 if ipl_match else 1.0

        # Combined multiplier
        combined = festival_mult * weather_mult * area_mult * salary_mult * ipl_mult
        final_forecast = round(base * combined, 2)

        # Stockout risk calculation
        daily_demand = final_forecast / max(days_remaining, 1)
        stock_days = current_stock / max(daily_demand, 0.01)

        if stock_days < 1:
            stockout_risk = "CRITICAL"
            risk_score = 0.95
        elif stock_days < 2:
            stockout_risk = "HIGH"
            risk_score = 0.75
        elif stock_days < 4:
            stockout_risk = "MEDIUM"
            risk_score = 0.45
        else:
            stockout_risk = "LOW"
            risk_score = 0.15

        # Cluster assignment (simulated KMeans output)
        cluster = self._assign_cluster(base, combined, risk_score)

        # SHAP-style feature importance
        total_log_mult = math.log(max(combined, 0.01))
        importances = {}
        if festival and festival in FESTIVAL_MULTIPLIERS:
            importances["festival"] = round(math.log(festival_mult) / max(total_log_mult, 0.01), 3)
        if rain:
            importances["weather"] = round(math.log(weather_mult) / max(total_log_mult, 0.01), 3)
        if salary_week:
            importances["salary_week"] = round(math.log(salary_mult) / max(total_log_mult, 0.01), 3)
        if ipl_match:
            importances["ipl_match"] = round(math.log(ipl_mult) / max(total_log_mult, 0.01), 3)
        importances["area_type"] = round(math.log(max(area_mult, 0.01)) / max(total_log_mult, 0.01), 3)

        return {
            "product": payload.get("product", "Unknown"),
            "category": category,
            "cluster": cluster,
            "stockout_risk": stockout_risk,
            "risk_score": round(risk_score, 2),
            "stock_days_remaining": round(stock_days, 1),
            "forecast": {
                "base": base,
                "festival_multiplier": festival_mult,
                "weather_multiplier": weather_mult,
                "area_multiplier": area_mult,
                "salary_multiplier": salary_mult,
                "ipl_multiplier": ipl_mult,
                "combined_multiplier": round(combined, 3),
                "final": final_forecast,
            },
            "explanation": {
                "top_factors": importances,
                "summary": self._generate_summary(
                    payload.get("product", "Product"),
                    final_forecast, base, festival, rain, stockout_risk
                ),
            },
            "recommendation": self._get_recommendation(
                stockout_risk, final_forecast, current_stock, days_remaining
            ),
            "timestamp": datetime.utcnow().isoformat(),
        }

    def _assign_cluster(self, base: float, multiplier: float, risk: float) -> int:
        """Simulated cluster assignment based on demand profile."""
        score = base * multiplier * (1 + risk)
        if score > 200:
            return 0  # High-demand cluster
        elif score > 100:
            return 1  # Medium-demand cluster
        else:
            return 2  # Low-demand cluster

    def _generate_summary(self, product, forecast, base, festival, rain, risk):
        parts = [f"Predicted demand for {product}: {forecast} units (base: {base})."]
        if festival:
            parts.append(f"{festival} festival is driving a significant demand surge.")
        if rain:
            parts.append("Rainy weather is affecting demand patterns.")
        if risk in ("CRITICAL", "HIGH"):
            parts.append(f"⚠️ Stockout risk is {risk} — immediate reorder recommended!")
        return " ".join(parts)

    def _get_recommendation(self, risk, forecast, stock, days):
        if risk == "CRITICAL":
            order_qty = round(forecast * 3 - stock)
            return f"🚨 URGENT: Order {max(order_qty, 0)} units immediately. Stock will deplete before next delivery."
        elif risk == "HIGH":
            order_qty = round(forecast * 2 - stock)
            return f"⚠️ Order {max(order_qty, 0)} units within 24 hours to avoid stockout."
        elif risk == "MEDIUM":
            order_qty = round(forecast * 1.5 - stock)
            return f"📋 Consider ordering {max(order_qty, 0)} units in the next 2 days."
        else:
            return "✅ Stock levels are healthy. No immediate action needed."
