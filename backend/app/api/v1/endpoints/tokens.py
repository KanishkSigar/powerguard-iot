from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def get_tokens():
    return {'message': 'tokens endpoint'}

