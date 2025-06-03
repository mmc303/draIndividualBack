from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import usuario, personaje, equipo, abismo, usuariopersonaje, inventario, auth, genshin_externo, scrap, objetoinventario
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
app.include_router(abismo.router)
app.include_router(usuariopersonaje.router)
app.include_router(inventario.router)
app.include_router(objetoinventario.router)
app.include_router(auth.router)
app.include_router(genshin_externo.router)
app.include_router(scrap.router)
