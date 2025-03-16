'''
author: zhangquanwei
Date: 2025-03-09 22:07:55
'''
from sqlmodel import Session
from .models import Approval

def create_approval(session: Session, approval: Approval):
    approval.state = "审批中"
    session.add(approval)
    session.commit()
    session.refresh(approval)
    return approval

def get_approval(session: Session, approval_id: int, flow_id: int):
    return session.query(Approval).filter(Approval.id == approval_id, Approval.flow_id == flow_id).first()

def get_approvals(session: Session, page: int, size: int, keyword: str):
    query = session.query(Approval)
    if keyword:
        query = query.filter(Approval.name.contains(keyword))
    total = query.count()
    approvals = query.order_by(Approval.create_at.desc()).offset((page - 1) * size).limit(size).all()
    return approvals, total

def update_approval(session: Session, approval_id: int, flow_id: int, approval_data: dict):
    approval = get_approval(session, approval_id, flow_id)
    if approval:
        for key, value in approval_data.items():
            setattr(approval, key, value)
        session.commit()
        session.refresh(approval)
    return approval

def delete_approval(session: Session, approval_id: int, flow_id: int):
    approval = get_approval(session, approval_id, flow_id)
    if approval:
        session.delete(approval)
        session.commit()
        return True
    return False
