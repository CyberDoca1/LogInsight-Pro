# LogInsight Pro

Sistema avanzado de análisis de logs y gestión de credenciales con agrupamiento inteligente de URLs y procesamiento acelerado por GPU.

## Características

- Procesamiento de logs acelerado por GPU para análisis de alto rendimiento
- Agrupamiento inteligente de URLs basado en similitud
- Almacenamiento óptimo de credenciales con detección de duplicados
- Interfaz avanzada con visualización de relaciones
- Escalabilidad para entornos de alta demanda

## Requisitos del sistema

- Python 3.10+
- PostgreSQL 14+
- CUDA 11.8+ (para aceleración GPU)
- Redis (para caché)

## Estructura del proyecto

```
LogInsight-Pro/
├── backend/         # API y lógica de backend (FastAPI)
├── frontend/        # Interfaz de usuario (PyQt6)
├── core/            # Módulos centrales y lógica de procesamiento
├── ml/              # Componentes de machine learning
├── gpu/             # Aceleración GPU y procesamiento paralelo
├── migrations/      # Migraciones de base de datos
└── scripts/         # Scripts de utilidad y herramientas
```

## Configuración inicial

1. Clona este repositorio
2. Crea un entorno virtual: `python -m venv venv`
3. Activa el entorno virtual:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Instala las dependencias: `pip install -r requirements.txt`
5. Configura la base de datos PostgreSQL
6. Ejecuta las migraciones: `python -m scripts.db_migrate`
7. Inicia el backend: `python -m backend.main`
8. Inicia la interfaz: `python -m frontend.main`

## Licencia

Copyright (c) 2025. Todos los derechos reservados.