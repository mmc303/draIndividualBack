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
    elemento: str
    urlImagen: str

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


#Equipo
class PersonajeEquipo(BaseModel):
    personaje: PersonajeBase
    arma: Optional[str]
    artefacto: Optional[str]

class DetallesEquipo(BaseModel):
    personajes: List[PersonajeEquipo]
    justificacion: str
    rotacion: str

class EquipoBase(BaseModel):
    canonicalKey: str
    detalles: DetallesEquipo

class Equipo(EquipoBase):
    idEquipo: int
    class Config:
        orm_mode = True


#Abismo
class PersonajeAbismo(BaseModel):
    personaje: PersonajeBase
    usoPersonaje: float

class EquipoAbismo(BaseModel):
    personajes: List[PersonajeBase]
    usoEquipo: float
    ratio: str

class AbismoBase(BaseModel):
    version: str
    listaPersonajes: List[PersonajeAbismo]
    listaEquipos: List[EquipoAbismo]

class Abismo(BaseModel):
    idAbismo: int
    class Config:
        orm_mode = True