FROM python:3.11-alpine

WORKDIR /app

RUN apk update \ 
    && apk add --no-cache gcc musl-dev libffi-dev postgresql-dev python3-dev \
    && pip install --upgrade pip

# Copiar los archivos de requerimientos
COPY requirements.txt /app/

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la app
COPY . /app/

# Exponer el puerto en el que Django ejecutará el servidor
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
