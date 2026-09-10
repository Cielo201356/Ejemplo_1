# Auditoría de accesibilidad, UX y responsive

**Alcance:** auditoría no destructiva de `index.html`, `styles.css` y `script.js` según WCAG 2.2 AA, UX y diseño responsive.

**Fecha:** 2026-09-07

No se modificaron los archivos auditados. Este informe es el único archivo nuevo.

## 1. Resumen ejecutivo

La página tiene una base sólida: usa HTML semántico, idioma declarado, jerarquía de encabezados coherente, navegación interna, textos alternativos para todas las imágenes, botones reales para la interacción, `defer` para el JavaScript y un foco visible global.

No se encontraron hallazgos críticos ni errores de ejecución durante la prueba en navegador. La línea de tiempo cambia correctamente de panel y mantiene el estado ARIA esperado. Las cuatro imágenes cargaron correctamente.

Se encontraron dos hallazgos altos: falta un mecanismo para saltar el bloque de navegación repetido y hay colores de texto pequeños que no alcanzan con seguridad el contraste AA. También hay mejoras medias: el `tablist` vertical no declara su orientación, los enlaces de navegación no tienen objetivos táctiles robustos, y el viewport extremo de 190 px produce overflow horizontal.

## 2. Hallazgos por severidad

### Críticos

- **Ninguno encontrado.** No hay formularios, autenticación, acciones destructivas ni contenido esencial bloqueado por un error crítico.

### Altos

#### A-01. Falta un enlace para saltar la navegación repetida

- **Criterio relacionado:** WCAG 2.2, 2.4.1 Bypass Blocks, nivel A.
- **Estado:** No cumple.
- **Evidencia:** La página comienza con el header y la navegación, pero no contiene un enlace visible al recibir foco que lleve directamente a `main`.
- **Impacto:** Una persona que navega con teclado o lector de pantalla debe recorrer los enlaces del header en cada carga o navegación interna antes de llegar al contenido.
- **Corrección recomendada:** Añadir un enlace `Saltar al contenido` como primer elemento interactivo del `body`, con `href="#contenido"`, y asignar `id="contenido"` al `main`. Hacerlo visible al recibir foco.

#### A-02. Contraste insuficiente o no demostrado en textos pequeños

- **Criterio relacionado:** WCAG 2.2, 1.4.3 Contrast (Minimum), nivel AA.
- **Estado:** Riesgo de incumplimiento confirmado por los valores definidos en CSS.
- **Evidencia:** `--red: #e84b3c` se usa en textos pequeños como `.eyebrow`, y `#f2c4bd` se usa como texto pequeño sobre `--red-dark: #aa2f28`.
- **Impacto:** Parte del texto secundario puede ser difícil de leer para personas con baja visión o en pantallas con brillo reducido.
- **Corrección recomendada:** Medir con un analizador WCAG y oscurecer `--red` para textos sobre fondos claros. Para el texto de `.stats-section .section-intro`, usar un color claro con una relación mínima de 4.5:1 frente a `#aa2f28`. Mantener `--gold` para títulos grandes solo después de comprobar el tamaño y peso efectivos.

### Medios

#### M-01. El tablist vertical no declara `aria-orientation`

- **Criterio relacionado:** WCAG 2.2, 4.1.2 Name, Role, Value; patrón WAI-ARIA Tabs.
- **Estado:** Mejora recomendada.
- **Evidencia:** El contenedor tiene `role="tablist"`, pero no `aria-orientation="vertical"`; visualmente `.timeline-tabs` usa `flex-direction: column`.
- **Impacto:** Algunas tecnologías de asistencia pueden interpretar el componente como una lista horizontal, aunque el script implemente flechas arriba/abajo.
- **Corrección recomendada:** Añadir `aria-orientation="vertical"`. Como mejora adicional, documentar o implementar también `Home` y `End` para recorrer el conjunto de pestañas.

#### M-02. Objetivos táctiles pequeños en la navegación principal

