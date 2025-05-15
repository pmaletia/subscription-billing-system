from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models
from app.utils import get_db

router = APIRouter()

@router.post("/")
def create_subscription(user_id: int, plan_id: int, db: Session = Depends(get_db)):
    subscription = models.Subscription(user_id=user_id, plan_id=plan_id)
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription

@router.get("/{user_id}")
def get_subscription_for_user(user_id: int, db: Session = Depends(get_db)):
    subscription = db.query(models.Subscription).filter(
        models.Subscription.user_id == user_id,
    ).first()
    if not subscription:
        return {"error": "Subscription not found"}
    return subscription

@router.get("/{subscription_id}/details")
def get_subscription_details(subscription_id: int, db: Session = Depends(get_db)):
    subscription = db.query(models.Subscription).filter(
        models.Subscription.id == subscription_id,
    ).first()
    if not subscription:
        return {"error": "Subscription not found"}
    return {
        "user_id": subscription.user_id,
        "plan_id": subscription.plan_id,
        "start_date": subscription.start_date,
        "end_date": subscription.end_date,
    }

@router.get("/")
def get_all_subscriptions(db: Session = Depends(get_db)):
    subscriptions = db.query(models.Subscription).all()
    return subscriptions

@router.delete("/{subscription_id}")
def delete_subscription(subscription_id: int, db: Session = Depends(get_db)):
    subscription = db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()
    if not subscription:
        return {"error": "Subscription not found"}
    db.delete(subscription)
    db.commit()
    return {"message": "Subscription deleted successfully"}
