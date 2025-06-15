from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import schemas
from app.models import models
from app.database import SessionLocal
import os
from google import genai

router = APIRouter(prefix="/equipos", tags=["equipos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.Equipo])
def listar_equipos(db: Session = Depends(get_db)):
    return db.query(models.Equipo).all()

@router.get("/{nombre}", response_model=schemas.Equipo)
def obtener_equipo(nombre: str, db: Session = Depends(get_db)):
    # Buscar por primer personaje en detalles.personajes
    db_equipo = buscar_equipo_por_primer_personaje(nombre, db)
    if db_equipo is None:
        # Si no existe, generar con IA
        equipo = generar_equipo_ia(nombre, db)
        if not equipo:
            raise HTTPException(status_code=404, detail="Equipo no encontrado")
    else:
        # Si es dict, devolver tal cual; si es objeto, mapear a dict
        if isinstance(db_equipo, dict):
            equipo = db_equipo
        else:
            equipo = {
                "canonicalKey": db_equipo.canonicalKey,
                "detalles": db_equipo.detalles,
                "idEquipo": db_equipo.idEquipo
            }
    return equipo

def generar_equipo_ia(personaje: str, db: Session = Depends(get_db)):
    import logging
    import time
    import json
    api_key = os.environ.get("AI_API_KEY")
    retries = 5
    while not api_key and retries > 0:
        time.sleep(1)
        api_key = os.environ.get("AI_API_KEY")
        retries -= 1
    if not api_key:
        raise HTTPException(status_code=500, detail="API key de IA no configurada")

    prompt = f"""
Dame una composición de equipo para Genshin Impact (4 personajes) basada en el personaje {personaje}.
Devuélvelo en formato JSON exactamente así (sin bloques de código ni texto adicional) y en español:
Usa este sitio para obtener el nombre en ingles de las armas: https://github.com/theBowja/genshin-db/tree/main/src/data/English/weapons
Usa este sitio para obtener el nombre en ingles de los artefactos: https://github.com/theBowja/genshin-db/tree/main/src/data/English/artifacts
Devuelve siempre 2 armas y 2 artefactos óptimos por personaje.

{{
  \"personajes\": [
    {{
      \"personaje\": \"{personaje}\",
      \"arma\": \"Arma óptima 1, Arma óptima 2\",
      \"artefacto\": \"Artefacto óptimo 1, Artefacto óptimo 2\"
    }},
    {{
      \"personaje\": \"Nombre del personaje 2\",
      \"arma\": \"Arma óptima 1, Arma óptima 2\",
      \"artefacto\": \"Artefacto óptimo 1, Artefacto óptimo 2\"
    }},
    {{
      \"personaje\": \"Nombre del personaje 3\",
      \"arma\": \"Arma óptima 1, Arma óptima 2\",
      \"artefacto\": \"Artefacto óptimo 1, Artefacto óptimo 2\"
    }},
    {{
      \"personaje\": \"Nombre del personaje 4\",
      \"arma\": \"Arma óptima 1, Arma óptima 2\",
      \"artefacto\": \"Artefacto óptimo 1, Artefacto óptimo 2\"
    }}
  ],
  \"justificacion\": \"Explica brevemente el rol y sinergia de cada personaje en el equipo.\",
  \"rotacion\": \"Describe la rotación recomendada de habilidades entre los personajes.\"
}}

No incluyas ningún texto antes o después del JSON.
Asegúrate de que los campos sean exactamente: personajes (lista de objetos), justificacion (string), rotacion (string).
El personaje principal ({personaje}) debe ser el primero en la lista.
"""

    client = genai.Client(api_key=api_key)
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        ia_text = response.text
        logging.warning(f"[DEBUG] IA text: {ia_text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar la IA: {str(e)}")

    ia_text = ia_text.strip()
    if ia_text.startswith('```json'):
        ia_text = ia_text[7:]
    if ia_text.startswith('```'):
        ia_text = ia_text[3:]
    if ia_text.endswith('```'):
        ia_text = ia_text[:-3]
    ia_text = ia_text.strip()

    try:
        equipo_json = json.loads(ia_text)
    except Exception:
        raise HTTPException(status_code=500, detail=f"La IA no devolvió un JSON válido: {ia_text}")

    detalles = equipo_json.get("detalles", equipo_json)

    # Normalizar campos
    for p in detalles.get('personajes', []):
        if isinstance(p.get('arma'), list):
            p['arma'] = ', '.join(map(str, p['arma']))
        if isinstance(p.get('artefacto'), list):
            p['artefacto'] = ', '.join(map(str, p['artefacto']))
        if 'arma' not in p:
            p['arma'] = ''
        if 'artefacto' not in p:
            p['artefacto'] = ''
        if 'personaje' not in p:
            p['personaje'] = ''

    # Calcular canonicalKey
    nombres = [p.get('personaje', '').strip().lower() for p in detalles.get('personajes', [])]
    nombres.sort()
    canonical_key = ''.join(nombres).replace(' ', '')

    # Guardar en base de datos
    db_equipo = models.Equipo(canonicalKey=canonical_key, detalles=detalles)
    db.add(db_equipo)
    db.commit()
    db.refresh(db_equipo)

    # Retornar con idEquipo incluido
    return {
        "canonicalKey": db_equipo.canonicalKey,
        "detalles": db_equipo.detalles,
        "idEquipo": db_equipo.idEquipo
    }

def buscar_equipo_por_primer_personaje(nombre_personaje: str, db: Session):
    """
    Busca un equipo donde el primer elemento de detalles.personajes.personaje sea igual a nombre_personaje.
    """
    from sqlalchemy import text
    query = text("""
        SELECT * FROM equipo
        WHERE detalles->'personajes'->0->>'personaje' = :nombre
        LIMIT 1
    """)
    result = db.execute(query, {"nombre": nombre_personaje}).fetchone()
    if result:
        return {
            "idEquipo": result.idEquipo,
            "canonicalKey": result.canonicalKey,
            "detalles": result.detalles
        }
    return None

def buscar_equipo_por_personaje(nombre_personaje: str, db: Session):
    """
    Busca un equipo donde cualquier elemento de detalles.personajes.personaje sea igual a nombre_personaje,
    ignorando mayúsculas, minúsculas y tildes.
    """
    from sqlalchemy import text
    # Usamos unquery que recorre el array y normaliza para comparar sin tildes ni mayúsculas
    query = text("""
        SELECT * FROM equipo
        WHERE EXISTS (
            SELECT 1 FROM jsonb_array_elements(detalles->'personajes') AS p
            WHERE unaccent(lower(trim(p->>'personaje'))) = unaccent(lower(trim(:nombre)))
        )
        LIMIT 1
    """)
    result = db.execute(query, {"nombre": nombre_personaje}).fetchone()
    if result:
        return {
            "idEquipo": result.idEquipo,
            "canonicalKey": result.canonicalKey,
            "detalles": result.detalles
        }
    return None
