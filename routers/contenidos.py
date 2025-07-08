from fastapi import APIRouter
from typing import List
from schemas.contenidos import ContenidoListar
from services.contenidos_service import obtener_contenidos

router = APIRouter()

@router.get("/contenidos", response_model=List[ContenidoListar], tags=["Contenidos"])
def listar_contenidos():
    return obtener_contenidos()