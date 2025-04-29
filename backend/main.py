"""
Punto de entrada principal para la API FastAPI de LogInsight Pro
"""

import uvicorn
from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from loguru import logger
import os

from .database import engine, get_db
from . import models, schemas, crud
from .config import settings

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Configurar la aplicación FastAPI
app = FastAPI(
    title="LogInsight Pro API",
    description="API para el sistema de análisis de logs y gestión de credenciales",
    version="0.1.0"
)

# Configurar CORS para permitir solicitudes desde la interfaz
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, limitar a orígenes específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar el logger
logger.add(
    "logs/api.log",
    rotation="10 MB",
    retention="1 week",
    level="INFO",
    format="{time} | {level} | {message}"
)

# Rutas para URLs
@app.get("/search/", response_model=schemas.SearchResult)
def search(
    q: str = Query(..., min_length=3),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Busca en las URLs y datos según el término de búsqueda
    """
    result = crud.search_items(db, q=q, skip=skip, limit=limit)
    return result

@app.get("/url/{url_id}", response_model=schemas.URLDetailed)
def get_url(url_id: int, db: Session = Depends(get_db)):
    """
    Obtiene los detalles de una URL específica
    """
    url = crud.get_url(db, url_id=url_id)
    if url is None:
        raise HTTPException(status_code=404, detail="URL no encontrada")
    return url

@app.get("/url_groups/", response_model=list[schemas.URLGroup])
def get_url_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtiene los grupos de URLs similares
    """
    groups = crud.get_url_groups(db, skip=skip, limit=limit)
    return groups

@app.get("/url_group/{group_id}", response_model=schemas.URLGroupDetailed)
def get_url_group(group_id: int, db: Session = Depends(get_db)):
    """
    Obtiene los detalles de un grupo de URLs específico
    """
    group = crud.get_url_group(db, group_id=group_id)
    if group is None:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    return group

@app.post("/update_url_groups/")
def update_url_groups(similarity_threshold: float = 0.8, db: Session = Depends(get_db)):
    """
    Actualiza los grupos de URLs similares
    """
    from .ml.url_clustering import group_similar_urls
    groups = group_similar_urls(db.connection(), similarity_threshold)
    return {"status": "success", "groups_updated": len(groups)}

# Rutas para cuentas
@app.get("/account/{account_id}", response_model=schemas.AccountDetailed)
def get_account(account_id: int, db: Session = Depends(get_db)):
    """
    Obtiene los detalles de una cuenta específica
    """
    account = crud.get_account(db, account_id=account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    return account

# Rutas para datos
@app.get("/dato/{dato_id}", response_model=schemas.DatoDetailed)
def get_dato(dato_id: int, db: Session = Depends(get_db)):
    """
    Obtiene los detalles de un dato específico
    """
    dato = crud.get_dato(db, dato_id=dato_id)
    if dato is None:
        raise HTTPException(status_code=404, detail="Dato no encontrado")
    return dato

if __name__ == "__main__":
    logger.info("Iniciando servidor API de LogInsight Pro")
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)