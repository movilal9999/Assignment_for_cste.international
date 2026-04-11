from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ShopBase(BaseModel):
    name: str
    address: str
    lat: float
    lon: float
    phone: str

class ItemBase(BaseModel):
    name: str

class ShopItemResponse(BaseModel):
    shop_id: int
    shop_name: str
    address: str
    phone: str
    price: float
    distance_km: float
    last_updated: datetime
    whatsapp_link: str

class SearchResponse(BaseModel):
    item: str
    results: List[ShopItemResponse]

class ShopItemCreate(BaseModel):
    shop_id: int
    item_id: int
    price: float