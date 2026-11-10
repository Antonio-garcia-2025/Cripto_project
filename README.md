# Crypto ML Predictor - Bitcoin

Aplicación web en español que utiliza aprendizaje automático para analizar datos históricos de Bitcoin (BTC-USD) y mostrar una predicción orientativa sobre su posible movimiento para el día siguiente.

## Funcionalidades

- Consulta datos históricos de Bitcoin mediante Yahoo Finance.
- Calcula indicadores como medias móviles y volatilidad.
- Entrena un modelo de clasificación Random Forest.
- Muestra el precio más reciente, la predicción y la probabilidad estimada de subida.
- Presenta una sugerencia algorítmica: comprar, vender o mantener/esperar.
- Informa si no se pudieron obtener los datos o generar la predicción.

## Tecnologías

- Python
- Flask
- pandas y NumPy
- scikit-learn
- yfinance
- Gunicorn

## Requisitos

- Python 3.9 o superior
- pip

## Instalación y ejecución local

1. Clona el repositorio:

   ```bash
   git clone https://github.com/Antonio-garcia-2025/Cripto_project.git
   cd Cripto_project
   ```

2. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

3. Inicia la aplicación:

   ```bash
   python app.py
   ```

4. Abre en el navegador:

   ```text
   http://localhost:5000
   ```

La aplicación está disponible en las rutas `/` y `/predecir`.

Te comparto el link en render para que veas el trabajo https://cripto-project.onrender.com



Este proyecto tiene fines educativos. Las predicciones y sugerencias generadas por el modelo no constituyen asesoría financiera ni recomendaciones reales de inversión. El mercado de criptomonedas es volátil; toma tus decisiones con precaución.
