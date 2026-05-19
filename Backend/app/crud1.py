from sqlalchemy.orm import Session
from . import models, Schemas1

def get_item_by_name(db: Session, name: str):
    return db.query(models.Item).filter(models.Item.name.ilike(f"%{name}%")).first()

def get_shop_items_by_item_id(db: Session, item_id: int):
    return db.query(models.ShopItem, models.Shop)\
             .join(models.Shop, models.ShopItem.shop_id == models.Shop.id)\
             .filter(models.ShopItem.item_id == item_id).all()

def create_shop(db: Session, shop: Schemas1.ShopBase):
    db_shop = models.Shop(**shop.dict())
    db.add(db_shop)
    db.commit()
    db.refresh(db_shop)
    return db_shop

#  can be added more CRUD functions later (update price, delete, etc.)