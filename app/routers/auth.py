from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_db
from app.schemas import schemas

router = APIRouter(tags=["auth"])

@router.post("/login")
def login(response: Response, form_data: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.correo, form_data.contrasena)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": str(user.idUsuario)}, expires_delta=access_token_expires)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return {"mensaje": "Inicio de sesión exitoso"}