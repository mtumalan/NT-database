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

Se eligió PostgreSQL porque:

    - Permite consultas eficientes y almacenamiento estructurado.
    - Soporta transacciones ACID para garantizar la integridad de los datos.
    - Es compatible con herramientas analíticas avanzadas.

## 1.2 Extracción de Datos
El archivo load_data.py es el encargado de extraer la data para la base de datos, limpiarla, extraerla en .csv y crear la vista daily_transactions.

Formato de Exportación

Se eligió CSV porque:

    - Es ligero y ampliamente compatible con bases de datos y hojas de cálculo.
    - Facilita el análisis y transformación de datos en herramientas externas.

## 1.3 Transformación de datos
Para cumplir con el esquema definido en init.sql, se realizan las siguientes transformaciones en data_processor:

    - Corrección de Tipos: Conversión de valores amount a DECIMAL y created_at a TIMESTAMP.
    - Limpieza de Datos: Eliminación de registros con valores nulos o inválidos.
    - Estandarización: Normalización de cadenas y eliminación de duplicados.