'''
author: zhangquanwei
Date: 2025-03-07 22:32:24
'''
import datetime
from typing import Optional
from pydantic import BaseModel


class IDData(BaseModel):
    id: int


class ShareItem(BaseModel):
    expire_value: int
    expire_style: str = "day"
    filename: str
    fileName: str


class DeleteItem(BaseModel):
    filename: str


class LoginData(BaseModel):
    account: str
    password: str


class UpdateFileData(BaseModel):
    id: int
    code: Optional[str] = None
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    expired_at: Optional[datetime.datetime] = None
    expired_count: Optional[int] = None
