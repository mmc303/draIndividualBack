from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import schemas
from app.models import models
from app.database import SessionLocal

router = APIRouter(prefix="/personajes", tags=["personajes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.Personaje])
def listar_personajes(db: Session = Depends(get_db)):
    return db.query(models.Personaje).all()

@router.get("/{idPersonaje}", response_model=schemas.Personaje)
def obtener_personaje(idPersonaje: int, db: Session = Depends(get_db)):
    db_personaje = db.query(models.Personaje).filter(models.Personaje.idPersonaje == idPersonaje).first()
    if not db_personaje:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")
    return db_personaje

@router.get("/nombre/{nombre}", response_model=schemas.Personaje)
def obtener_personaje_por_nombre(nombre: str, db: Session = Depends(get_db)):
    db_personaje = db.query(models.Personaje).filter(models.Personaje.nombrePersonaje.contains(nombre)).first()
    if not db_personaje:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")
    return db_personaje

@router.post("/", response_model=schemas.Personaje)
def crear_personaje(personaje: schemas.PersonajeBase, db: Session = Depends(get_db)):
    db_personaje = models.Personaje(**personaje.dict())
    db.add(db_personaje)
    db.commit()
    db.refresh(db_personaje)
    return db_personaje

@router.delete("/", response_model=List[schemas.Personaje])
def eliminar_todos_personajes(db: Session = Depends(get_db)):
    personajes = db.query(models.Personaje).all()
    if not personajes:
        raise HTTPException(status_code=404, detail="No hay personajes para eliminar")
    for personaje in personajes:
        db.delete(personaje)
    db.commit()
    return personajes
