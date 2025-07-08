from fastapi import APIRouter, Depends
from typing import List
from schemas.usuarios import UsuarioCrear, UsuarioModificar, UsuarioListar, UsuarioEliminar 
from services.usuarios_service import crear_usuario, modificar_usuario, eliminar_usuario, obtener_usuario_por_id, obtener_usuarios
from auth.deps import get_current_user, rol_requerido

router = APIRouter()

@router.post("/usuarios", response_model=UsuarioListar, status_code=201, tags=["Usuarios"])
async def crear(usuario: UsuarioCrear, _ = Depends(rol_requerido("admin"))):
    return crear_usuario(usuario)

@router.put("/usuarios/{id}", response_model=UsuarioListar, tags=["Usuarios"])
async def modificar(id: int, usuario: UsuarioModificar, _ = Depends(rol_requerido("admin"))):
    usuario.id = id
    return modificar_usuario(usuario)

@router.delete("/usuarios/{id}", status_code=204, tags=["Usuarios"])
async def eliminar(id: int, _ = Depends(rol_requerido("admin"))):
    usuario = UsuarioEliminar(id=id)
    eliminar_usuario(usuario)
    return

@router.get("/usuarios/{id}", response_model=UsuarioListar, tags=["Usuarios"])
async def por_id(id:int, _ = Depends(rol_requerido("admin"))):
    return obtener_usuario_por_id(id)

@router.get("/usuarios", response_model=List[UsuarioListar], tags=["Usuarios"])
async def listar_usuarios(skip: int = 0, limit: int = 100, _ =Depends(rol_requerido("admin"))):
    return obtener_usuarios(skip=skip, limit=limit)
