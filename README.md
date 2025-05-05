# FastAPI + PostgreSQL API

Este proyecto contiene una API REST construida con FastAPI y PostgreSQL, configurada para ejecutarse en Docker. 
Incluye autenticación con JWT y manejo de sesiones con cookies.

# 🧱 Estructura de la Base de Datos
## Tablas principales:
**Usuario**: Usuarios registrados.

**Personaje**: Personajes disponibles.

**UsuarioPersonaje**: Relación N:M entre usuarios y personajes, con información adicional como arma y artefacto.

**Equipo**: Información de equipos, con una clave única (canonicalKey) y detalles en formato JSON.

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
  "nombrePersonaje": "Aether"
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
  "idUsuario": 1,
  "idPersonaje": 2,
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
  "canonicalKey": "equipo_001",
  "detalles": {
    "personajes": [1, 2, 3],
    "sinergia": "Reacción elemental"
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
  "patch": "461",
  "listaPersonajes": {
    "1": "Xiao",
    "2": "Zhongli"
  },
  "listaEquipos": {
    "equipo_001": {
      "descripcion": "Equipo de daño en área"
    }
  }
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
```json
POST /usuarios/
{
  "correo": "ejemplo@correo.com",
  "contrasena": "1234"
}
```

4. Iniciar sesión
```json
POST /login
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