FROM python:3.9

RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY load_data.py .
COPY data_prueba_tecnica.csv .

CMD ["sh", "-c", "until pg_isready -h db -p 5432; do sleep 1; done; python load_data.py"]