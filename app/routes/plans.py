from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models
from app.utils import get_db

router = APIRouter()

@router.post("/")
def create_plan(name: str, price: float, db: Session = Depends(get_db)):
    plan = models.Plan(name=name, price=price)
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan

@router.get("/{plan_id}")
def get_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(models.Plan).filter(models.Plan.id == plan_id).first()
    if not plan:
        return {"error": "Plan not found"}
    return plan

@router.get("/")
def get_all_plans(db: Session = Depends(get_db)):
    plans = db.query(models.Plan).all()
    return plans

@router.delete("/{plan_id}")
def delete_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(models.Plan).filter(models.Plan.id == plan_id).first()
    if not plan:
        return {"error": "Plan not found"}
    db.delete(plan)
    db.commit()
    return {"message": "Plan deleted successfully"}
