# Ecocycle

Es un proyecto de DSSD 2024

## Setup con Docker

```bash
# Creamos el build de docker
docker compose build

# Levantamos los servicios
docker compose up
```
### Servicios
- La aplicacion de Django
- Un PGadmin por si no tienen un cliente DB
- Una base de datos PostgreSQL 16

### Notas
- Los cambios se reflejan automaticamente no hace falta apagar y volver a cargar.
- Si no quieren usar docker pueden levantar el sistema en su local en un venv.

## Setup local
```bash
pip install -r ./requirements.txt

python manage.py migrate
```

## Componentes principales


1. Dango
2. Swagger UI
3. Docker
4. PostgreSQL

## Contribuidores

- Ignacio Cafiero Torrubia
- Ariana Marchi
- Jose Ignacio Borrajo
