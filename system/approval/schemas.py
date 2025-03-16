'''
author: zhangquanwei
Date: 2025-03-09 22:07:50
'''

from datetime import datetime
from typing import Union

from pydantic import BaseModel

class ApprovalCreate(BaseModel):
    flow_id: int
    create_by: Union[str,None] = None
    state: Union[str,None] = None
    export_project: Union[str,None] = None
    export_content: Union[str,None] = None
    sensitive_info: Union[str,None] = None
    export_purpose: Union[str,None] = None
    remark: Union[str,None] = None

class ApprovalRead(BaseModel):
    id: int
    flow_id: int
    create_by: Union[str,None] = None
    create_at: Union[datetime]
    update_by: Union[str,None] = None
    update_at: Union[datetime]
    state: Union[str,None] = None
    export_project: Union[str,None] = None
    export_content: Union[str,None] = None
    sensitive_info: Union[str,None] = None
    export_purpose: Union[str,None] = None
    remark: Union[str,None] = None
    flow_no: Union[str,None] = None

class ApprovalUpdate(BaseModel):
    update_by: Union[str,None] = None
    update_at: Union[datetime] = datetime.utcnow()
    state: Union[str,None] = None
    export_project: Union[str,None] = None
    export_content: Union[str,None] = None
    sensitive_info: Union[str,None] = None
    export_purpose: Union[str,None] = None
    remark: Union[str,None] = None
    flow_no: Union[str,None] = None
