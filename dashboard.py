from tracking import predecir_tiempo

def mostrar_prediccion(datos):
    df = pd.DataFrame([datos])
    pred = predecir_tiempo(df)
    print(f"Tiempo estimado: {pred[0]:.2f} minutos")
    # Aquí agregar código para actualizar dashboard visualmente
