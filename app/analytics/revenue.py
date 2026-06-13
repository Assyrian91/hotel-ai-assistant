from sqlalchemy import text
from app.database import SessionLocal
from datetime import date, timedelta

def get_revenue_summary(days: int = 30) -> dict:
    db = SessionLocal()
    since = date.today() - timedelta(days=days)
    result = db.execute(text("""
        SELECT 
            ROUND(SUM(total_revenue), 2) as total_revenue,
            ROUND(AVG(total_revenue), 2) as avg_daily_revenue,
            ROUND(SUM(room_revenue), 2) as room_revenue,
            ROUND(AVG(CAST(occupied_rooms AS FLOAT) / total_rooms * 100), 1) as avg_occupancy_pct,
            ROUND(SUM(room_revenue) / SUM(total_rooms), 2) as revpar
        FROM revenue WHERE date >= :since
    """), {"since": since}).fetchone()
    db.close()
    return {
        "period_days": days,
        "total_revenue": result[0] or 0,
        "avg_daily_revenue": result[1] or 0,
        "room_revenue": result[2] or 0,
        "avg_occupancy_pct": result[3] or 0,
        "revpar": result[4] or 0,
    }

def get_daily_revenue(days: int = 14) -> list:
    db = SessionLocal()
    since = date.today() - timedelta(days=days)
    rows = db.execute(text("""
        SELECT date, total_revenue, occupied_rooms, total_rooms
        FROM revenue WHERE date >= :since ORDER BY date
    """), {"since": since}).fetchall()
    db.close()
    return [{"date": str(r[0]), "revenue": r[1], "occupied": r[2], "total": r[3]} for r in rows]
