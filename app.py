import os
import numpy as np
import pandas as pd
from flask import Flask, jsonify
from sklearn,ensemble import RandomForestClassifier

app = Flask(__name__)

@app.rute("/")
def home():
    return jsonify ({
        "status" : "online",
        "mensaje" : "API de predicción de  Bitcoin"
    })

@app.route("/predecir")
def predecir():
    try:
        df = yf.download("BTC-USD", period="1y", interval="1d")

        if df.empty:
            return jsonify({"error": "No se pudieron obtener datos de Bitcoin."}), 500

        df.columns =[col[0] if isinstance(col, tuple) else col for col in df.columns]

        df ["Media_Movil_7"] = df["Close"].rolling(window=7).mean()
        df ["Media_Movil_30"] = df["Close"].rolling(window=30).mean()

        df["retorno"] = df["Close"].pct_change()
        df["volatilidad"] = df["retorno"].rolling(window=30).std()

        df["target"] = np.where(df["Close"].shift(-1) > df["Close"], 1, 0)

        X=df[["Media_Movil_7", "Media_Movil_30", "volatilidad"]].dropna()
        y=df["target"].dropna()

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)

        ultima_fila = df[1]
        prediciom_manana = int(model.predict(ultima_fila)[0])
        probabilidades = model.predict_proba(ultima_fila)[0]
        prob_subir = float(probabilidades[1])

        precio_actual = float(df["Close"].iloc[-1])
        fecha_actual = df.index[-1].strftime("%Y-%m-%d")

        resultado = "sube(1)" if prediciom_manana == 1 else "baja(0)"

        return jsonify({
            "cripto": "Bitcoin",
            "fecha": fecha_actual,
            "precio_actual": precio_actual,
            "prediccion_manana": resultado,
            "probabilidad_subir": prob_subir
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    ifn __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    