from fastapi import APIRouter


router = APIRouter(prefix='/kb', tags=['kb'])

@router.get(
    response_model=
)