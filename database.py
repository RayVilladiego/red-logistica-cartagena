import pandas as pd

def get_orders():
    return pd.DataFrame([
        {"ID": 101, "Cliente": "Juan Pérez", "Estado": "En Ruta", "Tiempo Estimado (min)": 43},
        {"ID": 102, "Cliente": "Camila Ríos", "Estado": "Entregado", "Tiempo Estimado (min)": 35}
    ])

def get_route_data():
    return pd.DataFrame([
        {"Ruta": "Cartagena → Bocagrande", "Congestión": "Alta"},
        {"Ruta": "Cartagena → Zona Norte", "Congestión": "Media"}
    ])
