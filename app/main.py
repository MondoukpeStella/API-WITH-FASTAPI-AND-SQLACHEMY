from fastapi import FastAPI
import routers  # Assuming you have a users router defined in app/routers/users.py

app = FastAPI( title="EduMaster API",)

app.include_router(routers.router, prefix="/api")
