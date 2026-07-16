from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def get_tariffs():
    return {'message': 'tariffs endpoint'}

