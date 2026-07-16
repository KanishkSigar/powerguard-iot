from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def get_webhooks():
    return {'message': 'webhooks endpoint'}

