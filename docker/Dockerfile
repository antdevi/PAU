FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt ./

RUN apt-get update && apt-get install -y \
    gcc libpq-dev python3-dev default-libmysqlclient-dev libgl1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --no-cache --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 5000

ENV OPENAI_API_KEY=${OPENAI_API_KEY}

CMD ["python", "app.py"]
