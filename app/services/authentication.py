import bcrypt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from app.core.config import SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
import app.schemas as schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthException(BaseException):
    pass


class AuthService:
    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        print(password)
        return pwd_context.hash(password)

    """
    ユーザのアクセストークンを生成
    """

    def create_access_token_for_user(
        self, data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES
    ):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)

        to_encode.update({"exp": expire})
        access_token = jwt.encode(to_encode, str(SECRET_KEY), algorithm=JWT_ALGORITHM)

        return access_token

    """
    access_tokenからusernameを取得
    """

    def get_current_username(
        self,
        token: str = Depends(oauth2_scheme),
    ):
        try:
            # 受け取ったアクセストークンをdecodeする。payloadを分解して、usernameを取得
            payload = jwt.decode(token, str(SECRET_KEY), algorithms=[JWT_ALGORITHM])
            username: str = payload.get("sub")
            # tokenのschemaの一致を確認
            token_data = schemas.TokenData(username=username)
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token_data.username
