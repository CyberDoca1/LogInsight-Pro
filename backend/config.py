"""
Configuración general para LogInsight Pro
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path


class Settings(BaseSettings):
    """
    Configuración global del sistema usando Pydantic
    Los valores se cargan desde variables de entorno o un archivo .env
    """
    # Configuración general
    APP_NAME: str = "LogInsight Pro"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # Configuración de la base de datos
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "cerebro collar"  # Cambia esto en producción
    DB_NAME: str = "log_insight_pro"
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_ECHO: bool = False
    
    # Configuración de Redis para caché
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    
    # Configuración de GPU
    USE_GPU: bool = True
    GPU_MEMORY_LIMIT: Optional[int] = None  # En MB, None para usar toda la memoria disponible
    
    # Configuración de seguridad
    SECRET_KEY: str = "cambiar_esto_en_produccion_con_una_clave_segura"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Rutas de archivos
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    LOG_DIR: Path = BASE_DIR / "logs"
    DATA_DIR: Path = BASE_DIR / "data"
    TEMP_DIR: Path = DATA_DIR / "temp"
    RESULTS_DIR: Path = BASE_DIR / "results"
    
    # Configuración de procesamiento
    BATCH_SIZE: int = 1000
    MAX_PROCESSES: int = 8  # Para procesamiento paralelo en CPU
    SIMILARITY_THRESHOLD: float = 0.8  # Para agrupamiento de URLs
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Crear las carpetas necesarias
def create_required_directories(settings: Settings):
    """
    Crea los directorios requeridos por la aplicación si no existen
    """
    for directory in [settings.LOG_DIR, settings.DATA_DIR, settings.TEMP_DIR, settings.RESULTS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)


# Instancia global de configuración
settings = Settings()

# Crear directorios
create_required_directories(settings)