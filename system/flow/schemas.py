'''
author: zhangquanwei
Date: 2025-03-09 21:43:50
'''
from typing import Union
from pydantic import BaseModel, Field
from datetime import datetime

class FlowCreate(BaseModel):
    category_code: Union[str,None] = None
    category_name: Union[str,None] = None
    name: str
    node_str: Union[str,None] = None
    edgs_str: Union[str,None] = None
    is_active: Union[bool,None] = True

class FlowRead(BaseModel):
    id: int
    category_code: Union[str,None] = None
    category_name: Union[str,None] = None
    name: str
    node_str: Union[str,None] = None
    edgs_str: Union[str,None] = None
    is_active: Union[bool,None] = True
    create_at: Union[datetime] = None
    update_at: Union[datetime] = None
    version: int

    class Config:
        orm_mode = True

class FlowUpdate(BaseModel):
    category_code: Union[str,None] = None
    category_name: Union[str,None] = None
    name: Union[str,None] = None
    node_str: Union[str,None] = None
    edgs_str: Union[str,None] = None
    is_active: Union[bool,None] = True
    update_at: Union[datetime, None] = Field(default_factory=datetime.now)
    version: Union[int,None] = None
