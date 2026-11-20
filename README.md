# Diseño e Impresión 3D en el aula

Manual práctico y secuencial para integrar el diseño y la impresión 3D en colegios e institutos del programa **Código Escuela 4.0 (Andalucía)**: Bambu Lab P1S y AMS, MakerWorld, Bambu Studio, Bambu Handy, Tinkercad y Layerling.

## Estructura

| Archivo | Contenido |
|---|---|
| `index.html` | Portada e índice de contenidos |
| `01-por-que.html` … `08-saber-mas.html` | Un apartado por página, con menú lateral (05 Tinkercad y 06 Layerling por separado) |
| `css/estilo.css`, `js/app.js` | Estilos y comportamiento comunes |
| `img/` | Capturas propias (Layerling, Bambu Studio) y diapositivas del curso del CEP de Granada |
| `src/manual.html` | **Fuente única** del manual |
| `tools/construir_paginas.py` | Genera las páginas a partir de la fuente |
| `soluciones/stl`, `soluciones/scad`, `soluciones/img` | Soluciones descargables (STL binario), su fuente OpenSCAD y una vista previa |
| `tools/soluciones_scad.py`, `tools/generar_stl.ps1`, `tools/stl_binario.py` | Regeneran las soluciones: escribir los `.scad`, convertirlos en STL con OpenSCAD 2021.01 y pasarlos a binario |

## Editar y publicar

1. Editar siempre `src/manual.html`.
2. Regenerar las páginas:

   ```
   python tools/construir_paginas.py
   ```

3. Publicar la carpeta en GitHub Pages.

El progreso de prácticas y retos se guarda en el navegador de cada usuario (`localStorage`); no se envía a ningún servidor.

## Capturas opcionales de Bambu Studio y Lychee

Las prácticas BS-01…BS-05 y LS-01…LS-03 muestran esquemas. Si se añaden capturas con estos nombres, sustituyen automáticamente al esquema:
`img/bs-01.png` … `img/bs-05.png`, `img/ls-01.png` … `img/ls-03.png`.

## Licencia

© Pablo Moraga · Contenidos con licencia [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/deed.es).
Las marcas y capturas de terceros pertenecen a sus titulares (ver «07 · Para saber más → Créditos y licencias»).

Los iconos pixel-art de 16 × 16 se generan con `python tools/iconos16.py` (después, volver a ejecutar `construir_paginas.py`).
