from datetime import timedelta

import fastapi

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.se curity import OAuth2PasswordRequestForm

from .auth import (
    fake_users_db,
    create_access_token,
    User,
    get_current_user,
    authenticate_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from .middlware import LoggingMiddleware

app = fastapi.FastAPI()
app.add_middleware(LoggingMiddleware)


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
