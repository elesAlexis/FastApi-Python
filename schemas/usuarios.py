# app/models/usuarios.py
from pydantic import BaseModel, EmailStr, Field

# Para loguear un usuario
class UsuarioLogin(BaseModel):
    email: str
    password: str

# Para crear un usuario
class UsuarioCrear(BaseModel):
    nombre: str
    email: EmailStr
    contrasena: str

# Para modificar un usuario
class UsuarioModificar(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    contrasena: str   

# Para eliminar un usuario
class UsuarioEliminar(BaseModel):
    id: int

# Para devolver info de un usuario (sin contraseña)
class UsuarioListar(BaseModel):
    id: int
    nombre: str
    email: EmailStr

