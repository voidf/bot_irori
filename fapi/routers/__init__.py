from fastapi import APIRouter, Depends
master_router = APIRouter(
    # prefix="/api/v2",
    tags=["master"],
    dependencies=[]
)


from fapi.routers.auth import auth_route
from fapi.routers.worker import worker_route
# from .team import team_route
# from .sign import sign_route
# from .report import report_route
# from .initialize import initialize_route



master_router.include_router(auth_route)
master_router.include_router(worker_route)
# master_router.include_router(team_route)
# master_router.include_router(sign_route)
# master_router.include_router(report_route)
# master_router.include_router(initialize_route)
