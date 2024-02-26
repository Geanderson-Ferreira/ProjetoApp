from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from src.db_manager.config import API_PREFIX
from sqlalchemy.orm import Session
from src.db_manager.depends import get_db_session
from src.db_manager.methods.user_methods import UserMethod
from src.schemas.user import UserSchema, UserSchemaForLogin
from fastapi.security import OAuth2PasswordRequestForm
from src.db_manager.depends import token_verifier

router  = APIRouter(prefix=API_PREFIX + '/user')


@router.post('/login')
def user_login(
    request_form_user: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_db_session)
    ):

    uMethod = UserMethod(db_session)
    
    USchema = UserSchemaForLogin(
        username=request_form_user.username,
        password=request_form_user.password
    )

    auth_data = uMethod.user_login(USchema, 1)

    return JSONResponse(
        content=auth_data,
        status_code=status.HTTP_200_OK
    )



@router.post('/register-user', dependencies=[Depends(token_verifier)])
def user_register(
    user: UserSchema,
    db_session: Session = Depends(get_db_session)
    ):

    u = UserMethod(db_session)
    u.register_user(user=user)
    
    return JSONResponse(
        content={'msg':'success'},
        status_code=status.HTTP_201_CREATED
    )

@router.post('/hotel-assignment', dependencies=[Depends(token_verifier)])
def hotel_assignment(
    user_id : int,
    hotel_id : int,
    db_session: Session = Depends(get_db_session)
    ):
    
    UserMethod(db_session).hotel_assignment(user_id, hotel_id)

@router.post('/remove-hotel-assignment', dependencies=[Depends(token_verifier)])
def hotel_assignment(
    user_id : int,
    hotel_id : int,
    db_session: Session = Depends(get_db_session)
    ):
    
    UserMethod(db_session).remove_hotel_assignment(user_id, hotel_id)
