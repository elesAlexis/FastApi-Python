from pydantic import BaseModel
from typing import Optional
from enum import Enum

class TipoContenido(str, Enum):
    pelicula = 'pelicula'
    serie = 'serie'

class ContenidoCrear(BaseModel):
    titulo: str
    descripcion: Optional[str]
    fecha_lanzamiento: Optional[str]
    tipo_contenido: TipoContenido

class ContenidoModificar(BaseModel):
    id: int
    titulo: str
    descripcion: Optional[str]
    fecha_lanzamiento: Optional[str]
    tipo_contenido: TipoContenido

class ContenidoEliminar(BaseModel):
    id: int

class ContenidoListar(BaseModel):
    id: int
    titulo: str
    descripcion: Optional[str]
    fecha_lanzamiento: Optional[str]
    tipo_contenido: TipoContenido