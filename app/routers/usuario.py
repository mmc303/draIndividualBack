from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import schemas
from app.crud import crud
from app.database import SessionLocal
from typing import List

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Usuario)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return crud.create_usuario(db, usuario)

@router.delete("/{idUsuario}")
def eliminar_usuario(idUsuario: int, db: Session = Depends(get_db)):
    return crud.delete_usuario(db, idUsuario)