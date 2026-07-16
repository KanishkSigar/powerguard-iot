from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def get_integrations():
    return {'message': 'integrations endpoint'}

