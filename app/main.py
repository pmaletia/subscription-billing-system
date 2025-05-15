from fastapi import FastAPI
from .database import Base, engine
from .routes import user, subscription, invoice, plans

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router, prefix="/users")
app.include_router(subscription.router, prefix="/subscriptions")
app.include_router(invoice.router, prefix="/invoices")
app.include_router(plans.router, prefix="/plans")
