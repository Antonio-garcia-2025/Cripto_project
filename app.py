import os
import numpy as np
import pandas as pd
import yfinance as yf
from flask import Flask, jsonify
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "mensaje": "API de Predicción Real de BTC activa. Ve a /predecir"
    })

@app.route('/predecir')
def predecir():
    try:
        # 1. DESCARGA DE DATOS REALES DE BITCOIN (Últimos 2 años diariamente)
        # Trae las columnas: Open, High, Low, Close, Volume
        df = yf.download("BTC-USD", period="2y", interval="1d")
        
        if df.empty:
            return jsonify({"error": "No se pudieron obtener datos de Yahoo Finance"}), 500

        # Forzar que los nombres de las columnas sean simples (por si hay MultiIndex)
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

        # 2. INGENIERÍA DE CARACTERÍSTICAS (Features con datos reales)
        df["Media_Movil_7d"] = df["Close"].rolling(window=7).mean()
        df["Media_Movil_25d"] = df["Close"].rolling(window=25).mean()
        
        df["Retorno"] = df["Close"].pct_change()
        df["Volatilidad"] = df["Retorno"].rolling(window=7).std()
        
        # Objetivo: 1 si mañana el cierre es mayor que el de hoy, 0 si baja
        df["Target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)
        df.dropna(inplace=True)

        # 3. SEPARACIÓN Y ENTRENAMIENTO
        X = df[["Media_Movil_7d", "Media_Movil_25d", "Volatilidad", "Volume"]]
        y = df["Target"]
        
        # Entrenamos el Random Forest
        modelo = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=4)
        modelo.fit(X, y)

        # 4. PREDICCIÓN PARA MAÑANA (Usando los datos reales de HOY)
        ultima_fila = X.tail(1)
        prediccion_manana = int(modelo.predict(ultima_fila)[0])
        probabilidades = modelo.predict_proba(ultima_fila)[0]
        prob_subir = float(probabilidades[1])

        precio_actual = float(df["Close"].iloc[-1])
        fecha_actual = df.index[-1].strftime('%Y-%m-%d')

        resultado = "SUBE (1)" if prediccion_manana == 1 else "BAJA (0)"
        
        return jsonify({
            "criptomoneda": "BTC-USD",
            "fecha_ultimos_datos": fecha_actual,
            "ultimo_precio_cierre_real": round(precio_actual, 2),
            "prediccion_para_manana": resultado,
            "probabilidad_de_subida": f"{prob_subir * 100:.2f}%",
            "nota": "Modelo educativo basado en Random Forest y Yahoo Finance."
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
