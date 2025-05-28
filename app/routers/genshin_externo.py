import requests
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/genshin", tags=["genshin"])

@router.get("/externo/{nombre}")
def obtener_personaje_externo(nombre: str):
    url = f"https://genshin-db-api.vercel.app/api/v5/characters?query={nombre}&queryLanguages=spanish&resultLanguage=spanish"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Error al consultar la API externa: {str(e)}")
