import uuid
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, CookieTransport, JWTStrategy

from app.core.config import settings
from app.core.user_manager import get_user_manager
from app.db.models.user import MUser


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.auth_secret,
        lifetime_seconds=settings.access_token_lifetime_seconds,
    )


cookie_transport = CookieTransport(
    cookie_name=settings.cookie_name,
    cookie_max_age=settings.cookie_max_age_seconds,
    cookie_httponly=True,
    cookie_secure=settings.cookie_secure,
    cookie_samesite="lax",
)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[MUser, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)
