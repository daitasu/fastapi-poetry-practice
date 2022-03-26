from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app import schemas
from app.services.authentication import auth_service
import app.util_user as util_user

router = APIRouter()

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$ksGbpKo4SEVeYQImKWUYKubqqL/9B28E.ldD/u8Ed770w2rEquXy2",
        "disabled": False,
    }
}


# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return schemas.AuthUserInDB(**user_dict)


# def authenticate_user(fake_db, username: str, password: str):
#     user = get_user(fake_db, username)
#     if not user:
#         return False
#     if not auth_service.verify_password(password, user.hashed_password):
#         return False
#     return user


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     username = auth_service.get_current_username(token)
#     # dbからuserを取得
#     user = get_user(fake_users_db, username=username)
#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user


# async def get_current_active_user(
#     current_user: schemas.AuthUser = Depends(get_current_user),
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # user検索とパスワードの突合
    user = util_user.authenticate_user(
        fake_users_db, form_data.username, form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # 有効期限付きで、subにusernameを入れたアクセストークンを返す
    access_token = auth_service.create_access_token_for_user(
        data={"sub": user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(
    current_user: schemas.AuthUser = Depends(util_user.get_current_active_user),
):
    return current_user


@router.post("/pass/", response_model=str)
def get_pass(password: str):
    passes = auth_service.get_password_hash(password)
    return passes


@router.get("/users/me/items/")
async def read_own_items(
    current_user: schemas.AuthUser = Depends(util_user.get_current_active_user),
):
    return [{"item_id": "Foo", "owner": current_user.username}]
