from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import usuario, personaje, equipo, usuariopersonaje, abismo, auth, genshin_externo
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuario.router)
app.include_router(personaje.router)
app.include_router(equipo.router)
app.include_router(usuariopersonaje.router)
app.include_router(abismo.router)
app.include_router(auth.router)
app.include_router(genshin_externo.router)