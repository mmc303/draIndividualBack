from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuario"
    idUsuario = Column(Integer, primary_key=True, index=True)
    correo = Column(String, unique=True, index=True, nullable=False)
    contrasena = Column(String, nullable=False)
    personaje_usuario = relationship("UsuarioPersonaje", back_populates="usuario")

class Personaje(Base):
    __tablename__ = "personaje"
    idPersonaje = Column(Integer, primary_key=True, index=True)
    nombrePersonaje = Column(String, unique=True, index=True, nullable=False)
    elemento = Column(String, nullable=False)
    urlImagen = Column(String, nullable=False)
    usuarios_personaje = relationship("UsuarioPersonaje", back_populates="personaje")

class UsuarioPersonaje(Base):
    __tablename__ = "usuariopersonaje"
    idUsuario = Column(Integer, ForeignKey("usuario.idUsuario", ondelete="CASCADE"), primary_key=True)
    idPersonaje = Column(Integer, ForeignKey("personaje.idPersonaje", ondelete="CASCADE"), primary_key=True)
    arma = Column(String)
    artefacto = Column(String)
    usuario = relationship("Usuario", back_populates="personaje_usuario")
    personaje = relationship("Personaje", back_populates="usuarios_personaje")

class Equipo(Base):
    __tablename__ = "equipo"
    idEquipo = Column(Integer, primary_key=True, index=True)
    canonicalKey = Column(String, unique=True, index=True, nullable=False)
    detalles = Column(JSONB, nullable=False)

class Abismo(Base):
    __tablename__ = "abismo"
    idAbismo = Column(Integer, primary_key=True, index=True) 
    version = Column(String, nullable=False) #Version 1.0A / Version 5.4B
    listaPersonajes = Column(JSONB, nullable=False)
    listaEquipos = Column(JSONB, nullable=False)

class ObjetoInventario(Base):
    __tablename__ = "objetoinventario"
    idObjetoApi = Column(Integer, primary_key=True, index=True)
    nombreObjeto = Column(String, nullable=False)
    rarezaObjeto = Column(Integer, nullable=False)
    imagenObjeto = Column(String, nullable=False)

class Inventario(Base):
    __tablename__ = "inventario"
    idUsuario = Column(Integer, ForeignKey("usuario.idUsuario", ondelete="CASCADE"), primary_key=True)
    idObjetoApi = Column(Integer, ForeignKey("objetoinventario.idObjetoApi", ondelete="CASCADE"), primary_key=True)
    cantidadObjeto = Column(Integer, nullable=False)