import fastapi
import sqlite3
import hashlib
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer

app = fastapi.FastAPI()

securityBearer = HTTPBearer()

def md5_hash(text):
    """Función para calcular el hash MD5 de una cadena"""
    return hashlib.md5(text.encode()).hexdigest()

# Almacenamiento de sesiones en memoria (no recomendado para producción)
sessions = {}

class Session:
    def __init__(self):
        self.token = None

@app.middleware("http")
async def add_session(request: Request, call_next):
    request.state.session = Session()
    response = await call_next(request)
    return response

@app.get("/")
def auth(credentials: HTTPBearer = Depends(securityBearer), session: Session = Depends()):
    """Autenticación con token fijo"""
    token = credentials.credentials
    connx = sqlite3.connect("sql/usuarios.db")
    c = connx.cursor()
    c.execute('SELECT token FROM usuarios WHERE token = ?', (token,))
    existe = c.fetchone()

    if existe is None:
        raise HTTPException(status_code=401, detail="Not Authenticated")
    else:
        # Almacenar el token en la sesión
        session.token = token
        # Almacenar la sesión en el diccionario (no recomendado para producción)
        sessions[token] = session
        return {"mensaje": "Hola Mundo"}

security = HTTPBearer()

@app.post("/token")
def get_token(username: str = fastapi.Form(...), password: str = fastapi.Form(...), session: Session = Depends()):
    """Obtener token si las credenciales son correctas"""
    connx = sqlite3.connect("sql/usuarios.db")
    c = connx.cursor()

    hashed_password = md5_hash(password)

    c.execute('SELECT * FROM usuarios WHERE username = ? AND password = ?', (username, hashed_password))
    user_exists = c.fetchone()

    if user_exists:
        token = user_exists[2]  # Suponiendo que el token está en la tercera columna de la tabla usuarios
        # Almacenar el token en la sesión
        session.token = token
        # Almacenar la sesión en el diccionario (no recomendado para producción)
        sessions[token] = session
        return {"token": token}
    else:
        raise HTTPException(status_code=401, detail="Not Authenticated")
