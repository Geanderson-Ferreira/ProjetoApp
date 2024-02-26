from src.routers.hotel_routers import router as hotel_router
from src.routers.location_routers import router as location_router
from src.routers.order_routers import router as order_router
from src.routers.user_routers import router as user_router

routers = [
    user_router,
    hotel_router,
    location_router,
    order_router
]
