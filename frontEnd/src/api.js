// URL base de la API.
//
// En desarrollo apunta al backend local, así que no hace falta configurar nada.
// Para el build de producción se define REACT_APP_API: Create React App inyecta
// en tiempo de compilación toda variable que empiece con REACT_APP_.
//
//   REACT_APP_API=https://usuario-pyrobots.hf.space npm run build
export const API = process.env.REACT_APP_API || "http://127.0.0.1:8000";
