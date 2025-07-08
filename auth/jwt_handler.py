from datetime import datetime, timedelta
from jose import jwt, JWTError
from dotenv import load_dotenv
import os


load_dotenv()

# Usar las variables desde el entorno
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRATION_MINUTES = int(os.getenv("EXPIRATION_MINUTES", 30))  # Usa 30 como valor por defecto

def crear_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRATION_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None