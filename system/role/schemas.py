'''
author: zhangquanwei
Date: 2025-03-09 19:48:36
'''
from pydantic import BaseModel, Field
from typing import Optional
class RoleCreate(BaseModel):
    role_code: str
    name: str

class RoleRead(BaseModel):
    id: int
    role_code: str
    name: str
    class Config:
        orm_mode = True

class RoleUpdate(BaseModel):
    role_code: str
    name: str
