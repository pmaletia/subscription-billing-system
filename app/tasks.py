from datetime import date, timedelta
from .celery_worker import celery_app
from .database import SessionLocal
from .models import Subscription, Invoice, StatusEnum

@celery_app.task
def generate_invoices():
    db = SessionLocal()
    today = date.today()
    subs = db.query(Subscription).filter(Subscription.start_date == today).all()
    for sub in subs:
        invoice = Invoice(
            user_id=sub.user_id,
            plan_id=sub.plan_id,
            amount=sub.plan.price,
            issue_date=today,
            due_date=today + timedelta(days=7),
            status=StatusEnum.active
        )
        db.add(invoice)
    db.commit()
    db.close()

@celery_app.task
def mark_overdue_invoices():
    db = SessionLocal()
    today = date.today()
    overdue = db.query(Invoice).filter(Invoice.due_date < today, Invoice.status == StatusEnum.pending).all()
    for invoice in overdue:
        invoice.status = StatusEnum.expired
    db.commit()
    db.close()

@celery_app.task
def send_reminders():
    db = SessionLocal()
    pending = db.query(Invoice).filter(Invoice.status == StatusEnum.expired).all()
    for invoice in pending:
        print(f"Reminder: Invoice {invoice.id} for User {invoice.user_id} is still unpaid.")
    db.close()
