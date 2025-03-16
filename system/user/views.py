'''
author: zhangquanwei
Date: 2025-03-09 14:41:40
'''
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from .schemas import UserCreate, UserRead, UserUpdate
from .services import get_user, get_users, create_user, update_user, delete_user
from ..database import get_session
from fastapi import Query
from core.response import APIResponse  # 假设与案例中一致的响应类
from typing import Optional

user_api = APIRouter(prefix="/user", tags=["用户管理"])

@user_api.post("/add", response_model=UserRead)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_session)):
    return create_user(db, user)

@user_api.get("/detail/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_session)):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@user_api.get("/list")
def read_users(
    keyword: Optional[str] = None,  # 可选搜索参数
    page: int = Query(1, ge=1, le=100),  # 分页参数约束
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_session)
) :
    """
    分页查询用户列表，支持关键字搜索
    """
    users, total = get_users(db, keyword=keyword, page=page, size=size)
    return APIResponse(detail={
            "data": users,
            "total": total,
            "page": page,
            "size": size
        }
    )


@user_api.put("/edit/{user_id}", response_model=UserRead)
def update_user_endpoint(user_id: int, user: UserUpdate, db: Session = Depends(get_session)):
    db_user = update_user(db, user_id, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@user_api.delete("/delete/{user_id}", response_model=UserRead)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_session)):
    db_user = delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
