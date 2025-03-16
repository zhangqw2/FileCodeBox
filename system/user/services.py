'''
author: zhangquanwei
Date: 2025-03-09 11:35:34
'''
from sqlalchemy import func
from sqlmodel import Session, select
from .models import User
from .schemas import UserCreate, UserUpdate

def get_user(db: Session, user_id: int):
    return db.get(User, user_id)


# services.py 示例
def get_users(db: Session, keyword=None, page=1, size=10):
    offset = (page - 1) * size
    stmt = select(User)
    if keyword:
        stmt = stmt.where(User.name.like(f"%{keyword}%"))
    total = db.scalar(select(func.count()).select_from(stmt.subquery()))
    users = db.execute(stmt.offset(offset).limit(size)).scalars().all()
    return users, total


def create_user(db: Session, user: UserCreate):
    db_user = User.from_orm(user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = db.get(User, user_id)
    if not db_user:
        return None
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.get(User, user_id)
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user

def get_password_by_account(db: Session, account: str):
    stmt = select(User.password).where(User.account == account)
    result = db.execute(stmt).scalar_one_or_none()
    return result

def update_is_login_by_account(db: Session, account: str, is_login: bool):
    stmt = select(User).where(User.account == account)
    db_user = db.execute(stmt).scalar_one_or_none()
    if not db_user:
        return None
    db_user.is_login = is_login
    db.commit()
    db.refresh(db_user)
    return db_user

def count_logged_in_users(db: Session):
    stmt = select(func.count()).where(User.is_login == True)
    total_logged_in = db.scalar(stmt)
    return total_logged_in

def get_user_by_account(db: Session, account: str):
    stmt = select(User).where(User.account == account)
    user = db.execute(stmt).scalar_one_or_none()
    return user
