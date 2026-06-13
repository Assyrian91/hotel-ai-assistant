from fastapi import APIRouter
from app.analytics.revenue import get_revenue_summary, get_daily_revenue
from app.analytics.pricing import get_pricing_suggestion
from app.analytics.guests import get_guest_analytics

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/revenue")
def revenue(days: int = 30):
    return get_revenue_summary(days)

@router.get("/revenue/daily")
def daily_revenue(days: int = 14):
    return get_daily_revenue(days)

@router.get("/pricing")
def pricing():
    return get_pricing_suggestion()

@router.get("/guests")
def guests():
    return get_guest_analytics()
