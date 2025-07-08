from database.connection import ConnectionFactory
from schemas.usuarios import UsuarioCrear, UsuarioModificar, UsuarioListar, UsuarioEliminar
from fastapi import HTTPException, status

import bcrypt

def hash_password(password: str) -> str:
    # Genera el salt y hashea la contraseña (en bytes)
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    # Lo convertimos a string para guardar en DB
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def autenticar_usuario(email: str, password: str):
    conn = ConnectionFactory.create_connection()
    cursor = conn.cursor()

    query = """
        SELECT id, nombre, email, contrasena, rol
        FROM usuarios
        WHERE email = ?
    """

    cursor.execute(query, (email,))
    row = cursor.fetchone()
    conn.close()

    if row and verify_password(password, row.contrasena):
        print("Encuentro usuario")
        print(row.id)
        return {
            "id": row.id,
            "username": row.nombre,
            "email": row.email,
            "rol": row.rol
        }
    
    return None

def crear_usuario(usuario: UsuarioCrear) -> UsuarioListar:
    usuario.contrasena = hash_password(usuario.contrasena)
    conn = ConnectionFactory.create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO usuarios (nombre, email, contrasena)
        OUTPUT INSERTED.id, INSERTED.nombre, INSERTED.email
        VALUES (?, ?, ?)""", 
        (usuario.nombre, usuario.email, usuario.contrasena))

    row = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    return UsuarioListar(
        id=row.id,
        nombre=row.nombre,
        email=row.email
    )

def modificar_usuario(usuario: UsuarioModificar) -> UsuarioListar:
    conn = ConnectionFactory.create_connection()
    usuario.contrasena = hash_password(usuario.contrasena)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET nombre = ?, email = ?, contrasena = ?
        OUTPUT INSERTED.id, INSERTED.nombre, INSERTED.email
        WHERE id = ? """, 
    (usuario.nombre, usuario.email, usuario.contrasena, usuario.id))

    row = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    return UsuarioListar(
        id=row.id,
        nombre=row.nombre,
        email=row.email
    )

def eliminar_usuario(usuario: UsuarioEliminar) ->  None :
    conn = ConnectionFactory.create_connection()
    cursor = conn.cursor()

    cursor.execute("""DELETE FROM usuarios WHERE id = ?""", (usuario.id,))
    conn.commit()

    cursor.close()
    conn.close()

    # Verificar si se eliminó alguna fila
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id {user_id} no encontrado"
        )

    cursor.close()
    conn.close()

    
def obtener_usuario_por_id(user_id: int) -> UsuarioListar:
    conn = ConnectionFactory.create_connection()
    cursor = conn.cursor()

    cursor.execute("""SELECT id, nombre, email
                   FROM usuarios
                   WHERE id = ?""", (user_id))
    
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if not row:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id {user_id} no encontrado"
        )

    return UsuarioListar(
        id=row.id,
        nombre=row.nombre,
        email=row.email

    )
 
def obtener_usuarios(skip: int = 0, limit: int = 100):
    conn = ConnectionFactory.create_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
                    SELECT id, nombre, email
                    FROM usuarios
                    ORDER BY id
                    OFFSET ? ROWS
                    FETCH NEXT ? ROWS ONLY
                    """,
        (skip, limit),
    )
    rows = cursor.fetchall()
    return [
        UsuarioListar(
            id=row[0],
            nombre=row[1],
            email=row[2],
        )
        for row in rows
    ]





