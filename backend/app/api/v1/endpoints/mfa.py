from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def get_mfa():
    return {'message': 'mfa endpoint'}

