# Savoria — Backend

API REST del sistema Savoria, plataforma de gestión administrativa para restaurantes. Gestiona la lógica de negocio completa: facturación con patrón maestro-detalle, control de inventario, reportes y autenticación segura.

**Stack:** Python · FastAPI · PostgreSQL (NeonDB) · SQLAlchemy · Pydantic · bcrypt

---

## ¿Qué hace este backend?

Expone una API REST que centraliza toda la lógica del negocio:

- Autenticación de usuarios con contraseñas cifradas con **bcrypt**
- CRUD completo para clientes, artículos y facturas
- Cálculo automático de **IVA (19%)** por línea de detalle y total
- Generación correlativa de números de factura (FAC-0001, FAC-0002...)
- Descuento automático de stock al emitir una factura
- Módulo de reportes: resumen general, top 5 artículos y ventas por categoría

---

## Módulos

| Módulo | Endpoints |
|---|---|
| `auth` | Registro e inicio de sesión |
| `clientes` | CRUD de clientes del restaurante |
| `articulos` | CRUD del catálogo del menú con subida de imágenes |
| `facturas` | Emisión, consulta, actualización de estado y eliminación |
| `reportes` | Resumen general, top artículos y ventas por categoría |

Cada módulo tiene `models.py` (SQLAlchemy), `schemas.py` (Pydantic) y `router.py` (endpoints).

---

## Stack técnico

- **Python 3.11+**
- **FastAPI 0.136.1** — framework principal de la API REST
- **PostgreSQL (Neon)** — base de datos relacional en la nube
- **SQLAlchemy 2.0** — ORM para manejo de base de datos
- **Pydantic 2.13** — validación de datos de entrada y salida
- **bcrypt 5.0** — cifrado seguro de contraseñas
- **Uvicorn 0.47** — servidor ASGI

---

## Cómo correr el proyecto

### 1. Clonar el repositorio
```bash
git clone https://github.com/lauu2801r-dotcom/savoria_backend.git
cd savoria_backend
```

### 2. Crear entorno virtual
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
Crea un archivo `.env` en la raíz:

DATABASE_URL=postgresql://usuario:contraseña@host/savoria?sslmode=require

SECRET_KEY=tu_clave_secreta

ALGORITHM=HS256

### 4. Correr el servidor
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Documentación automática en `http://localhost:8000/docs`

---

## Estructura del proyecto
savoria_backend/

└── app/

├── core/

│   ├── config.py      # variables de entorno

│   └── database.py    # conexión PostgreSQL

└── modules/

├── auth/          # models, schemas, router

├── clientes/

├── articulos/

├── facturas/

└── reportes/

---

## Contexto académico

Proyecto de la asignatura **Computación Móvil**  
Universidad Manuela Beltrán · Bogotá, Colombia · 2026  
Autora: Laura Valentina González Rojas  
Docente: Robert Osorio Torres
