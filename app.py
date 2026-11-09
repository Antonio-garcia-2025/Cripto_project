import os
import numpy as np
import pandas as pd
import yfinance as yf
from flask import Flask, render_template
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

@app.route('/')
@app.route('/predecir')
def predecir():
    try:
        df = yf.download("BTC-USD", period="2y", interval="1d", progress=False)
        if df.empty:
            return render_template(
                "index.html",
                error="Yahoo Finance no devolvió datos. Inténtalo de nuevo más tarde.",
            ), 503

        if isinstance(df.columns, pd.MultiIndex):
            for level in range(df.columns.nlevels):
                columns = df.columns.get_level_values(level)
                if {"Close", "Volume"}.issubset(columns):
                    df.columns = columns
                    break

        if not {"Close", "Volume"}.issubset(df.columns):
            raise ValueError("La descarga no contiene las columnas Close y Volume.")

        df["Media_Movil_7d"] = df["Close"].rolling(window=7).mean()
        df["Media_Movil_25d"] = df["Close"].rolling(window=25).mean()
        df["Retorno"] = df["Close"].pct_change()
        df["Volatilidad"] = df["Retorno"].rolling(window=7).std()
        df["Target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)
        df.dropna(inplace=True)

        X = df[["Media_Movil_7d", "Media_Movil_25d", "Volatilidad", "Volume"]]
        y = df["Target"]
        modelo = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=4)
        modelo.fit(X, y)

        ultima_fila = X.tail(1)
        prediccion_manana = int(modelo.predict(ultima_fila)[0])
        prob_subir = float(modelo.predict_proba(ultima_fila)[:, 1][0])

        precio_actual = float(df["Close"].iloc[-1])
        fecha_actual = df.index[-1].strftime('%Y-%m-%d')
        direccion = "SUBE" if prediccion_manana == 1 else "BAJA"

        if prediccion_manana == 1 and prob_subir >= 0.55:
            recomendacion = "COMPRAR"
            motivo = f"El modelo detecta una tendencia alcista sólida con un {prob_subir*100:.2f}% de probabilidad de incremento para mañana."
        elif prediccion_manana == 0 and prob_subir <= 0.45:
            recomendacion = "VENDER"
            motivo = f"El modelo proyecta una alta probabilidad de corrección o baja ({100 - prob_subir*100:.2f}% de probabilidad de caída)."
        else:
            recomendacion = "MANTENER / ESPERAR"
            motivo = f"El mercado muestra indecisión. La probabilidad de subida está muy cerca del 50% ({prob_subir*100:.2f}%). Es mejor no arriesgar."

        contexto_datos = {
            "cripto": "BTC-USD",
            "fecha": fecha_actual,
            "precio": f"{precio_actual:,.2f}",
            "prediccion": direccion,
            "prob_subir": f"{prob_subir * 100:.2f}",
            "recomendacion": recomendacion,
            "motivo": motivo,
            "nota": "Modelo educativo basado en Machine Learning (Random Forest). No constituye asesoría financiera real."
        }

        return render_template("index.html", data=contexto_datos)

    except Exception:
        app.logger.exception("No se pudo generar la predicción de Bitcoin")
        return render_template(
            "index.html",
            error="No se pudo generar la predicción. Inténtalo de nuevo más tarde.",
        ), 503

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
