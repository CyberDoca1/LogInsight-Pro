"""
Configuración de la base de datos para LogInsight Pro
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from loguru import logger

from .config import settings

# Crear la URL de conexión a la base de datos
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

# Crear el motor de base de datos
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_recycle=3600,
    echo=settings.DB_ECHO
)

# Crear el generador de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear la base para los modelos declarativos
Base = declarative_base()

def get_db():
    """
    Dependencia para obtener una sesión de base de datos
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_db_connection():
    """
    Gestor de contexto para obtener una conexión directa
    Útil para operaciones masivas y procesamiento por lotes
    """
    try:
        connection = engine.connect()
        yield connection
    except Exception as e:
        logger.error(f"Error al conectar a la base de datos: {e}")
        raise
    finally:
        connection.close()