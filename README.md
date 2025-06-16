# FastAPI + PostgreSQL API

Este proyecto contiene una API REST construida con FastAPI y PostgreSQL, configurada para ejecutarse en Docker. 
Incluye autenticación con JWT y manejo de sesiones con cookies.

# 🧱 Estructura de la Base de Datos
## Tablas principales:
- **Usuario**: Usuarios registrados.
- **Personaje**: Personajes disponibles.
- **UsuarioPersonaje**: Relación N:M entre usuarios y personajes, con información adicional como arma y artefacto.
- **Equipo**: Información de equipos, con una clave única (canonicalKey) y detalles en formato JSON.
- **Abismo**: Información de mejores personajes y equipos por versión de abismo.
- **ObjetoInventario**: Objetos disponibles en el inventario.
- **Inventario**: Inventario de cada usuario, con la cantidad de cada objeto.

## Relaciones
Usuario ⟷ UsuarioPersonaje ⟷ Personaje
Usuario ⟷ Inventario

# 🔐 Autenticación
**POST /login**: Permite a los usuarios iniciar sesión enviando su correo y contraseña.

Usa JWT y guarda el token en una cookie segura (access_token).

Puede proteger rutas usando get_current_user del archivo auth.py.

# 🧪 Endpoints Disponibles

## Usuario
- **POST `/usuarios/`**
  - Crea un nuevo usuario.
  - Body (JSON):
    ```json
    {
      "correo": "usuario@ejemplo.com",
      "contrasena": "secreta123"
    }
    ```
- **DELETE `/usuarios/{idUsuario}`**
  - Elimina un usuario por su ID.

## Autenticación
- **POST `/login`**
  - Inicia sesión con correo y contraseña. Si las credenciales son correctas, se establece una cookie de sesión.
  - Body (JSON):
    ```json
    {
      "correo": "usuario@ejemplo.com",
      "contrasena": "secreta123"
    }
    ```
  - Devuelve: `{ "idUsuario": int, "correo": string }`

## Personaje
- **GET `/personajes/`**
  - Devuelve la lista de todos los personajes disponibles.
  - Devuelve: `Array` de objetos Personaje (idPersonaje, nombrePersonaje, elemento, rareza, urlImagen, ascensiones, talentos)
- **GET `/personajes/{idPersonaje}`**
  - Devuelve un personaje por su ID.
  - Devuelve: Objeto Personaje
- **GET `/personajes/nombre/{nombre}`**
  - Devuelve un personaje por coincidencia de nombre.
  - Devuelve: Objeto Personaje
- **POST `/personajes/`**
  - Crea un nuevo personaje.
  - Body (JSON):
    ```json
    {
      "nombrePersonaje": "Aether",
      "urlImagen": "https://example.com/images/aether.png"
    }
    ```
- **DELETE `/personajes/`**
  - Elimina todos los personajes.

## UsuarioPersonaje
- **GET `/usuario-personaje/usuario/{idUsuario}`**
  - Devuelve todas las relaciones entre un usuario específico y sus personajes.
  - Devuelve: `Array` de objetos UsuarioPersonaje (idUsuario, idPersonaje, arma, artefacto, constelacion, nivel, nivelDeseado, ascension, ascensionDeseada, talentos, talentosDeseados)
- **POST `/usuario-personaje/`**
  - Crea una nueva relación entre un usuario y un personaje.
  - Body (JSON):
    ```json
    {
      "idUsuario": 1,
      "idPersonaje": 2,
      "arma": "Espada mágica",
      "artefacto": "Orbe de fuego",
      "constelacion": 0,
      "nivel": 1,
      "nivelDeseado": 90,
      "ascension": 0,
      "ascensionDeseada": 6,
      "talentos": {"ataque": 1, "habilidad": 1, "ulti": 1},
      "talentosDeseados": {"ataque": 10, "habilidad": 10, "ulti": 10}
    }
    ```
- **PUT `/usuario-personaje/{idUsuario}/{idPersonaje}`**
  - Actualiza la relación entre usuario y personaje.
  - Body (JSON): igual que el POST.
- **DELETE `/usuario-personaje/{idUsuario}/{idPersonaje}`**
  - Elimina una relación específica entre un usuario y un personaje.

## Equipo
- **GET `/equipos/`**
  - Lista todos los equipos registrados.
  - Devuelve: `Array` de objetos Equipo (idEquipo, canonicalKey, detalles)
