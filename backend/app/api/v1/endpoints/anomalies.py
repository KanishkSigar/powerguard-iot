from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def get_anomalies():
    return {'message': 'anomalies endpoint'}

