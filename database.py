import pandas as pd

def get_route_data():
    return pd.DataFrame({
        'Origen': ['Bocagrande', 'Manga', 'Centro'],
        'Destino': ['Crespo', 'El Bosque', 'Pie de la Popa'],
        'Distancia_km': [6.2, 5.4, 4.1],
        'Congestion': ['Media', 'Alta', 'Baja']
    })


def get_kpi_data():
    return {
        'entregados': 124,
        'en_ruta': 27,
        'pendientes': 9
    }


def get_order_data():
    return pd.DataFrame({
        'ID': [1, 2, 3],
        'Cliente': ['Luis', 'Ana', 'Pedro'],
        'Estado': ['Entregado', 'En ruta', 'Pendiente'],
        'Dirección': ['Calle 1', 'Carrera 10', 'Transversal 5']
    })
