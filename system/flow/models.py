'''
author: zhangquanwei
Date: 2025-03-09 21:42:07
'''
from sqlmodel import SQLModel, Field
from sqlalchemy import Text  # 新增导入
from typing import Optional
from datetime import datetime

class Flow(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    category_code: Optional[str] = Field(default=None, max_length=25)
    category_name: Optional[str] = Field(default=None, max_length=30)
    name: str = Field(index=True,unique= True,max_length=64)
    node_str: Optional[str] = Field(default=None)
    edgs_str: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)
    create_at: Optional[datetime] = Field(default_factory=datetime.now)
    update_at: Optional[datetime] = Field(default_factory=datetime.now)
    version: int = Field(default=1)
