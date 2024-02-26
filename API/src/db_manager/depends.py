from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from src.db_manager.config import SESSION
from src.db_manager.methods.user_methods import UserMethod
from sqlalchemy.orm import Session

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/api/user/login')

def get_db_session():
    try:
        session = SESSION()
        yield session
    finally:
        session.close()

def token_verifier(db_session: Session = Depends(get_db_session),
                   token = Depends(oauth_scheme)
                   ):
    
    UserMethod(db_session).verify_token(token)
    
