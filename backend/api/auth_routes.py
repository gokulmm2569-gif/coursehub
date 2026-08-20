import os
import django
from fastapi import APIRouter, Depends, HTTPException, status

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import User
from .auth_schemas import LoginRequest, MessageResponse, RefreshRequest, RefreshResponse, RegisterRequest, TokenResponse, UserResponse
from .auth_security import current_user, decode_token, issue_tokens

router = APIRouter(prefix='/api/v1/auth', tags=['auth'])


def serialize_user(user: User) -> UserResponse:
    return UserResponse(id=user.pk, email=user.email, first_name=user.first_name, last_name=user.last_name, role=user.role)


@router.post('/register', response_model=TokenResponse, status_code=201)
def register(payload: RegisterRequest):
    if User.objects.filter(email__iexact=payload.email).exists():
        raise HTTPException(status_code=409, detail='An account with this email already exists')
    user = User.objects.create_user(email=payload.email, password=payload.password, first_name=payload.first_name, last_name=payload.last_name)
    access, refresh = issue_tokens(user)
    return TokenResponse(access_token=access, refresh_token=refresh, user=serialize_user(user))


@router.post('/login', response_model=TokenResponse)
def login(payload: LoginRequest):
    try:
        user = User.objects.get(email__iexact=payload.email)
    except User.DoesNotExist as exc:
        raise HTTPException(status_code=401, detail='Invalid email or password') from exc
    if not user.is_active or not user.check_password(payload.password):
        raise HTTPException(status_code=401, detail='Invalid email or password')
    access, refresh = issue_tokens(user)
    return TokenResponse(access_token=access, refresh_token=refresh, user=serialize_user(user))


@router.post('/refresh', response_model=RefreshResponse)
def refresh(payload: RefreshRequest):
    claims = decode_token(payload.refresh_token, 'refresh')
    try:
        user = User.objects.get(pk=int(claims['sub']), is_active=True)
    except (User.DoesNotExist, ValueError) as exc:
        raise HTTPException(status_code=401, detail='User not found or inactive') from exc
    access, next_refresh = issue_tokens(user)
    return RefreshResponse(access_token=access, refresh_token=next_refresh)


@router.post('/logout', response_model=MessageResponse)
def logout(user=Depends(current_user)):
    return MessageResponse(message='Signed out successfully')


@router.get('/me', response_model=UserResponse)
def me(user=Depends(current_user)):
    return serialize_user(user)
