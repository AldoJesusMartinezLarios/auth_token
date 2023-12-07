import fastapi
import sqlite3
import random
import datetime
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPBasic, HTTPBasicCredentials

app = fastapi.FastAPI()

securityBearer = HTTPBearer()

@app.get("/")
def auth(credentials: HTTPBearer = Depends(securityBearer)):
    """Autenticación con token fijo"""
    token = credentials.credentials
    connx = sqlite3.connect("sql/usuarios.db")
    c = connx.cursor()
    c.execute('SELECT token FROM usuarios WHERE token = ?', (token,))
    existe = c.fetchone()

    if existe is None:
        raise HTTPException(status_code=401, detail="Not Authenticated")
    else:
        return {"mensaje": "Hola Mundo"}


security = HTTPBasic()

@app.post("/token")
def get_token(username: str = fastapi.Form(...), password: str = fastapi.Form(...)):
    """Obtener token si las credenciales son correctas"""
    connx = sqlite3.connect("sql/usuarios.db")
    c = connx.cursor()

    c.execute('SELECT * FROM usuarios WHERE username = ? AND password = ?', (username, password))
    user_exists = c.fetchone()
    if user_exists:
        token = user_exists[2]  # Suponiendo que el token está en la tercera columna de la tabla usuarios
        return {"token": token}
    else:
        raise HTTPException(status_code=401, detail="Not Authenticated")
