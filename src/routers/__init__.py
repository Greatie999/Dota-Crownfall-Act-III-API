from src.routers.accounts import router as accounts_router
from src.routers.clients import router as clients_router
from src.routers.launcher import router as launcher_router
from src.routers.reports import router as reports_router
# from src.routers.server import router as server_router
from src.routers.status import router as status_router
from src.routers.users import router as users_router
from src.routers.vpn import router as vpn_router

routers = [
    accounts_router,
    status_router,
    users_router,
    clients_router,
    launcher_router,
    # server_router,
    vpn_router,
    reports_router
]

__all__ = [
    "accounts_router",
    "clients_router",
    "launcher_router",
    "reports_router",
    # "server_router",
    "status_router",
    "users_router",
    "vpn_router",
    "routers"
]
