from fastapi import FastAPI
from app.api.routes import tenant,payment


app = FastAPI(title = "Tenant Platform")
app.include_router(tenant.router, prefix="/tenants", tags=["Tenants"])
app.include_router(payment.router, prefix="/payments", tags=["Payments"])


@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/debug")
async def debug():
    return {"ok": True}
