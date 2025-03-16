'''
author: zhangquanwei
Date: 2025-03-09 21:43:59
'''
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, SQLModel
from .models import Flow
from .services import create_flow, get_flow, get_flows, update_flow, delete_flow
from .schemas import FlowCreate, FlowRead, FlowUpdate
from system.database import engine, get_session
from core.response import APIResponse

flow_api = APIRouter(prefix="/flow", tags=["流程管理"])

@flow_api.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@flow_api.post("/add", response_model=FlowRead)
def create_flow_endpoint(flow: FlowCreate, session: Session = Depends(get_session)):
    flow_model = Flow.from_orm(flow)
    return create_flow(session, flow_model)

@flow_api.get("/detail/{flow_id}", response_model=FlowRead)
def read_flow(flow_id: int, session: Session = Depends(get_session)):
    flow = get_flow(session, flow_id)
    if not flow:
        raise HTTPException(status_code=404, detail="Flow not found")
    return flow

@flow_api.get("/list")
def read_flows(
    session: Session = Depends(get_session),
    keyword: str = "",
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1)
):
    flows, total = get_flows(session, keyword=keyword, page=page, size=size)
    return APIResponse(
        detail={
            "page": page,
            "size": size,
            "data": flows,
            "total": total,
            "keyword": keyword
        }
    )

@flow_api.put("/edit/{id}", response_model=FlowRead)
def update_flow_endpoint(id: int, flow_data: FlowUpdate, session: Session = Depends(get_session)):
    flow = update_flow(session, id, flow_data.dict(exclude_unset=True))
    if not flow:
        raise HTTPException(status_code=404, detail="Flow not found")
    return flow

@flow_api.delete("/delete/{id}", response_model=bool)
def delete_flow_endpoint(id: int, session: Session = Depends(get_session)):
    success = delete_flow(session, id)
    if not success:
        raise HTTPException(status_code=404, detail="Flow not found")
    return success
