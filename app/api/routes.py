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
