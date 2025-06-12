from fastapi import APIRouter, HTTPException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import requests
import time
from app.database import SessionLocal
from app.routers.objetoinventario import create_objeto_inventario
from app.routers.personaje import crear_personaje
from app.schemas.schemas import ObjetoInventario, Personaje

router = APIRouter(prefix="/scrap", tags=["scrap"])

@router.get("/items")
def scrap_items():
    url = "https://gi20.hakush.in/item"
    print('Iniciando scraping de', url)
    
    filters = [19, 20, 21, 22, 23, 26, 27, 28, 32] 
    print('Filtros a aplicar:', filters)

    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--lang=es-ES")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")

    driver = uc.Chrome(options=chrome_options)

    try:
        driver.get(url)
        print('Página cargada')

        # Cierre del popup de cookies
        try:
            overlay = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.fc-dialog-overlay'))
            )
            popup = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button, .fc-dialog-container button, .fc-cta-consent'))
            )
            popup.click()
            WebDriverWait(driver, 10).until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.fc-dialog-overlay'))
            )
            print('Cookies aceptadas')
            time.sleep(1)
        except Exception as e:
            print('No hay popup de cookies o no se pudo cerrar:', e)

        # Aplicar filtros
        for f in filters:
            try:
                print(f'Click en filtro {f}')
                btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, f"filter-{f}"))
                )
                btn.click()
                time.sleep(5)
            except:
                print(f'No se encontró el filtro {f}, continuando...')

        # Scroll progresivo
        grid_selector = 'div.grid.grid-cols-4.p-3.sm\\:grid-cols-5.md\\:grid-cols-6.lg\\:grid-cols-7.xl\\:grid-cols-8.h-100.text-slate-950'
        last_count = 0
        same_count_repeats = 0
        max_scrolls = 50

        for i in range(max_scrolls):
            try:
                grid = driver.find_element(By.CSS_SELECTOR, grid_selector)
                divs = grid.find_elements(By.CSS_SELECTOR, 'div.p-2.text-center')
                if divs:
                    driver.execute_script("arguments[0].scrollIntoView();", divs[-1])
                else:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2.5)

                new_divs = grid.find_elements(By.CSS_SELECTOR, 'div.p-2.text-center')
                print(f'Iteración scroll {i}: {len(new_divs)} elementos encontrados')

                if len(new_divs) == last_count:
                    same_count_repeats += 1
                    if same_count_repeats >= 3:
                        print('Fin del scroll, no hay más elementos nuevos.')
                        break
                else:
                    same_count_repeats = 0

                last_count = len(new_divs)
            except Exception as e:
                print('Error durante el scroll:', e)
                break

        # Extracción final de elementos
        items = []
        db = SessionLocal()
        grid = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, grid_selector))
        )
        divs = [d for d in grid.find_elements(By.CSS_SELECTOR, 'div.p-2.text-center') if d.is_displayed()]
        
        for idx, div in enumerate(divs):
            name = div.text.strip()
            print(f'Elemento {idx}: "{name}"')
            if not name:
                continue
            query_name = name.replace(' ', '%20')
            api_url = f"https://genshin-db-api.vercel.app/api/materials?query={query_name}&queryLanguages=english&resultLanguage=spanish"
            print(f'Consultando API para: {query_name}')
            resp = requests.get(api_url)
            if resp.status_code == 200:
                try:
                    data = resp.json()
                    item = {
                        'idObjetoApi': data.get('id'),
                        'nombreObjeto': data.get('name'),  
                        'rarezaObjeto': data.get('rarity') if data.get('rarity') else 0,
                        'imagenObjeto': data.get('images', {}).get('nameicon')
                    }
                    items.append(item)
                    # Guardar en la base de datos
                    if item['idObjetoApi'] and item['nombreObjeto'] and item['rarezaObjeto'] and item['imagenObjeto']:
                        try:
                            objeto_schema = ObjetoInventario(**item)
                            create_objeto_inventario(objeto=objeto_schema, db=db)
                        except Exception as db_ex:
                            print(f'Error guardando en base de datos: {db_ex}')
                    print(f'Item recogido: {item}')
                except Exception as ex:
                    print(f'Error parseando JSON para {query_name}:', ex)
            else:
                print(f'Error en API {query_name}: {resp.status_code}')
        db.close()
        driver.quit()
        print(f'Total items recogidos: {len(items)}')
        return items

    except Exception as e:
        driver.quit()
        print('Error en scraping:', e)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/characters")
