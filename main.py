from fastapi import FastAPI
from database.connection import create_tables
from routes.users import user_router
from routes.auths import auth_router
import uvicorn

app = FastAPI()

app.include_router(user_router, prefix="api/users")
app.include_router(auth_router, prefix="api/auth")

@app.on_event("startup")
def on_startup():
    create_tables()

    
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)