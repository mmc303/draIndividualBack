from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import schemas
from app.models import models
from app.database import SessionLocal

router = APIRouter(prefix="/objetoinventario", tags=["objetoinventario"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.ObjetoInventario])
def get_objetos(db: Session = Depends(get_db)):
    '''Obtiene todos los objetos disponibles en la base de datos.'''
    objetos = db.query(models.ObjetoInventario).all()
    if not objetos:
        raise HTTPException(status_code=404, detail="No se encontraron objetos")
    return objetos

@router.post("/", response_model=schemas.ObjetoInventario)
def create_objeto_inventario(objeto: schemas.ObjetoInventario, db: Session = Depends(get_db)):
    '''Crea un nuevo objeto en la base de datos.'''
    db_objeto = models.ObjetoInventario(**objeto.dict())
    db.add(db_objeto)
    db.commit()
    db.refresh(db_objeto)
    return db_objeto