def scrap_characters():
    url = "https://gi20.hakush.in/character"
    print('Iniciando scraping de', url)
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--lang=es-ES")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")

    driver = uc.Chrome(options=chrome_options)

    try:
        driver.get(url)
        print('Página de personajes cargada')
        # Cierre del popup de cookies
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.fc-dialog-overlay'))
            )
            popup = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button, .fc-dialog-container button, .fc-cta-consent'))
            )
            popup.click()
            WebDriverWait(driver, 10).until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.fc-dialog-overlay'))
            )
            print('Cookies aceptadas')
            time.sleep(1)
        except Exception as e:
            print('No hay popup de cookies o no se pudo cerrar:', e)

        # Scroll progresivo
        grid_selector = 'div.grid.grid-cols-4.p-3.sm\\:grid-cols-5.md\\:grid-cols-6.lg\\:grid-cols-7.xl\\:grid-cols-8.h-100.text-slate-950'
        last_count = 0
        same_count_repeats = 0
        max_scrolls = 50

        for i in range(max_scrolls):
            try:
                grid = driver.find_element(By.CSS_SELECTOR, grid_selector)
                divs = grid.find_elements(By.CSS_SELECTOR, 'div.p-2.text-center')
                if divs:
                    driver.execute_script("arguments[0].scrollIntoView();", divs[-1])
                else:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2.5)

                new_divs = grid.find_elements(By.CSS_SELECTOR, 'div.p-2.text-center')
                print(f'Iteración scroll {i}: {len(new_divs)} elementos encontrados')

                if len(new_divs) == last_count:
                    same_count_repeats += 1
                    if same_count_repeats >= 3:
                        print('Fin del scroll, no hay más elementos nuevos.')
                        break
                else:
                    same_count_repeats = 0

                last_count = len(new_divs)
            except Exception as e:
                print('Error durante el scroll:', e)
                break

        # Extracción final de personajes
        characters = []
        grid = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, grid_selector))
        )
        divs = [d for d in grid.find_elements(By.CSS_SELECTOR, 'div.p-2.text-center') if d.is_displayed()]
        for idx, div in enumerate(divs):
            name = div.text.strip()
            print(f'Personaje {idx}: "{name}"')
            if not name:
                continue
            query_name = name.replace(' ', '%20')
            api_url = f"https://genshin-db-api.vercel.app/api/characters?query={query_name}&queryLanguages=english&resultLanguage=spanish"
            print(f'Consultando API para: {query_name}')
            resp = requests.get(api_url)
            if resp.status_code == 200:
                try:
                    data = resp.json()
                    # Procesar ascensiones
                    ascensiones = {}
                    costs = data.get('costs', {})
                    for asc_key, mats in costs.items():
                        asc_list = []
                        for mat in mats:
                            # Consultar información del material
                            material_name = mat.get('name', '').replace(' ', '%20')
                            imagen_material = _get_material_image(material_name)
                            asc_list.append({
                                'idMaterial': mat.get('id'),
                                'nombreMaterial': mat.get('name'),
                                'cantidadMaterial': mat.get('count'),
                                'imagenMaterial': imagen_material
                            })
                        ascensiones[asc_key] = asc_list
                except Exception as ex:
                    print(f'Error parseando JSON para {query_name}:', ex)
                    continue
                # Procesar talentos
                talentos_api_url = f"https://genshin-db-api.vercel.app/api/talents?query={query_name}&queryLanguages=english&resultLanguage=spanish"
                print(f'Consultando talentos para: {query_name}')
                resp_talentos = requests.get(talentos_api_url)
                if resp_talentos.status_code == 200:
                    try:
                        talentos_data = resp_talentos.json()
                        talentos = {}
                        costs_talentos = talentos_data.get('costs', {})
                        for lvl, materials in costs_talentos.items():
                            talentos[lvl] = []
                            for mat in materials:
                                # Consultar información del material
                                material_name = mat.get('name', '').replace(' ', '%20')
                                imagen_material = _get_material_image(material_name)
                                talentos[lvl].append({
                                    'idMaterial': mat.get('id'),
                                    'nombreMaterial': mat.get('name'),
                                    'cantidadMaterial': mat.get('count'),
                                    'imagenMaterial': imagen_material
                                })
                    except Exception as ex:
                        print(f'Error parseando JSON para talentos: {ex}')
                    character = {
                        'idPersonaje': data.get('id'),
                        'nombrePersonaje': data.get('name'),
                        'elemento': data.get('element'),
                        'rareza': int(data.get('rarity')),
                        'urlImagen': data.get('images', {}).get('nameicon'),
                        'ascensiones': ascensiones,
                        'talentos': talentos
                    }
                    db = SessionLocal()
                    personaje_schema = Personaje(**character)
                    try:
                        crear_personaje(personaje_schema, db)
                        print(f'Personaje guardado en la base de datos: {character}')
                    except Exception as db_ex:
                        db.rollback()
                        print(f'Error guardando en base de datos: {db_ex}')
                    finally:
                        db.close()
                    characters.append(character)
                    print(f'Personaje recogido: {character}')
            else:
                print(f'Error en API {query_name}: {resp.status_code}')
        driver.quit()
        print(f'Total personajes recogidos: {len(characters)}')
        return characters

    except Exception as e:
        driver.quit()
        print('Error en scraping:', e)
        raise HTTPException(status_code=500, detail=str(e))

def _get_material_image(material_name: str) -> str:
    """Fetches the image URL of a material from the API."""
    material_api_url = f"https://genshin-db-api.vercel.app/api/materials?query={material_name}&queryLanguages=spanish&resultLanguage=spanish"
    material_resp = requests.get(material_api_url)
    if material_resp.status_code == 200:
        try:
            material_data = material_resp.json()
            return material_data.get('images', {}).get('nameicon', '')
        except Exception as mat_ex:
            print(f'Error parseando material {material_name}:', mat_ex)
    return ''

