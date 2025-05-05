from pydantic import BaseModel
from typing import Optional, List, Dict

class UsuarioBase(BaseModel):
    correo: str

class UsuarioCreate(UsuarioBase):
    contrasena: str

class Usuario(UsuarioBase):
    idUsuario: int
    class Config:
        orm_mode = True

class PersonajeBase(BaseModel):
    nombrePersonaje: str

class Personaje(PersonajeBase):
    idPersonaje: int
    class Config:
        orm_mode = True

class UsuarioPersonaje(BaseModel):
    idUsuario: int
    idPersonaje: int
    arma: Optional[str]
    artefacto: Optional[str]
    class Config:
        orm_mode = True

class EquipoBase(BaseModel):
    canonicalKey: str
    detalles: Dict

class Equipo(EquipoBase):
    idEquipo: int
    class Config:
        orm_mode = True

class AbismoBase(BaseModel):
    patch: str
    listaPersonajes: Dict
    listaEquipos: Dict
    class Config:
        orm_mode = True

class Abismo(AbismoBase):
    idAbismo: int
    class Config:
        orm_mode = True