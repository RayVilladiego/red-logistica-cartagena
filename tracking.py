from fastapi import APIRouter

router = APIRouter()

@router.get("/tracking/{order_id}")
def get_tracking(order_id: int):
    # Simulación de estado de seguimiento
    return {"order_id": order_id, "status": "En ruta", "location": "Cartagena"}

