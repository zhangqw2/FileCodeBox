'''
author: zhangquanwei
Date: 2025-03-09 14:41:31
'''
from datetime import datetime
from pydantic import BaseModel
from typing import Union

class UserBase(BaseModel):
    account: Union[str, None] = None
    name: Union[str, None] = None
    employee_id: str
    deployment: Union[str, None] = None
    role_code: Union[str, None] = None
    role_name: Union[str, None] = None
    status: Union[str, None] = None
    is_login: bool = False

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int
    create_at: datetime
    update_at: datetime

    class Config:
        orm_mode = True

class UserUpdate(UserBase):
    pass
