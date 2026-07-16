from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def get_rules():
    return {'message': 'rules endpoint'}

