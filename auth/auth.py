from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from services.usuarios_service import autenticar_usuario
from auth.jwt_handler import crear_token
from schemas.usuarios import UsuarioLogin

router = APIRouter()

@router.post("/login", tags=["Autenticación"])
async def login(user: UsuarioLogin):
    usuario = autenticar_usuario(user.email, user.password)
    if not usuario:
        raise HTTPException(status_code=400, detail="Credenciales inválidas")
    
    print(usuario)
    token = crear_token({"sub": str(usuario.get("id")), "rol": usuario.get("rol")})
    return {"access_token": token, "token_type": "bearer"}
