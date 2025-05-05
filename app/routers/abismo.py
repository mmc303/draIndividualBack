from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import models
from app.schemas import schemas
from typing import List

router = APIRouter(prefix="/abismo", tags=["abismo"])

@router.get("/{idAbismo}", response_model=schemas.Abismo)
def obtener_abismo(idAbismo: int, db: Session = Depends(get_db)):
    abismo = db.query(models.Abismo).filter(models.Abismo.idAbismo == idAbismo).first()
    if not abismo:
        raise HTTPException(status_code=404, detail="Abismo no encontrado")
    return abismo

@router.post("/", response_model=schemas.Abismo)
def crear_abismo(abismo: schemas.AbismoBase, db: Session = Depends(get_db)):
    nuevo_abismo = models.Abismo(**abismo.dict())
    db.add(nuevo_abismo)
    db.commit()
    db.refresh(nuevo_abismo)
    return nuevo_abismo
