from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import schemas
from app.models import models
from app.database import SessionLocal

router = APIRouter(prefix="/inventario", tags=["inventario"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Inventario de usuario
@router.get("/{idUsuario}", response_model=list[schemas.Inventario])
def get_inventario(idUsuario: int, db: Session = Depends(get_db)):
    '''Obtiene el inventario de un usuario.'''
    inventario = db.query(models.Inventario).filter(models.Inventario.idUsuario == idUsuario).all()
    if not inventario:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    return inventario

@router.post("/{idUsuario}", response_model=schemas.Inventario)
def add_inventario(idUsuario: int, item: schemas.InventarioBase, db: Session = Depends(get_db)):
    '''Agrega un objeto al inventario de un usuario (si existe suma la cantidad).'''
    inv = db.query(models.Inventario).filter(
        models.Inventario.idUsuario == idUsuario,
        models.Inventario.idObjetoApi == item.idObjetoApi
    ).first()
    if inv:
        inv.cantidadObjeto += item.cantidadObjeto
        db.commit()
        db.refresh(inv)
        return inv
    else:
        nuevo = models.Inventario(idUsuario=idUsuario, idObjetoApi=item.idObjetoApi, cantidadObjeto=item.cantidadObjeto)
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return nuevo

@router.put("/{idUsuario}", response_model=schemas.Inventario)
def update_inventario(idUsuario: int, item: schemas.InventarioBase, db: Session = Depends(get_db)):
    '''Modifica la cantidad de un objeto en el inventario de un usuario.'''
    inv = db.query(models.Inventario).filter(
        models.Inventario.idUsuario == idUsuario,
        models.Inventario.idObjetoApi == item.idObjetoApi
    ).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Objeto no encontrado en inventario")
    inv.cantidadObjeto = item.cantidadObjeto
    db.commit()
    db.refresh(inv)
    return inv
