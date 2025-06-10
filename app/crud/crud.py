from sqlalchemy.orm import Session
from app.schemas import schemas
from app.models import models
from app.auth import get_password_hash

def get_usuario(db: Session, correo: str):
    usuario = db.query(models.Usuario).filter(models.Usuario.correo == correo).first()
    return { "idUsuario": usuario.idUsuario, "correo": usuario.correo }

def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    hashed_password = get_password_hash(usuario.contrasena)
    db_usuario = models.Usuario(
        correo=usuario.correo,
        contrasena=hashed_password
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    # Crear inventario vacío para cada objeto existente
    objetos = db.query(models.ObjetoInventario).all()
    for obj in objetos:
        db_inventario = models.Inventario(
            idUsuario=db_usuario.idUsuario,
            idObjetoApi=obj.idObjetoApi,
            cantidadObjeto=0
        )
        db.add(db_inventario)
    db.commit()
    usuario = get_usuario(db, usuario.correo)
    return usuario

def get_usuarios(db: Session):
    return db.query(models.Usuario).all()