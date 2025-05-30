from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import schemas
from app.crud import crud
from app.database import SessionLocal

router = APIRouter(prefix="/inventario", tags=["inventario"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Inventario)
def add_inventario(idUsuario: int, item: schemas.Inventario, db: Session = Depends(get_db)):
    '''Agrega un objeto al inventario de un usuario (si existe suma la cantidad).'''
    return crud.add_inventario(db, idUsuario, item)

@router.put("/", response_model=schemas.Inventario)
def update_inventario(idUsuario: int, item: schemas.Inventario, db: Session = Depends(get_db)):
    '''Modifica la cantidad de un objeto en el inventario de un usuario.'''
    return crud.update_inventario(db, idUsuario, item)

@router.get("/{idUsuario}", response_model=list[schemas.Inventario])
def get_inventario(idUsuario: int, db: Session = Depends(get_db)):
    '''Obtiene el inventario de un usuario.'''
    inventario = crud.get_inventario(db, idUsuario)
    if not inventario:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    return inventario

@router.get("/objetos", response_model=list[schemas.ObjetoInventario])
def get_objetos(db: Session = Depends(get_db)):
    '''Obtiene todos los objetos disponibles en la base de datos.'''
    objetos = crud.get_objetos(db)
    if not objetos:
        raise HTTPException(status_code=404, detail="No se encontraron objetos")
    return objetos