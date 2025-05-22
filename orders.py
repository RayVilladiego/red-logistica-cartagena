from fastapi import APIRouter

router = APIRouter()

@router.get("/orders")
def get_orders():
    # Aquí iría la lógica para listar órdenes
    return [{"id": 1, "description": "Orden 1"}, {"id": 2, "description": "Orden 2"}]
