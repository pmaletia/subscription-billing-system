from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models
from app.utils import get_db

router = APIRouter()

@router.post("/")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    user = models.User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
