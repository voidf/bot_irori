from fastapi import APIRouter, Depends
from utils import general_before_request
master_router = APIRouter(
    # prefix="/api/v2",
    tags=["master"],
    dependencies=[Depends(general_before_request)]
)


from .auth import auth_route
from .team import team_route
from .sign import sign_route
from .report import report_route
from .initialize import initialize_route



master_router.include_router(auth_route)
master_router.include_router(team_route)
master_router.include_router(sign_route)
master_router.include_router(report_route)
master_router.include_router(initialize_route)
