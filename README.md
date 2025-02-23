# DB Prueba Técnica

Este proyecto tiene como objetivo procesar y transferir datos de compras de dos compañías ficticias. A lo largo del documento se detallan los procedimientos de instalación, ejecución y pruebas necesarias.

## Requisitos

Asegúrate de tener instalados los siguientes componentes:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Instalación y Ejecución
Sigue estos pasos para ejecutar la aplicación dentro de un contenedor Docker.

### 1. Clonar el Repositorio

```sh
git clone https://github.com/mtumalan/NT-database.git
cd NT-database
```

### 2. Construir y Ejecutar el Contenedor

```sh
docker-compose up --build
```

Esto iniciará un contenedor con PostgreSQL y un servicio de procesamiento de datos.

### 3. Verificar los contenedores en ejecución
```sh
docker ps
```

Deberías ver los servicios postgres_db y data_processor corriendo.

# Sección 1: Procesamiento y Transferencia de Datos

## 1.1 Carga de información
Los datos proporcionados en el dataset se almacenan en PostgreSQL, utilizando el esquema definido en init.sql.

Se utilizó PostgreSQL porque es la base de datos con la que he estado trabajando últimamente y considero que ofrece varias ventajas en la integración con Python, especialmente con SQLAlchemy y Pandas, lo que facilita la manipulación de datos y su almacenamiento eficiente.

## 1.2 Extracción de Datos
El archivo load_data.py es el encargado de extraer la data para la base de datos, limpiarla, extraerla en .csv y crear la vista daily_transactions.

Formato de Exportación

Se eligió CSV porque:

    - Es ligero y ampliamente compatible con bases de datos y hojas de cálculo.
    - Facilita el análisis y transformación de datos en herramientas externas.

## 1.3 Transformación de datos
Para cumplir con el esquema definido en init.sql, se realizan las siguientes transformaciones en data_processor:

### Limpieza de datos:

    - Se eliminaron valores no válidos en company_id (por ejemplo, "*******").
    - Se reemplazaron valores NaN en company_id con "unknown_company".
    - Se asignó 0 a amount cuando estaba vacío.
    - Se eliminaron registros con fechas inválidas en created_at.

### Conversión de tipos:

    - Se convirtió amount a tipo numérico (float) para evitar errores en cálculos.
    - Se convirtieron created_at y updated_at a tipo datetime para manejar fechas correctamente.

### Filtrado de valores extremos:

    - Se eliminaron valores amount fuera del rango de [1, 10,000,000] para evitar errores en el análisis.