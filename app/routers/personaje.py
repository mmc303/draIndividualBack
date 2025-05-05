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

@router.post("/", response_model=schemas.Personaje)
def crear_personaje(personaje: schemas.PersonajeBase, db: Session = Depends(get_db)):
    db_personaje = models.Personaje(**personaje.dict())
    db.add(db_personaje)
    db.commit()
    db.refresh(db_personaje)
    return db_personaje