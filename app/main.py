from fastapi import FastAPI
from app.api import affiliate

app = FastAPI(title="Affiliate Worker API")

# Include the routers
app.include_router(affiliate.router, prefix="/api/v1", tags=["Affiliate"])

@app.get("/")
def read_root():
    return {"status": "Worker is running with Clean Architecture"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)