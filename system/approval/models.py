'''
author: zhangquanwei
Date: 2025-03-09 22:07:48
'''
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import random

class Approval(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    flow_id: int = Field(description="流程id")
    create_by: Optional[str] = Field(default=None, max_length=64, description="创建人")
    create_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="创建时间")
    update_by: Optional[str] = Field(default=None, max_length=64, description="更新人")
    update_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="更新时间")
    state: Optional[str] = Field(default=None, max_length=10, description="审批状态")
    export_project: Optional[str] = Field(default=None, max_length=255, description="导出项目")
    export_content: Optional[str] = Field(default=None, max_length=255, description="导出内容")
    sensitive_info: Optional[str] = Field(default=None, max_length=255, description="敏感信息")
    export_purpose: Optional[str] = Field(default=None, max_length=255, description="导出目的")
    remark: Optional[str] = Field(default=None, max_length=255, description="备注")
    flow_no: str = Field(default_factory=lambda: datetime.utcnow().strftime('%Y%m%d%H') + str(random.randint(1, 99)).zfill(2), max_length=14, description="审批编号")
