from fastapi_users import FastAPIUsers
from apps.auth.database import User
from apps.auth.auth import auth_backend
from apps.auth.manager import get_user_manager

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_superuser = fastapi_users.current_user(active=True, superuser=True)
