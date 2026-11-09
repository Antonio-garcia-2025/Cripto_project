# Cripto_project

Para desplegar en Render como servicio web, configura:

- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`

La ruta `/` sirve la página principal. Si Yahoo Finance no está disponible, la página muestra un mensaje en lugar de dejar la portada en blanco.