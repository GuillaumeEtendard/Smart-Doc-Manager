from sqlalchemy.orm import Session
from sqlalchemy import desc

import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_password = user.password
    db_user = models.User(email=user.email, password=fake_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, type: str, skip: int = 0, limit: int = 100):
    return db.query(models.Item).filter(models.Item.type == type).order_by(desc(models.Item.date)).offset(skip).limit(
        limit).all()


def get_all_items(db: Session):
    return db.query(models.Item).all()


def get_item(db: Session, id: int):
    return db.query(models.Item).filter(models.Item.id == id).first()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_user_item_dict(db: Session, item: dict, user_id: int):
    db_item = models.Item(**item, owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_total(db: Session, type: str):
    return db.query(models.Item).filter(models.Item.type == type).count()
