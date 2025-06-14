from pydantic import BaseModel
from typing import Optional, List, Dict

#Objeto base
class ObjetoInventario(BaseModel):
    idObjetoApi: int
    nombreObjeto: str
    rarezaObjeto: int
    imagenObjeto: str
    class Config:
        model_config = {"from_attributes": True}

# Relación usuario-inventario
class InventarioBase(BaseModel):
    idObjetoApi: int
    cantidadObjeto: int

class Inventario(InventarioBase):
    idUsuario: int
    class Config:
        model_config = {"from_attributes": True}

#Usuario
class UsuarioBase(BaseModel):
    correo: str

class UsuarioCreate(UsuarioBase):
    contrasena: str

class Usuario(UsuarioBase):
    idUsuario: int
    inventario: Optional[List[Inventario]] = []
    class Config:
        model_config = {"from_attributes": True}

#Personaje
class Material(BaseModel):
    idMaterial: int
    nombreMaterial: str
    cantidadMaterial: int
    imagenMaterial: str

class PersonajeBase(BaseModel):
    nombrePersonaje: str
    elemento: str
    rareza: int
    urlImagen: str
    ascensiones: Dict[str, List[Material]]
    talentos: Dict[str, List[Material]]

class Personaje(PersonajeBase):
    idPersonaje: int
    class Config:
        model_config = {"from_attributes": True}

#Relación usuario-personaje
class UsuarioPersonajeBase(BaseModel):
    arma: Optional[str]
    artefacto: Optional[str]
    constelacion: int
    nivel: int
    nivelDeseado: int
    ascension: int
    ascensionDeseada: int
    talentos: Dict[str, int]
    talentosDeseados: Dict[str, int]

class UsuarioPersonaje(UsuarioPersonajeBase):
    idUsuario: int
    idPersonaje: int
    class Config:
        model_config = {"from_attributes": True}

#Equipo
class PersonajeEquipo(BaseModel):
    personaje: str
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
        model_config = {"from_attributes": True}

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
        model_config = {"from_attributes": True}