import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from faker import Faker
from datetime import date, timedelta
import random
from app.database import create_tables, SessionLocal, Room, Guest, Booking, Revenue

fake = Faker()
random.seed(42)

ROOM_TYPES = {
    "standard": {"price": 120, "count": 20},
    "deluxe":   {"price": 200, "count": 20},
    "suite":    {"price": 380, "count": 10},
}
NATIONALITIES = ["American", "British", "French", "German", "Japanese", "Emirati", "Saudi", "Indian", "Chinese", "Australian"]


def seed():
    create_tables()
    db = SessionLocal()

    # Rooms
    rooms = []
    room_num = 101
    for rtype, info in ROOM_TYPES.items():
        for i in range(info["count"]):
            floor = room_num // 100
            room = Room(
                room_number=str(room_num),
                room_type=rtype,
                floor=floor,
                base_price=info["price"],
                max_occupancy=2 if rtype != "suite" else 4,
                amenities="WiFi, AC, TV, Minibar" + (", Jacuzzi, Balcony" if rtype == "suite" else "")
            )
            rooms.append(room)
            room_num += 1
            if room_num % 100 == 21:
                room_num = (floor + 1) * 100 + 1
    db.add_all(rooms)
    db.commit()

    # Guests
    guests = []
    for _ in range(200):
        tier = random.choices(["standard", "silver", "gold"], weights=[60, 30, 10])[0]
        g = Guest(
            name=fake.name(),
            email=fake.unique.email(),
            nationality=random.choice(NATIONALITIES),
            phone=fake.phone_number(),
            loyalty_tier=tier,
            total_stays=random.randint(1, 20)
        )
        guests.append(g)
    db.add_all(guests)
    db.commit()

    # Bookings (last 12 months)
    rooms_db = db.query(Room).all()
    guests_db = db.query(Guest).all()
    today = date.today()

    bookings = []
    for _ in range(600):
        check_in = today - timedelta(days=random.randint(0, 365))
        stay = random.randint(1, 7)
        check_out = check_in + timedelta(days=stay)
        room = random.choice(rooms_db)
        seasonal = 1.2 if check_in.month in [6, 7, 8, 12] else 1.0
        rate = round(room.base_price * seasonal * random.uniform(0.9, 1.3), 2)
        status = "checked_out" if check_out < today else random.choice(["confirmed", "checked_in"])
        b = Booking(
            guest_id=random.choice(guests_db).id,
            room_id=room.id,
            check_in=check_in,
            check_out=check_out,
            status=status,
            nightly_rate=rate,
            total_amount=round(rate * stay, 2),
            num_guests=random.randint(1, room.max_occupancy),
            special_requests=random.choice(["", "Late check-in", "Extra pillows", "Sea view preferred", ""])
        )
        bookings.append(b)
    db.add_all(bookings)
    db.commit()

    # Revenue records (daily, last 12 months)
    revenue_records = []
    for i in range(365):
        d = today - timedelta(days=i)
        is_weekend = d.weekday() >= 4
        is_peak = d.month in [6, 7, 8, 12]
        base = 4500 if is_peak else 3000
        multiplier = 1.2 if is_weekend else 1.0
        room_rev = round(base * multiplier * random.uniform(0.85, 1.15), 2)
        revenue_records.append(Revenue(
            date=d,
            room_revenue=room_rev,
            food_revenue=round(room_rev * 0.25, 2),
            spa_revenue=round(room_rev * 0.10, 2),
            total_revenue=round(room_rev * 1.35, 2),
            occupied_rooms=random.randint(25, 48),
            total_rooms=50
        ))
    db.add_all(revenue_records)
    db.commit()
    db.close()
    print("✅ Database seeded successfully!")


if __name__ == "__main__":
    seed()
