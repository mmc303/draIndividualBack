# FastAPI + PostgreSQL API

Este proyecto contiene una API REST construida con FastAPI y PostgreSQL, configurada para ejecutarse en Docker. 
Incluye autenticación con JWT y manejo de sesiones con cookies.

# 🧱 Estructura de la Base de Datos
## Tablas principales:
**[Usuario](#usuario)**: Usuarios registrados.

**[Personaje](#personaje)**: Personajes disponibles.

**[UsuarioPersonaje](#usuariopersonaje)**: Relación N:M entre usuarios y personajes, con información adicional como arma y artefacto.

**[Equipo](#equipo)**: Información de equipos, con una clave única (canonicalKey) y detalles en formato JSON.

**[Abismo](#abismo)**: Información de mejores personajes y equipos por versión de abismo.

## Relaciones
Usuario ⟷ UsuarioPersonaje ⟷ Personaje

# 🔐 Autenticación
**/login**: Permite a los usuarios iniciar sesión enviando su correo y contraseña.

Usa JWT y guarda el token en una cookie segura (access_token).

Puede proteger rutas usando get_current_user del archivo auth.py.

# 🧪 Endpoints Disponibles
## Usuario
GET `/usuarios/{idUsuario}`

Obtiene un usuario por su ID.

POST `/usuarios/`

Crea un nuevo usuario.

Body (JSON):
```json
{
  "correo": "usuario@ejemplo.com",
  "contrasena": "secreta123"
}
```

DELETE `/usuarios/{idUsuario}`

Elimina un usuario por su ID.

## Autenticación
POST `/login`

Inicia sesión con correo y contraseña. Si las credenciales son correctas, se establece una cookie de sesión.

Body (JSON):
```json
{
  "correo": "usuario@ejemplo.com",
  "contrasena": "secreta123"
}
```

## Personaje
GET `/personajes/`

Devuelve la lista de todos los personajes disponibles.

POST `/personajes/`

Crea un nuevo personaje.

Body (JSON):
```json
{
  "nombrePersonaje": "Aether",
  "elemento": "Anemo",
  "urlImagen": "https://example.com/images/aether.png"
}
```

## UsuarioPersonaje
GET `/usuario-personaje/usuario/{idUsuario}`

Devuelve todas las relaciones entre un usuario específico y sus personajes.

POST `/usuario-personaje/`

Crea una nueva relación entre un usuario y un personaje, incluyendo el arma y el artefacto.

Body (JSON):
```json
{
  "idUsuario": 1,
  "idPersonaje": 2,
  "arma": "Espada de plata",
  "artefacto": "Amuleto antiguo"
}
```

PUT `/usuario-personaje/{idUsuario}/{idPersonaje}`

Actualiza el arma o artefacto de una relación existente.

Body (JSON):
```json
{
  "arma": "Espada mágica",
  "artefacto": "Orbe de fuego"
}
```

DELETE `/usuario-personaje/{idUsuario}/{idPersonaje}`

Elimina una relación específica entre un usuario y un personaje.

## Equipo
GET `/equipos/`

Lista todos los equipos registrados.

POST `/equipos/`

Crea un nuevo equipo con su configuración detallada.

Body (JSON):
```json
{
  "canonicalKey": "BennettXianglingXingqiuSucrose",
  "detalles": {
    "personajes": [
      {
        "personaje": {
          "nombrePersonaje": "Bennett",
          "elemento": "Pyro",
          "urlImagen": "https://example.com/images/bennett.png"
        },
        "arma": "Espada de Favonius",
        "artefacto": "4x Nobleza"
      },
      {
        "personaje": {
          "nombrePersonaje": "Xiangling",
          "elemento": "Pyro",
          "urlImagen": "https://example.com/images/xiangling.png"
        },
        "arma": "La Captura",
        "artefacto": "4x Emblema del Destino"
      },
      {
        "personaje": {
          "nombrePersonaje": "Xingqiu",
          "elemento": "Hydro",
          "urlImagen": "https://example.com/images/xingqiu.png"
        },
        "arma": "Espada de Sacrificio",
        "artefacto": "4x Emblema del Destino"
      },
      {
        "personaje": {
          "nombrePersonaje": "Sucrose",
          "elemento": "Anemo",
          "urlImagen": "https://example.com/images/sucrose.png"
        },
        "arma": "Cuentos de Cazadores de Dragones",
        "artefacto": "4x Sombra Verde Esmeralda"
      }
    ],
    "justificacion": "Equipo Nacional clásico, gran daño y sinergia elemental.",
    "rotacion": "Bennett Q E -> Sucrose E -> Xiangling Q E -> Xingqiu Q E -> Bennett E..."
  }
}
```

GET `/abismo/{idAbismo}`

Obtiene un abismo específico por su ID.

POST `/abismo/`

Crea una nueva entrada de abismo.

Body (JSON):
```json
{
  "version": "4.6A",
  "listaPersonajes": [
    {
      "personaje": {
        "nombrePersonaje": "Furina",
        "elemento": "Hydro",
        "urlImagen": "https://example.com/images/furina.png"
      },
      "usoPersonaje": 92.5
    },
    {
      "personaje": {
        "nombrePersonaje": "Neuvillette",
        "elemento": "Hydro",
        "urlImagen": "https://example.com/images/neuvillette.png"
      },
      "usoPersonaje": 89.7
    }
  ],
  "listaEquipos": [
    {
      "personajes": [
        {
          "nombrePersonaje": "Neuvillette",
          "elemento": "Hydro",
          "urlImagen": "https://example.com/images/neuvillette.png"
        },
        {
          "nombrePersonaje": "Furina",
          "elemento": "Hydro",
          "urlImagen": "https://example.com/images/furina.png"
        },
        {
          "nombrePersonaje": "Kaedehara Kazuha",
          "elemento": "Anemo",
          "urlImagen": "https://example.com/images/kazuha.png"
        },
        {
          "nombrePersonaje": "Baizhu",
          "elemento": "Dendro",
          "urlImagen": "https://example.com/images/baizhu.png"
        }
      ],
      "usoEquipo": 34.0,
      "ratio": "95:5"
    }
  ]
}
```

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

# 🔧 Cómo modificar
Modelos: app/models/models.py

Esquemas (schemas): app/schemas/schemas.py

Rutas (API): app/routers/

Autenticación: app/auth.py

Base de datos: app/database.py

Configuración del servidor: main.py y docker-compose.yml