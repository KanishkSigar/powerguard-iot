from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def get_firmware():
    return {'message': 'firmware endpoint'}