- **GET `/equipos/{nombre}`**
  - Devuelve un equipo por nombre de personaje principal. Si no existe, lo genera con IA.
  - Devuelve: Objeto Equipo (idEquipo, canonicalKey, detalles)
- **POST `/equipos/`**
  - Crea un nuevo equipo con su configuración detallada.
  - Body (JSON):
    ```json
    {
      "canonicalKey": "bennettxianglingxingqiusucrose",
      "detalles": { }
    }
    ```

## Abismo
- **GET `/abismo/{idAbismo}`**
  - Obtiene un abismo específico por su ID.
  - Devuelve: Objeto Abismo (idAbismo, version, listaPersonajes, listaEquipos)
- **POST `/abismo/`**
  - Crea una nueva entrada de abismo.
  - Body (JSON):
    ```json
    {
      "version": "4.6A",
      "mejoresEquipos": [ ]
    }
    ```

## Inventario
- **GET `/inventario/{idUsuario}`**
  - Devuelve el inventario de un usuario específico, con detalles de cada objeto.
  - Devuelve: `Array` de objetos (idUsuario, idObjetoApi, nombreObjeto, rarezaObjeto, imagenObjeto, cantidadObjeto)
- **GET `/inventario/{idUsuario}/{idObjetoApi}`**
  - Devuelve un objeto específico del inventario de un usuario.
  - Devuelve: Objeto (idUsuario, idObjetoApi, nombreObjeto, rarezaObjeto, imagenObjeto, cantidadObjeto)
- **POST `/inventario/{idUsuario}`**
  - Agrega un objeto al inventario de un usuario.
  - Body (JSON):
    ```json
    {
      "idObjetoApi": 1,
      "cantidadObjeto": 5
    }
    ```
- **PUT `/inventario/{idUsuario}/{idObjetoApi}`**
  - Modifica la cantidad de un objeto en el inventario de un usuario.
  - Body (JSON): igual que el POST.

## ObjetoInventario
- **GET `/objetoinventario/`**
  - Devuelve la lista de todos los objetos disponibles en la base de datos.
  - Devuelve: `Array` de objetos ObjetoInventario (idObjetoApi, nombreObjeto, rarezaObjeto, imagenObjeto)
- **POST `/objetoinventario/`**
  - Crea un nuevo objeto en la base de datos.
  - Body (JSON):
    ```json
    {
      "idObjetoApi": 1,
      "nombreObjeto": "Amatista",
      "rarezaObjeto": 5,
      "imagenObjeto": "https://example.com/images/amatista.png"
    }
    ```

## Endpoints Externos (Genshin API)
- **GET `/genshin/personaje/{nombre}`**
  - Consulta un personaje externo por nombre.
  - Devuelve: Objeto con los datos completos del personaje desde la API externa.
- **GET `/genshin/arma/{nombre}`**
  - Consulta un arma externa por nombre.
  - Devuelve: Objeto con los datos completos del arma desde la API externa.
- **GET `/genshin/artefacto/{nombre}`**
  - Consulta un artefacto externo por nombre.
  - Devuelve: Objeto con los datos completos del artefacto desde la API externa.
- **GET `/genshin/material/{nombre}`**
  - Consulta un material externo por nombre.
  - Devuelve: Objeto con los datos completos del material desde la API externa.

## Scraping (solo para administración y carga de datos)
- **GET `/scrap/items`**
  - Scrapea y almacena objetos desde una web externa.
  - Devuelve: `Array` de objetos (idObjetoApi, nombreObjeto, rarezaObjeto, imagenObjeto)
- **GET `/scrap/characters`**
  - Scrapea y almacena personajes desde una web externa.
  - Devuelve: `Array` de objetos Personaje (idPersonaje, nombrePersonaje, elemento, rareza, urlImagen, ascensiones, talentos)

# 🚀 Cómo usar el proyecto
1. Clonar el repositorio y navegar dentro
```bash
unzip dra-individual-api.zip
cd dra-individual-api
```
2. Levantar el entorno con Docker
```bash
docker-compose up --build
```
Accede a la API en: http://localhost:8000/docs

3. Crear cuenta
POST /usuarios/
```json
{
  "correo": "ejemplo@correo.com",
  "contrasena": "1234"
}
```

4. Iniciar sesión
POST /login
```json
{
  "correo": "ejemplo@correo.com",
  "contrasena": "1234"
}
```