'''
author: zhangquanwei
Date: 2025-03-09 21:43:48
'''
from typing import Optional, Tuple

from sqlmodel import Session, select
from .models import Flow

def create_flow(session: Session, flow: Flow) -> Flow:
    session.add(flow)
    session.commit()
    session.refresh(flow)
    return flow

def get_flow(session: Session, flow_id: int) -> Optional[Flow]:
    return session.get(Flow, flow_id)

def build_flow_query(session: Session, keyword: str = '') -> select:
    """构建Flow查询语句"""
    statement = select(Flow).order_by(Flow.create_at.desc())  # 按创建时间倒排
    if keyword:
        statement = statement.where(Flow.name.contains(keyword))
    return statement

def get_flows(session: Session, keyword: str = '', page: int = 1, size: int = 10) -> Tuple[list[Flow], int]:
    # 构建基础查询
    statement = build_flow_query(session, keyword)
    
    # 总数查询
    total_statement = statement  # 直接复用基础查询
    total = len(session.exec(total_statement).all())  # 使用len计算总数
    
    # 分页逻辑
    offset = (page - 1) * size
    statement = statement.offset(offset).limit(size)
    flows = session.exec(statement).all()
    
    return flows, total

def update_flow(session: Session, flow_id: int, flow_data: dict) -> Optional[Flow]:
    flow = session.get(Flow, flow_id)
    if not flow:
        return None
    for key, value in flow_data.items():
        setattr(flow, key, value)
    session.commit()
    session.refresh(flow)
    return flow

def delete_flow(session: Session, flow_id: int) -> bool:
    flow = session.get(Flow, flow_id)
    if not flow:
        return False
    session.delete(flow)
    session.commit()
    return True
