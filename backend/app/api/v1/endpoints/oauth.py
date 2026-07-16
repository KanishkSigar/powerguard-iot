from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def get_oauth():
    return {'message': 'oauth endpoint'}

