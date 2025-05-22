from flask import Flask, request, jsonify
import pandas as pd
from tracking import predecir_tiempo

app = Flask(__name__)

@app.route('/predecir', methods=['POST'])
def predecir():
    data = request.get_json()
    df = pd.DataFrame([data])
    pred = predecir_tiempo(df)
    return jsonify({'tiempo_estimado': float(pred[0])})

if __name__ == '__main__':
    app.run(debug=True)
