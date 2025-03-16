'''
author: zhangquanwei
Date: 2025-03-09 19:48:42
'''
from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

from core.response import APIResponse
from ..database import engine
from .models import Role
from .schemas import RoleCreate, RoleRead, RoleUpdate

role_api = APIRouter(prefix="/roles", tags=["角色管理"])

@role_api.post("/add/", response_model=RoleRead)
def create_role(role: RoleCreate):
    with Session(engine) as session:
        db_role = Role.from_orm(role)
        session.add(db_role)
        session.commit()
        session.refresh(db_role)
        return db_role

@role_api.get("/detail/{role_id}", response_model=RoleRead)
def read_role(role_id: int):
    with Session(engine) as session:
        role = session.get(Role, role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        return role


from typing import List
from sqlmodel import select
from sqlmodel.sql.expression import Select, SelectOfScalar
from sqlmodel.ext.asyncio.session import AsyncSession  # 如果使用异步需导入
from sqlmodel import Session, func


@role_api.get("/list/")
def read_role_list(
        page: int = 1,
        size: int = 10,
        keyword: str = None
):
    with Session(engine) as session:
        stmt = select(Role)

        # 关键字过滤（假设过滤name字段）
        if keyword:
            stmt = stmt.where(Role.name.like(f"%{keyword}%"))

        # 分页处理
        total = session.scalar(select(func.count('*')).select_from(stmt.subquery()))
        offset = (page - 1) * size
        stmt = stmt.offset(offset).limit(size)

        roles = session.exec(stmt).all()
        return APIResponse(detail={
            "data": roles,
            "total": total,
            "page": page,
            "size": size
        })


@role_api.put("/edit/{role_id}", response_model=RoleRead)
def update_role(role_id: int, role: RoleUpdate):
    with Session(engine) as session:
        db_role = session.get(Role, role_id)
        if not db_role:
            raise HTTPException(status_code=404, detail="Role not found")
        for key, value in role.dict().items():
            setattr(db_role, key, value)
        session.add(db_role)
        session.commit()
        session.refresh(db_role)
        return db_role

@role_api.delete("/delete/{role_id}")
def delete_role(role_id: int):
    with Session(engine) as session:
        role = session.get(Role, role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        session.delete(role)
        session.commit()
        return {"ok": True}
