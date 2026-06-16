# PyRobots

PyRobots es una plataforma web para registrar usuarios, crear y administrar robots, armar partidas y simular combates automáticos entre ellos. El proyecto está dividido en un backend en FastAPI/Pony ORM y un frontend en React.

## Estructura del proyecto

- `backEnd/`: API, lógica de juego, persistencia, carga de avatares y tests.
- `frontEnd/`: interfaz web para usuarios, robots, partidas, lobby y simulaciones.

## Requisitos

- Python 3.10 o superior.
- Node.js 16 o superior.
- `pip` y `npm` disponibles en el sistema.

## Levantar el backend

```bash
cd backEnd
pip install -r requirements.txt
uvicorn src.endpoints:app --reload
```

La API usa la configuración de `backEnd/src/config.ini`. Para habilitar tests, cambiar `testing` a `yes`, `1` o `true` dentro de la sección `DATABASE`.

## Levantar el frontend

```bash
cd frontEnd
npm install
npm start
```

También están disponibles `npm test` y `npm run build`.

## Testing

- Backend: `pytest` dentro de `backEnd/`.
- Frontend: `npm test` dentro de `frontEnd/`.

## Notas

- Los avatares de usuarios y robots se guardan en `backEnd/user_avatars/` y `backEnd/robot_avatars/`.
- Si aparece un conflicto al instalar `PyJWT`, revisar si quedó instalado el paquete `jwt` junto con las dependencias.