from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .database import Base
import enum

class StatusEnum(str, enum.Enum):
    active = "active"
    cancelled = "cancelled"
    expired = "expired"
    pending = "pending"
    paid = "paid"

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)

    subscriptions = relationship("Subscription", back_populates="user")
    invoices = relationship("Invoice", back_populates="user")

class Plan(Base):
    __tablename__ = 'plans'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    price = Column(Integer)

class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    plan_id = Column(Integer, ForeignKey('plans.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(Enum(StatusEnum))

    user = relationship("User", back_populates="subscriptions")
    plan = relationship("Plan")

class Invoice(Base):
    __tablename__ = 'invoices'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    plan_id = Column(Integer, ForeignKey('plans.id'))
    amount = Column(Integer)
    issue_date = Column(Date)
    due_date = Column(Date)
    status = Column(Enum(StatusEnum))

    user = relationship("User", back_populates="invoices")
    plan = relationship("Plan")
