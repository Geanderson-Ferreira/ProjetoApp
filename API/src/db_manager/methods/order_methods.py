from sqlalchemy.orm import joinedload, Session
from sqlalchemy import func, update
from src.db_manager.models import Order, Location, OrderStatus, OrderType, User
from src.schemas.order import OrderSchema, FilterOrderSchema, OrderTypeSchema
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from fastapi import status
from datetime import datetime

class OrderMethods:
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def insert_order(self, order: OrderSchema):

        try:
            order_to_insert = Order(
                LocationId=order.location_id,
                CreationDate=datetime.utcnow(),
                OrderTypeId=order.order_type_id,
                ImageData=bytes(order.image_data, 'utf-8'),
                Description=order.description,
                UserId=order.created_by_id,
                OrderStatusId=order.status_id,
                HotelId=order.hotel_id
            )
        except Exception as erro:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Erro ao processar insertOrder.: {erro}',
                )

        try:
            self.db_session.add(order_to_insert)
            self.db_session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Erro de Integridade do Banco. Verifique os dados que esta tentando inserir.',
            )

    def query_orders_summarized(self):

        try:
            order_counts = (
                self.db_session.query(OrderType.OrderTypeName, func.count(Order.OrderId))
                    .join(Order, OrderType.OrderTypeId == Order.OrderTypeId)
                    .filter(Order.OrderStatusId == 2)
                    .group_by(OrderType.OrderTypeName)
                        .all()
            )

            # Criando um dicionário para armazenar os resultados
            return {"order_counts": [{"OrderTypeName": order_type, "Count": count} for order_type, count in order_counts]}
        except Exception as ERRO:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Erro ao processar queryOrdersSummarized: {ERRO}'
            )

    def query_orders(self, orderFilter: FilterOrderSchema):

        query = (
            self.db_session.query(Order, Location.LocationName, User.Username, OrderStatus.StatusName, OrderType.OrderTypeName)
            .join(Location, Order.LocationId == Location.LocationId)
            .join(OrderType)
            .join(User)
            .join(OrderStatus)
            .options(
                joinedload(Order.Location_rel),
                joinedload(Order.OrderType),
                joinedload(Order.created_by),
                joinedload(Order.OrderStatus)
            )
        )

        #Aplica os filtros que o usuario colocou, caso colocou.
        if orderFilter.id is not None:
            query = query.filter(Order.OrderId==orderFilter.id)

        if orderFilter.location_id is not None:
            query = query.filter(Order.LocationId==orderFilter.location_id)
        
        if orderFilter.order_type_id is not None:
            query = query.filter(Order.OrderTypeId==orderFilter.order_type_id)
        
        if orderFilter.created_by_id is not None:
            query = query.filter(Order.UserId==orderFilter.created_by_id)
        
        if orderFilter.status_id is not None:
            query = query.filter(Order.OrderStatusId==orderFilter.status_id)

        if orderFilter.hotel_id is not None:
            query = query.filter(Order.HotelId==orderFilter.hotel_id)

        #Cria lista para serializar como JSON
        serialized_result = list()

        for order, local, nome, status, order_type in query:

            serialized_order = {
                'IdOrder': order.OrderId,
                'Description': order.Description,
                'Status': status,
                'CreatedBy': nome,
                'Location': local,
                'Type': order_type
            }

            serialized_result.append(serialized_order)

        return serialized_result
    
    def set_status(self, order_id: int, status_id: int):
        try:
 
            order_to_update = self.db_session.query(Order).filter(Order.OrderId == order_id).first()

            if order_to_update is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Order with ID {order_id} not found.',
                )


            order_to_update.OrderStatusId = status_id
            self.db_session.commit()

        except Exception as error:

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'Error updating order status: {error}',
            )
        
    def insert_order_type(self, order_type: OrderTypeSchema):
        order_type_to_insert = OrderType(
            OrderTypeName=order_type.order_type_name
        )
        try:
            self.db_session.add(order_type_to_insert)
            self.db_session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Erro de Integridade do Banco. Verifique os dados que esta tentando inserir.',
            )
        
    def delete_order_type(self, order_type_id: int):
        order_type_to_delete = self.db_session.query(OrderType).filter(OrderType.OrderTypeId == order_type_id).first()
        
        if order_type_to_delete:
            self.db_session.delete(order_type_to_delete)
            self.db_session.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'OrderType with ID {order_type_id} not found.',
            )