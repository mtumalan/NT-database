--Este conjunto de instrucciones SQL crea la base de datos nt_group y define dos tablas principales: companies y charges.


-- Asegurar que la base de datos exista
CREATE DATABASE nt_group;
\c nt_group;

-- Crear la tabla de empresas
CREATE TABLE IF NOT EXISTS companies (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(130) NOT NULL
);

-- La tabla charges almacena información sobre los cargos o transacciones asociadas a cada empresa.
CREATE TABLE IF NOT EXISTS charges (
    id SERIAL PRIMARY KEY,
    company_id INT NOT NULL,
    amount DECIMAL(16,2) NOT NULL,
    status VARCHAR(30) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NULL,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);