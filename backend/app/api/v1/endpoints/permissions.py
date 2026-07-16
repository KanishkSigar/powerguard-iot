from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def get_permissions():
    return {'message': 'permissions endpoint'}

