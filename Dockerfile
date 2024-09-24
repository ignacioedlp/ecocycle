FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk update \ 
    && apk add --no-cache gcc musl-dev libffi-dev postgresql-dev python3-dev \
    && pip install --upgrade pip

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./

CMD ["sh", "entrypoint.sh"]
