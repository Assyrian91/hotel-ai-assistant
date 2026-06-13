from sqlalchemy import text
from app.database import SessionLocal
from datetime import date, timedelta

def query_sql(question: str) -> str:
    """Direct SQL query approach without agent toolkit"""
    db = SessionLocal()
    try:
        question_lower = question.lower()
        
        if "revenue" in question_lower and "month" in question_lower:
            result = db.execute(text("""
                SELECT ROUND(SUM(total_revenue), 2) as total
                FROM revenue WHERE date >= date('now', '-30 days')
            """)).fetchone()
            return f"Total revenue for the last 30 days: ${result[0] or 0}"
        
        elif "occupancy" in question_lower:
            result = db.execute(text("""
                SELECT ROUND(AVG(CAST(occupied_rooms AS FLOAT) / total_rooms * 100), 1) as occ
                FROM revenue WHERE date >= date('now', '-7 days')
            """)).fetchone()
            return f"Current occupancy rate (last 7 days): {result[0] or 0}%"
        
        elif "pricing" in question_lower or "price" in question_lower:
            result = db.execute(text("""
                SELECT ROUND(AVG(CAST(occupied_rooms AS FLOAT) / total_rooms * 100), 1) as occ
                FROM revenue WHERE date = date('now')
            """)).fetchone()
            occupancy = result[0] or 72
            if occupancy >= 90:
                suggestion = "INCREASE rates by 20%"
            elif occupancy >= 75:
                suggestion = "INCREASE rates by 8%"
            elif occupancy >= 55:
                suggestion = "MAINTAIN current rates"
            elif occupancy >= 40:
                suggestion = "DECREASE rates by 10%"
            else:
                suggestion = "DISCOUNT rates by 20% - activate promotions"
            return f"Pricing recommendation: {suggestion} (Current occupancy: {occupancy}%)"
        
        elif "nationalities" in question_lower or "guest" in question_lower:
            rows = db.execute(text("""
                SELECT g.nationality, COUNT(*) as cnt
                FROM bookings b JOIN guests g ON b.guest_id = g.id
                WHERE b.status != 'cancelled'
                GROUP BY g.nationality ORDER BY cnt DESC LIMIT 5
            """)).fetchall()
            if rows:
                result_str = "Top 5 guest nationalities:\n"
                for nat, cnt in rows:
                    result_str += f"- {nat}: {cnt} bookings\n"
                return result_str
            return "No guest data available"
        
        else:
            return "I can answer questions about revenue, occupancy, pricing recommendations, and guest nationalities. Please ask about one of these topics."
    
    except Exception as e:
        return f"Database query error: {str(e)}"
    finally:
        db.close()
