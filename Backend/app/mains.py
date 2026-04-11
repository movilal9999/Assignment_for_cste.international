from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from . import models, Schemas1, crud1, databases1, utilss

app = FastAPI(title="InstantMarket API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables automatically
models.Base.metadata.create_all(bind=databases1.engine)

def seed_database():
    db: Session = next(databases1.get_db())
    # Check if data already exists
    if db.query(models.Item).first() is None:
        print("Database is empty → Running automatic seed...")

        # Clear old data (safe)
        db.query(models.ShopItem).delete()
        db.query(models.Item).delete()
        db.query(models.Shop).delete()
        db.commit()

        # Add Shops
        shops = [
            ("Stationery King", "Lajpat Nagar, Delhi", 28.5678, 77.2400, "9876543210"),
            ("Market Hub", "Karol Bagh, Delhi", 28.6515, 77.1900, "9876543211"),
            ("Notebook Palace", "Connaught Place, Delhi", 28.6300, 77.2180, "9876543212"),
            ("Local Stationery", "Saket, Delhi", 28.5200, 77.2200, "9876543213"),
            ("Paper World", "Dwarka, Delhi", 28.5800, 77.0500, "9876543214"),
        ]
        for name, address, lat, lon, phone in shops:
            shop = models.Shop(name=name, address=address, lat=lat, lon=lon, phone=phone)
            db.add(shop)
        db.commit()

        # Add Items
        items = ["A4 notebook", "A4 notebook 100 pages", "notebook", "pen", "file folder", "A4 paper"]
        for item_name in items:
            item = models.Item(name=item_name)
            db.add(item)
        db.commit()

        # Link Items to Shops
        shop_items_data = [(1,1,45),(1,2,50),(2,1,40),(3,1,48),(4,1,42),(5,1,47),(1,6,35)]
        for shop_id, item_id, price in shop_items_data:
            shop_item = models.ShopItem(shop_id=shop_id, item_id=item_id, price=price)
            db.add(shop_item)
        db.commit()

        print("Automatic seeding completed successfully!")
    else:
        print("Database already has data - skipping seed")

# Run seed when server starts
seed_database()

@app.get("/search", response_model=Schemas1.SearchResponse)
def search_items(item_name: str, user_lat: float, user_lon: float, db: Session = Depends(databases1.get_db)):
    item = crud1.get_item_by_name(db, item_name)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found in our databases1")

    shop_items = crud1.get_shop_items_by_item_id(db, item.id)
    results = []
    for shop_item, shop in shop_items:
        distance_km = utilss.haversine(user_lat, user_lon, shop.lat, shop.lon)
        whatsapp_link = f"https://wa.me/{shop.phone}?text=Hi,%20I%20need%20{item.name}%20at%20₹{shop_item.price}.%20I'm%20near%20your%20shop%20({distance_km:.1f}km%20away).%20Can%20we%20bargain?"

        results.append(Schemas1.ShopItemResponse(
            shop_id=shop.id,
            shop_name=shop.name,
            address=shop.address,
            phone=shop.phone,
            price=shop_item.price,
            distance_km=round(distance_km, 2),
            last_updated=shop_item.last_updated,
            whatsapp_link=whatsapp_link
        ))

    results.sort(key=lambda x: (x.price + x.distance_km * 8))
    return Schemas1.SearchResponse(item=item.name, results=results[:15])

