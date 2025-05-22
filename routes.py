from flask import Flask, request, jsonify
import pandas as pd
from tracking import predecir_tiempo  # importa la función

app = Flask(__name__)

@app.route('/predecir_entrega', methods=['POST'])
def predecir_entrega():
    data = request.get_json()
    df = pd.DataFrame([data])
    pred = predecir_tiempo(df)
    return jsonify({'tiempo_estimado': float(pred[0])})

# Agrega si necesitas ejecutar el servidor local
if __name__ == '__main__':
    app.run(debug=True)
