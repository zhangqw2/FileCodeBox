'''
author: zhangquanwei
Date: 2025-03-09 14:41:29
'''
from datetime import datetime
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    account: str = Field(max_length=25, nullable=True)
    name: str = Field(max_length=64, nullable=True)
    employee_id: str = Field(max_length=10, nullable=False)
    deployment: str = Field(max_length=255, nullable=True)
    role_code: str = Field(max_length=25, nullable=False)
    role_name: str = Field(max_length=25, nullable=False)
    status: str = Field(max_length=25, nullable=False)
    is_login: bool = Field(default=False)
    create_at: datetime = Field(default_factory=datetime.utcnow)
    update_at: datetime = Field(default_factory=datetime.utcnow)
