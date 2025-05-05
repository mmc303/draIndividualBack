from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import schemas
from app.models import models
from app.database import SessionLocal

router = APIRouter(prefix="/equipos", tags=["equipos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.Equipo])
def listar_equipos(db: Session = Depends(get_db)):
    return db.query(models.Equipo).all()

@router.post("/", response_model=schemas.Equipo)
def crear_equipo(equipo: schemas.EquipoBase, db: Session = Depends(get_db)):
    db_equipo = models.Equipo(**equipo.dict())
    db.add(db_equipo)
    db.commit()
    db.refresh(db_equipo)
    return db_equipo