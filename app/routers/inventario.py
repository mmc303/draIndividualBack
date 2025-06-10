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
    '''Obtiene el inventario de un usuario con detalles del objeto.'''
    inventario = db.query(models.Inventario).filter(models.Inventario.idUsuario == idUsuario).all()
    if not inventario:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")

    inventario_detallado = []
    for item in inventario:
        objeto = db.query(models.ObjetoInventario).filter(models.ObjetoInventario.idObjetoApi == item.idObjetoApi).first()
        if objeto:
            inventario_detallado.append({
                "idUsuario": item.idUsuario,
                "idObjetoApi": objeto.idObjetoApi,
                "nombreObjeto": objeto.nombreObjeto,
                "rarezaObjeto": objeto.rarezaObjeto,
                "imagenObjeto": objeto.imagenObjeto,
                "cantidadObjeto": item.cantidadObjeto,
            })
    return inventario_detallado

@router.post("/{idUsuario}", response_model=dict)
def add_inventario(idUsuario: int, item: schemas.InventarioBase, db: Session = Depends(get_db)):
    '''Agrega un objeto al inventario de un usuario y retorna detalles del objeto.'''
    nuevo = models.Inventario(idUsuario=idUsuario, idObjetoApi=item.idObjetoApi, cantidadObjeto=item.cantidadObjeto)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return {"message": "Objeto agregado al inventario"}

@router.put("/{idUsuario}", response_model=dict)
def update_inventario(idUsuario: int, item: schemas.InventarioBase, db: Session = Depends(get_db)):
    '''Modifica la cantidad de un objeto en el inventario de un usuario y retorna detalles del objeto.'''
    inv = db.query(models.Inventario).filter(
        models.Inventario.idUsuario == idUsuario,
        models.Inventario.idObjetoApi == item.idObjetoApi
    ).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Objeto no encontrado en inventario")

    inv.cantidadObjeto = item.cantidadObjeto
    db.commit()
    db.refresh(inv)
    return {"message": "Objeto agregado al inventario"}
