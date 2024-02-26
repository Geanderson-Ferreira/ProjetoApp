from sqlalchemy import create_engine
from starlette_admin.contrib.sqla import Admin
from src.db_manager.models import *
from src.db_manager.config import DATABASE, ENGINE
from starlette_admin.contrib.sqla import Admin, ModelView

#Models a serem registradas no admin dash
models = [OrderType, OrderStatus, Location, LocationType, Hotel, Order, User]

engine = create_engine(DATABASE, connect_args={"check_same_thread": False})
admin = Admin(ENGINE)
for model in models:
    admin.add_view(ModelView(model))
