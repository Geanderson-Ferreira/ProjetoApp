from fastapi import FastAPI, Depends
from src.admin_way.starlette import admin
from src.routers import routers
from src.db_manager.depends import token_verifier

from fastapi import FastAPI

app = FastAPI()

app.title = 'Projeto App Care'
@app.get('/')
def health_check():
    return {"HERE WE ARE!"}

for router in routers: app.include_router(router)


@app.get('/admin', dependencies=[Depends(token_verifier)])
def admin_page():
    return admin.mount_to(app)