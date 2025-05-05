from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import schemas
from app.models import models
from app.database import SessionLocal

router = APIRouter(prefix="/usuario-personaje", tags=["usuario-personaje"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/usuario/{idUsuario}", response_model=List[schemas.UsuarioPersonaje])
def obtener_relaciones_por_usuario(idUsuario: int, db: Session = Depends(get_db)):
    relaciones = db.query(models.UsuarioPersonaje).filter(
        models.UsuarioPersonaje.idUsuario == idUsuario
    ).all()
    return relaciones

@router.post("/", response_model=schemas.UsuarioPersonaje)
def crear_relacion(relacion: schemas.UsuarioPersonaje, db: Session = Depends(get_db)):
    db_rel = models.UsuarioPersonaje(**relacion.dict())
    db.add(db_rel)
    db.commit()
    db.refresh(db_rel)
    return db_rel

@router.put("/{idUsuario}/{idPersonaje}", response_model=schemas.UsuarioPersonaje)
def actualizar_relacion(idUsuario: int, idPersonaje: int, datos: schemas.UsuarioPersonaje, db: Session = Depends(get_db)):
    relacion = db.query(models.UsuarioPersonaje).filter(
        models.UsuarioPersonaje.idUsuario == idUsuario,
        models.UsuarioPersonaje.idPersonaje == idPersonaje
    ).first()
    if not relacion:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    
    relacion.arma = datos.arma
    relacion.artefacto = datos.artefacto
    db.commit()
    db.refresh(relacion)
    return relacion

@router.delete("/{idUsuario}/{idPersonaje}")
def eliminar_relacion(idUsuario: int, idPersonaje: int, db: Session = Depends(get_db)):
    relacion = db.query(models.UsuarioPersonaje).filter(
        models.UsuarioPersonaje.idUsuario == idUsuario,
        models.UsuarioPersonaje.idPersonaje == idPersonaje
    ).first()
    if not relacion:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    
    db.delete(relacion)
    db.commit()
    return {"ok": True, "mensaje": "Relación eliminada correctamente"}
