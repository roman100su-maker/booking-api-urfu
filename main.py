from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Booking API", docs_url="/docs")

# Данные в памяти
users = []
hotels = [
    {"id": 1, "name": "Гранд Отель", "city": "Москва", "stars": 5},
    {"id": 2, "name": "Спорт Отель", "city": "Екатеринбург", "stars": 4}
]
rooms = [
    {"id": 1, "hotel_id": 1, "room_type": "standard", "price": 5000, "capacity": 2},
    {"id": 2, "hotel_id": 1, "room_type": "premium", "price": 10000, "capacity": 4}
]
bookings = []
flights = [
    {"id": 1, "from_city": "Москва", "to_city": "Екатеринбург", "price": 8000, "available_seats": 50},
    {"id": 2, "from_city": "Москва", "to_city": "Екатеринбург", "price": 12000, "available_seats": 30}
]

class UserRegister(BaseModel):
    email: str
    name: str
    password: str

class BookingCreate(BaseModel):
    user_id: int
    room_id: int
    start_date: str
    end_date: str

@app.get("/")
def home():
    return {"message": "Booking API работает!", "version": "1.0"}

@app.get("/hotels")
def get_hotels(city: Optional[str] = None):
    if city:
        return [h for h in hotels if h["city"].lower() == city.lower()]
    return hotels

@app.get("/rooms")
def get_rooms(hotel_id: Optional[int] = None):
    if hotel_id:
        return [r for r in rooms if r["hotel_id"] == hotel_id]
    return rooms

@app.post("/register")
def register(user: UserRegister):
    user_id = len(users) + 1
    new_user = {"id": user_id, "email": user.email, "name": user.name, "role": "user"}
    users.append(new_user)
    return {"message": "Регистрация успешна", "user_id": user_id}

@app.post("/bookings")
def create_booking(booking: BookingCreate):
    room_exists = any(r["id"] == booking.room_id for r in rooms)
    if not room_exists:
        raise HTTPException(status_code=404, detail="Номер не найден")
    
    booking_id = len(bookings) + 1
    new_booking = {
        "id": booking_id,
        "user_id": booking.user_id,
        "room_id": booking.room_id,
        "start_date": booking.start_date,
        "end_date": booking.end_date
    }
    bookings.append(new_booking)
    return {"message": "Бронь создана", "booking_id": booking_id}

@app.get("/flights")
def search_flights(from_city: str, to_city: str, passengers: int = 1):
    available_flights = [
        f for f in flights 
        if f["from_city"].lower() == from_city.lower() 
        and f["to_city"].lower() == to_city.lower() 
        and f["available_seats"] >= passengers
    ]
    
    if available_flights:
        cheapest = min(available_flights, key=lambda x: x["price"])
        for flight in available_flights:
            flight["is_cheapest"] = flight["id"] == cheapest["id"]
        return available_flights
    return []

if __name__ == "__main__":
    import uvicorn
    print("🚀 Сервер запущен: http://localhost:8000")
    print("📚 Документация: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
