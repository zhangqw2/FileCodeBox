'''
author: zhangquanwei
Date: 2025-03-09 19:48:34
'''
from typing import Optional

from sqlmodel import SQLModel, Field

class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    role_code: Optional[str] = Field(max_length=25)
    name: Optional[str] = Field(max_length=32)
