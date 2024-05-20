# Servicio de correo electrónico

## Instalar dependencias del archivo requirements.txt

pip install -r requirements.txt

## Levantar proyecto

uvicorn main:app --host 0.0.0.0 --port 8000 --reload

## Capturar migraciones

alembic revision --autogenerate -m "message"

## Aplicar migraciones

alembic upgrade head
