# Trayectoria CR7

Sitio web estático en español sobre Cristiano Ronaldo. Está construido únicamente con HTML semántico, CSS y JavaScript vanilla, sin frameworks, dependencias ni backend.

## Archivos

- `index.html`: estructura semántica, contenido, navegación, trayectoria, estadísticas y galería.
- `styles.css`: sistema visual responsive, estados de foco, animaciones y composición.
- `script.js`: interacción accesible de la línea de tiempo mediante botones y teclado.

Los nombres `index.ntml` y `stles.css` se interpretaron como errores tipográficos y se corrigieron a `index.html` y `styles.css`, que son los nombres reconocidos por el navegador.

## Ejecutar localmente

Desde esta carpeta, inicia un servidor estático local. Por ejemplo, con Python:

```powershell
python -m http.server 8000
```

Después abre `http://localhost:8000` en el navegador. También puedes abrir `index.html` directamente, aunque el servidor local ofrece una experiencia más consistente.

## Validación realizada

- HTML enlaza correctamente `styles.css` y `script.js`.
- JavaScript validado con `node --check script.js`.
- Se verificó la existencia de los cuatro archivos del proyecto.
- La línea de tiempo usa botones con roles ARIA y navegación con flechas arriba/abajo.
- Las imágenes tienen textos `alt` descriptivos, carga diferida en la galería y proceden de Wikimedia Commons.
- El layout incluye puntos de adaptación para móvil, tableta y escritorio.
