'''
Este script en Python se encarga de cargar, limpiar y almacenar datos en una base de datos PostgreSQL, 
asegurando que solo se almacenen registros válidos y consistentes. 

De igual forma, se crea una extracción de los datos en un archivo CSV (charges_data.csv) para su posterior análisis.

Además, crea una vista (daily_transactions) que permite consultar transacciones agregadas por fecha y empresa.
'''

import pandas as pd
from sqlalchemy import create_engine, text
import numpy as np
import os

# Conexión a la base de datos PostgreSQL con sqlalchemy
DATABASE_URL = "postgresql://user:password@db:5432/nt_group"
engine = create_engine(DATABASE_URL)

# Se carga el archivo CSV con los datos de prueba
df = pd.read_csv("data_prueba_tecnica.csv")

# Se renombran las columnas para asegurar consistencia en la base de datos:
df.columns = ['id', 'company_name', 'company_id', 'amount', 'status', 'created_at', 'updated_at']

# Se limpian los datos para asegurar que sean válidos y consistentes:
df['company_id'] = df['company_id'].replace("*******", np.nan) # Limpiar company_id con valores no válidos
df = df.assign(company_id=df['company_id'].fillna("unknown_company"))  # Si company_id es nulo, se asigna 'unknown_company'
df = df.assign(amount=df['amount'].fillna(0))  # Si amount es nulo, se asigna 0
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')  # Convertir 'amount' a numérico (si es posible)
df = df[df['amount'].between(1, 1e7)]  # Eliminar 'amount' fuera del rango [1, 10,000,000]
df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce') # Convertir 'created_at' a fecha
df = df.dropna(subset=['created_at'])  # Eliminar registros con 'created_at' nulo
df['updated_at'] = pd.to_datetime(df['updated_at'], errors='coerce') # Convertir 'updated_at' a fecha

# Se almacenan los datos limpios en la base de datos PostgreSQL
df.to_sql('charges', engine, if_exists='append', index=False)
print("¡Datos cargados en la base de datos PostgreSQL!")

# Consulta SQL para extraer los datos
df = pd.read_sql("SELECT * FROM charges", engine)

output_dir = "./extracted_data"
os.makedirs(output_dir, exist_ok=True)

# Cargar los datos en un DataFrame de Pandas
csv_path = os.path.join(output_dir, "charges_data.csv")
df.to_csv(csv_path, index=False)

print("¡Datos guardados en charges_data.csv!")

# Se crea una vista (daily_transactions) que permite consultar transacciones agregadas por fecha y empresa
'''
Esta vista:
- Agrupa las transacciones por fecha y empresa
- Suma los montos de las transacciones
- Excluye las transacciones de empresas desconocidas
- Ordena los resultados por fecha
'''
with engine.connect() as conn:
    conn.execute(text("""
        DROP VIEW IF EXISTS daily_transactions;
        CREATE VIEW daily_transactions AS
        SELECT 
            DATE(created_at) AS transaction_date, 
            company_id, 
            SUM(amount) AS total_amount
        FROM charges
        WHERE company_id != 'unknown_company'  -- Exclude unknown companies
        GROUP BY DATE(created_at), company_id
        ORDER BY transaction_date;
    """))
    conn.commit()

print("¡Vista 'daily_transactions' creada en la base de datos PostgreSQL!")