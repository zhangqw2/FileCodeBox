'''
author: zhangquanwei
Date: 2025-03-09 22:08:07
'''
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, SQLModel
from .models import Approval
from .services import create_approval, get_approval, get_approvals, update_approval, delete_approval
from .schemas import ApprovalCreate, ApprovalRead, ApprovalUpdate
from system.database import engine, get_session
from core.response import APIResponse
from apps.admin.dependencies import ( get_current_user)
from system.flow.services import get_flow  # 新增导入
import json  # 新增导入

approval_api = APIRouter(prefix="/approval", tags=["审批管理"])

@approval_api.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@approval_api.post("/add")
def create_approval_endpoint(approval: ApprovalCreate, session: Session = Depends(get_session), current_user= Depends(get_current_user)):
    approval_model = Approval.from_orm(approval)

    # 根据approval.flow_id查询流程
    flow = get_flow(session, approval.flow_id)
    if not flow:
        raise HTTPException(status_code=404, detail="Flow not found")

    # 获取edgs_str和node_str
    edgs_str = flow.edgs_str
    node_str = flow.node_str
    
    # 格式化打印
    print(f"Edges: {edgs_str}")
    print(f"Nodes: {node_str}")
     
    # 从node_str中获取type值为input的对象节点
    nodes = json.loads(node_str)
    input_nodes = [node for node in nodes if node.get("type") == "input"]
    print(f"Input Nodes: {input_nodes}")

    # 更新节点中的data值
    for node in input_nodes:
        node['data']['label'] = f"{current_user['account']} | {current_user['name']}"
        node['data']['employeeId'] = current_user['account']
        node['data']['employeeName'] = current_user['name']
    print(f"Updated Input Nodes: {input_nodes}")

    # approval_model.create_by = current_user["account"]
    # approval_model.flow_no = f"{approval_model.flow_id}-{approval_model.id}"
    # create_approval(session, approval_model)
    
    return APIResponse(detail=approval_model)

@approval_api.get("/{approval_id}/{flow_id}", response_model=ApprovalRead)
def read_approval(approval_id: int, flow_id: int, session: Session = Depends(get_session)):
    approval = get_approval(session, approval_id, flow_id)
    if not approval:
        raise HTTPException(status_code=404, detail="Approval not found")
    return approval

@approval_api.get("/list")
def read_approvals(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    keyword: str = "",
    session: Session = Depends(get_session)
):
    approvals, total = get_approvals(session, page, size, keyword)
    return APIResponse(
        detail={
            "page": page,
            "size": size,
            "keyword": keyword,
            "data": approvals,
            "total": total,
        }
    )

@approval_api.put("/edit/{approval_id}/{flow_id}", response_model=ApprovalRead)
def update_approval_endpoint(approval_id: int, flow_id: int, approval_data: ApprovalUpdate, session: Session = Depends(get_session)):
    approval_data.update_at = datetime.utcnow()
    approval = update_approval(session, approval_id, flow_id, approval_data.dict(exclude_unset=True))
    if not approval:
        raise HTTPException(status_code=404, detail="Approval not found")
    return approval

@approval_api.delete("/delete/{approval_id}/{flow_id}", response_model=bool)
def delete_approval_endpoint(approval_id: int, flow_id: int, session: Session = Depends(get_session)):
    success = delete_approval(session, approval_id, flow_id)
    if not success:
        raise HTTPException(status_code=404, detail="Approval not found")
    return success
