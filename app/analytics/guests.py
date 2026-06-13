from sqlalchemy import text
from app.database import SessionLocal

def get_guest_analytics() -> dict:
    db = SessionLocal()
    nationality = db.execute(text("""
        SELECT g.nationality, COUNT(*) as cnt
        FROM bookings b JOIN guests g ON b.guest_id = g.id
        WHERE b.status != 'cancelled'
        GROUP BY g.nationality ORDER BY cnt DESC LIMIT 5
    """)).fetchall()

    loyalty = db.execute(text("""
        SELECT loyalty_tier, COUNT(*) as cnt FROM guests GROUP BY loyalty_tier
    """)).fetchall()

    stats = db.execute(text("""
        SELECT 
            ROUND(AVG(julianday(check_out) - julianday(check_in)), 1) as avg_stay,
            COUNT(CASE WHEN status = 'cancelled' THEN 1 END) * 100.0 / COUNT(*) as cancel_rate,
            COUNT(*) as total_bookings
        FROM bookings
    """)).fetchone()
    db.close()

    return {
        "top_nationalities": [{"nationality": r[0], "count": r[1]} for r in nationality],
        "loyalty_distribution": {r[0]: r[1] for r in loyalty},
        "avg_stay_days": stats[0] or 0,
        "cancellation_rate_pct": round(stats[1] or 0, 1),
        "total_bookings": stats[2] or 0
    }
