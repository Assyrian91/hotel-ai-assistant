from sqlalchemy import text
from app.database import SessionLocal
from datetime import date

def get_pricing_suggestion() -> dict:
    db = SessionLocal()
    today = date.today()
    row = db.execute(text("""
        SELECT AVG(CAST(occupied_rooms AS FLOAT) / total_rooms * 100)
        FROM revenue WHERE date = :today
    """), {"today": today}).fetchone()
    occupancy = row[0] or 72.0
    db.close()

    if occupancy >= 90:
        action, pct, reason = "INCREASE", 20, "Very high demand"
    elif occupancy >= 75:
        action, pct, reason = "INCREASE", 8, "Above average demand"
    elif occupancy >= 55:
        action, pct, reason = "MAINTAIN", 0, "Normal demand"
    elif occupancy >= 40:
        action, pct, reason = "DECREASE", 10, "Below average demand"
    else:
        action, pct, reason = "DISCOUNT", 20, "Low demand — activate promotions"

    base_rates = {"standard": 120, "deluxe": 200, "suite": 380}
    suggestions = {
        rtype: round(rate * (1 + pct / 100), 2)
        for rtype, rate in base_rates.items()
    }
    return {
        "current_occupancy_pct": round(occupancy, 1),
        "recommendation": action,
        "adjustment_pct": pct,
        "reason": reason,
        "suggested_rates": suggestions
    }
