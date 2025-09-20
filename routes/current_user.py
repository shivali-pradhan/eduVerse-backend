from fastapi import APIRouter, Depends

from schemas.token_schemas import CurrentUser
from auth.dependencies import get_current_user

router = APIRouter(
    prefix = "/me", 
    tags = ["user"]
)

@router.get("/me")
def get_user(current_user: CurrentUser = Depends(get_current_user)):
    return current_user