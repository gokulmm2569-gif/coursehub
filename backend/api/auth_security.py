import os
import uuid
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

JWT_ALGORITHM = 'HS256'
JWT_SECRET = os.getenv('JWT_SECRET_KEY', 'development-jwt-secret-change-me')
ACCESS_MINUTES = int(os.getenv('ACCESS_TOKEN_MINUTES', '30'))
REFRESH_DAYS = int(os.getenv('REFRESH_TOKEN_DAYS', '14'))
bearer = HTTPBearer(auto_error=False)


def create_token(user_id: int, role: str, token_type: str, lifetime: timedelta) -> str:
    now = datetime.now(timezone.utc)
    payload = {'sub': str(user_id), 'role': role, 'type': token_type, 'jti': str(uuid.uuid4()), 'iat': now, 'exp': now + lifetime}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def issue_tokens(user) -> tuple[str, str]:
    return (
        create_token(user.pk, user.role, 'access', timedelta(minutes=ACCESS_MINUTES)),
        create_token(user.pk, user.role, 'refresh', timedelta(days=REFRESH_DAYS)),
    )


def decode_token(token: str, expected_type: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid or expired token') from exc
    if payload.get('type') != expected_type or not payload.get('sub'):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token type')
    return payload


def current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)):
    if not credentials:
        raise HTTPException(status_code=401, detail='Authorization required')
    payload = decode_token(credentials.credentials, 'access')
    from core.models import User
    try:
        return User.objects.get(pk=int(payload['sub']), is_active=True)
    except (User.DoesNotExist, ValueError) as exc:
        raise HTTPException(status_code=401, detail='User not found or inactive') from exc


def require_admin(user=Depends(current_user)):
    if user.role != 'admin':
        raise HTTPException(status_code=403, detail='Admin role required')
    return user