- **Criterio relacionado:** WCAG 2.2, 2.5.8 Target Size (Minimum), nivel AA.
- **Estado:** Riesgo de incumplimiento.
- **Evidencia:** Los enlaces `.site-nav a` solo reciben el tamaño derivado de una fuente de `0.73rem`, sin `padding`, `min-height` ni una caja mínima. En móvil el bloque reduce aún más la fuente a `0.62rem`.
- **Impacto:** En pantallas táctiles resulta más difícil activar `Perfil`, `Trayectoria`, `Cifras` y `Galería sin tocar un enlace vecino.
- **Corrección recomendada:** Dar a cada enlace un área de interacción aproximada de 24 x 24 CSS px como mínimo AA y preferiblemente 44 x 44 px, mediante `min-height`, `padding` y alineación flex; comprobar que el espaciado entre objetivos siga siendo suficiente.

#### M-03. Overflow horizontal confirmado a 190 px

- **Criterio relacionado:** WCAG 2.2, 1.4.10 Reflow, nivel AA; además de usabilidad responsive extrema.
- **Estado:** No cumple para ese ancho de prueba.
- **Evidencia:** En navegador, a viewport de 190 px se obtuvo `document.documentElement.scrollWidth = 245` y `clientWidth = 175`. A 320, 768 y 1280 px no se observó overflow horizontal.
- **Causa probable:** El branding combina un bloque fijo de 42 px, separación, texto con mayúsculas y letter-spacing; además, el `h1` conserva `font-size: 4.2rem` en el breakpoint de hasta 430 px.
- **Corrección recomendada:** Probar un breakpoint adicional para anchos menores de 320 px: reducir el tamaño del branding y del `h1`, permitir cortes controlados con `overflow-wrap: anywhere` donde sea necesario y revisar el ancho mínimo de los componentes. No ocultar el overflow como solución única.

#### M-04. Los destinos de ancla pueden quedar ocultos por el header sticky

- **Criterio relacionado:** WCAG 2.2, 2.4.11 Focus Not Obscured (Minimum), nivel AA; UX de navegación interna.
- **Estado:** Riesgo contextual.
- **Evidencia:** El header usa `position: sticky` y `top: 0`, pero no se define `scroll-margin-top` para las secciones enlazadas.
- **Impacto:** Al activar un enlace interno o navegar por teclado hacia una sección, su título podría quedar parcialmente bajo el header en ciertos tamaños o alturas.
- **Corrección recomendada:** Añadir `scroll-margin-top` a las secciones con ancla, con un valor que cubra la altura real del header sticky en escritorio y móvil.

### Bajos

#### B-01. No hay preferencia para reducir movimiento

- **Criterio relacionado:** WCAG 2.2, 2.3.3 Animation from Interactions, nivel AAA; buena práctica UX AA.
- **Estado:** Mejora recomendada, no una falla AA automática.
- **Evidencia:** Hay transiciones y la animación `reveal` en CSS, pero no existe `@media (prefers-reduced-motion: reduce)`.
- **Corrección recomendada:** Desactivar o reducir `transition`, `transform` y `animation` cuando el usuario solicite menos movimiento.

#### B-02. Enlace externo sin aviso textual de nueva pestaña

- **Criterio relacionado:** WCAG 2.2, 3.2.5 Change on Request y consistencia UX.
- **Estado:** Mejora recomendada.
- **Evidencia:** El enlace de Wikimedia usa `target="_blank"` y `rel="noopener noreferrer"`, pero el texto solo comunica la fuente, no que se abrirá otra pestaña.
- **Corrección recomendada:** Añadir texto visible o una etiqueta accesible como `Se abre en una pestaña nueva`, sin depender únicamente del símbolo `↗`.

#### B-03. Las estadísticas podrían tener una semántica de datos más precisa

- **Criterio relacionado:** HTML semántico y experiencia con lectores de pantalla.
- **Estado:** Mejora, no incumplimiento AA directo.
- **Evidencia:** Las cifras usan `div`, `strong` y `span`, sin relación explícita de término y valor.
- **Corrección recomendada:** Considerar un `dl` con `dt` para la métrica y `dd` para el valor. Esto mejora la lectura estructurada sin cambiar el diseño visual.

## 3. Evidencia concreta y criterios que cumplen

### Estructura, idioma y encabezados: cumple

- `lang="es"`, `meta viewport`, descripción y título están presentes en [index.html](index.html#L1-L9).
- Existen `header`, `nav`, `main` y `footer` en [index.html](index.html#L12-L25) y [index.html](index.html#L123-L127).
- Hay un único `h1` y los bloques principales usan `h2`; los paneles de trayectoria usan `h3`, como se observa en [index.html](index.html#L29-L67) y [index.html](index.html#L80-L103).
- Las secciones usan `aria-labelledby` con títulos existentes, por ejemplo en [index.html](index.html#L49-L62) y [index.html](index.html#L101-L113).

### Nombres accesibles, enlaces y controles: cumple con una mejora ARIA pendiente

- La navegación tiene nombre accesible mediante `aria-label` y los enlaces tienen texto visible en [index.html](index.html#L16-L25).
- La línea de tiempo usa botones reales, `role="tab"`, `aria-selected` y `aria-controls` en [index.html](index.html#L71-L77).
- Cada panel referencia su pestaña con `aria-labelledby` y los paneles inactivos usan `hidden` en [index.html](index.html#L79-L95).
- El script actualiza selección, foco secuencial y visibilidad de paneles en [script.js](script.js#L6-L23).
- La navegación por `ArrowUp` y `ArrowDown` está implementada en [script.js](script.js#L26-L36). Falta declarar la orientación vertical, documentado como M-01.

### Imágenes y textos alternativos: cumple

- Las cuatro imágenes tienen `alt`, dimensiones explícitas y las tres de galería usan `loading="lazy"` en [index.html](index.html#L39-L43) y [index.html](index.html#L113-L119).
- La prueba de navegador confirmó que las cuatro imágenes terminaron con `complete: true` y `naturalWidth` mayor que cero.
- La galería ofrece un enlace a la categoría fuente de Wikimedia en [index.html](index.html#L115-L119).

### Foco y teclado: cumple parcialmente

- Existe un estilo global `:focus-visible` con contorno de 3 px y offset en [styles.css](styles.css#L93-L94).
- El componente de pestañas respondió al click, actualizó `aria-selected` y ocultó el panel anterior durante la prueba en navegador.
- Falta un enlace de salto al contenido, por lo que A-01 sigue abierto.
- Los enlaces de navegación no tienen un área táctil explícita, por lo que M-02 sigue abierto.

### Responsive y overflow: resultado de pruebas

- **190 px:** falla por overflow horizontal medible: `scrollWidth 245`, `clientWidth 175`.
- **320 px:** sin overflow horizontal detectado: `scrollWidth 305`, `clientWidth 305`.
- **768 px:** sin overflow horizontal detectado: `scrollWidth 753`, `clientWidth 753`.
- **1280 px:** sin overflow horizontal detectado: `scrollWidth 1265`, `clientWidth 1265`.
- Los breakpoints principales están definidos en [styles.css](styles.css#L95-L96). El layout pasa a una columna a 760 px y la galería a una columna a 430 px.

### JavaScript: sin error observable

- El script está cargado con `defer` en [index.html](index.html#L8-L9).
- La página se cargó en navegador y la interacción de la línea de tiempo funcionó, lo que confirma que el JavaScript fue interpretado y ejecutado sin un error fatal.
- La validación previa del proyecto con `node --check script.js` había sido correcta. En la sesión de auditoría, `node` no estaba disponible en el `PATH`, por lo que no se pudo repetir ese comando desde la terminal actual; no se modificó `script.js`.

## 4. Recomendaciones de corrección por prioridad

1. Añadir skip link y destino `main` para resolver A-01.
2. Medir y corregir los pares de contraste de textos pequeños para resolver A-02.
3. Añadir `aria-orientation="vertical"` y completar la navegación esperada del tablist.
4. Aumentar el área táctil de los enlaces del header.
5. Añadir un breakpoint para 190 px y comprobar branding, `h1` y componentes con el zoom del navegador.
6. Añadir `scroll-margin-top` en las secciones enlazadas.
7. Incorporar `prefers-reduced-motion` y el aviso de nueva pestaña.
8. Evaluar migrar estadísticas a `dl`, `dt` y `dd`.

## 5. Pruebas que deberían repetirse después de corregir

- Ejecutar axe DevTools o Lighthouse en WCAG AA y revisar todos los ratios de contraste con los colores finales.
- Repetir navegación completa con teclado: `Tab`, `Shift+Tab`, `Enter`, `Space`, `ArrowUp`, `ArrowDown`, `Home` y `End`.
- Comprobar que el foco nunca quede bajo el header sticky al activar anclas.
- Probar viewport de 190, 320, 768 y 1280 px, además de zoom al 200 % y 400 %, verificando `scrollWidth <= clientWidth` cuando aplique.
- Probar en un dispositivo táctil o emulación que los enlaces y pestañas sean fáciles de activar sin solaparse.
- Activar `prefers-reduced-motion: reduce` y confirmar que no haya animaciones innecesarias.
- Ejecutar `node --check script.js` con Node.js disponible y revisar la consola del navegador sin errores.
- Confirmar carga de imágenes, textos `alt`, enlaces externos y estados `hidden` de todos los paneles.
3