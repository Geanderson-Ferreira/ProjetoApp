from fastapi import APIRouter, Depends, status
from src.schemas.order import OrderSchema, FilterOrderSchema, OrderTypeSchema
from sqlalchemy.orm import Session
from src.db_manager.depends import get_db_session
from src.db_manager.methods.order_methods import OrderMethods
from fastapi.responses import JSONResponse
from src.db_manager.config import API_PREFIX
from src.db_manager.depends import token_verifier

router = APIRouter(prefix=API_PREFIX + '/order')#, dependencies=[Depends(token_verifier)])

@router.get('/list-orders')
def list_orders(orderfilter: FilterOrderSchema = Depends(FilterOrderSchema), db_session: Session = Depends(get_db_session)):
    
    return OrderMethods(db_session).query_orders(orderfilter)

@router.post('/insert-order')
def insert_order(order: OrderSchema, db_session: Session = Depends(get_db_session)):

    OrderMethods(db_session).insert_order(order)

    return JSONResponse(
        content={'msg':'success'},
        status_code=status.HTTP_201_CREATED
    )

@router.get('/orders-types-summarized')
def orders_types_summarized(db_session: Session = Depends(get_db_session)):

    return OrderMethods(db_session).query_orders_summarized()
    
@router.post('/set-order-status')
def set_order_status(order_id: int, set_to_status: int, db_session: Session = Depends(get_db_session)):
    
    OrderMethods(db_session).set_status(order_id, set_to_status)

    return JSONResponse(
        content={'msg':'success'},
        status_code=status.HTTP_201_CREATED
    )

@router.post('/insert-order-type')
def insert_order_type(order_type: OrderTypeSchema, db_session: Session = Depends(get_db_session)):

    OrderMethods(db_session).insert_order_type(order_type)

    return JSONResponse(
        content={'msg':'success'},
        status_code=status.HTTP_201_CREATED
    )

@router.post('/delete-order-type')
def delete_order_type(order_type_id: int, db_session: Session = Depends(get_db_session)):
    
    OrderMethods(db_session).delete_order_type(order_type_id)

    return JSONResponse(
        content={'msg':'success'},
        status_code=status.HTTP_201_CREATED
    )