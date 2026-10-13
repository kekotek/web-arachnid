# Arte conceptual de web-arachnid

Abre [index.html](index.html) en un navegador para explorar la galería. Funciona directamente desde el archivo, sin instalar dependencias ni iniciar un servidor. Incluye búsqueda, filtros por tema y versión, vista ampliada, tamaño real y descarga, comparación de altura de Bruce, ficha de proporciones y lectura de las ideas y ambos README. En la vista ampliada, usa las flechas del teclado para recorrer las imágenes y Esc para cerrar.

## Organización de la carpeta

| Carpeta | Contenido |
| --- | --- |
| [assets/characters/](assets/characters/) | Estudios vigentes de Bruce. |
| [assets/meshy/](assets/meshy/) | Cuatro vistas revisadas y dos guías de construcción. |
| [assets/suits/](assets/suits/) | Skins casera, normal, alienígena, neón, roquera y estilo cómic. |
| [assets/menus/](assets/menus/) | Concepto del menú principal del juego. |
| [assets/equipment/](assets/equipment/) | Guantes y habilidades. |
| [assets/environments/](assets/environments/) | Aster City y sus tres capas. |
| [assets/story/](assets/story/) | Origen y desarrollo de los guantes. |
| [assets/archive/](assets/archive/) | Versiones anteriores, separadas por los mismos temas. |
| [prompts/](prompts/) | Instrucciones de generación; las antiguas están en `prompts/archive/`. |
| [scripts/](scripts/) | Herramientas auxiliares y actualización de los datos de la galería. |

`manifest.json` es el catálogo de las 69 imágenes: 33 vigentes y 36 anteriores (59 PNG y diez guías SVG). `gallery-data.js` se genera desde ese catálogo para que la página funcione también al abrirla como archivo local. Las ideas y ambos README también se incorporan a los datos de la página. Las medidas maestras se guardan en `bruce-proportions.json`. Después de cambiarlas, ejecutar `python3 scripts/build_character_spec.py` para regenerar ficha, ideas, maniquí y prompt, y luego actualizar la galería. Después de cambiar las referencias de Meshy, ejecutar `python3 scripts/build_scale_reference.py` para renovar la guía de altura. Después de cambiar las vistas de los trajes, ejecutar `python3 scripts/build_suit_scale_references.py` para renovar sus seis láminas. Después de cambiar el catálogo o los documentos, ejecutar `python3 scripts/build_gallery_data.py` desde esta carpeta.

Revisión del 12 de octubre de 2026 basada en [ideas.md](../ideas.md). Las imágenes de esta página son las referencias vigentes. Se conserva el arte anterior para comparar la evolución del diseño.

Los nombres de carpetas y archivos están en inglés; los rótulos de la página y los documentos permanecen en español. [file-renames.json](file-renames.json) registra los cambios de rutas.

## Bruce para Meshy: proporciones revisadas

El conjunto `v3` ajusta brazos, manos y la posición de las rodillas hacia las medidas maestras de Bruce, además de mantener la altura total de **1,80 m**. Conserva rostro, pelo castaño, sudadera naranja, jeans azules, zapatillas claras y un único bolso en la cadera izquierda.

| Vista | Archivo vigente |
| --- | --- |
| Frente | [bruce-for-meshy-front-v3.png](assets/meshy/bruce-for-meshy-front-v3.png) |
| Perfil izquierdo, mirando a la derecha | [bruce-for-meshy-left-v3.png](assets/meshy/bruce-for-meshy-left-v3.png) |
| Perfil derecho, mirando a la izquierda | [bruce-for-meshy-right-v3.png](assets/meshy/bruce-for-meshy-right-v3.png) |
| Espalda | [bruce-for-meshy-back-v3.png](assets/meshy/bruce-for-meshy-back-v3.png) |
| Escala y alturas objetivo de articulaciones | [bruce-scale-180cm.svg](assets/meshy/bruce-scale-180cm.svg) |

Las cuatro vistas son PNG con transparencia. La comparación alinea su silueta entre las suelas y la parte superior de la cabeza. Las líneas cian muestran las alturas objetivo de hombros, codos, caderas, muñecas, dedos y rodillas. Estas ilustraciones permiten comparar las proporciones visualmente; las medidas exactas gobiernan el maniquí y el futuro modelo 3D.

Las seis vistas `v2`, incluidos los ángulos alto y bajo, se conservan en `assets/archive/meshy/` y no gobiernan las proporciones actuales. Los scripts de reconstrucción anteriores siguen asociados a imágenes antiguas.

![Bruce de frente revisado](assets/meshy/bruce-for-meshy-front-v3.png)

## Medidas maestras del cuerpo

La [ficha de proporciones](bruce-proportions.md) define las medidas objetivo de Bruce: brazo superior de 32 cm, antebrazo de 26 cm, mano de 18 cm, muslo de 46 cm y rodilla a tobillo de 41 cm. Incluye anchos y alturas de articulaciones desde el suelo. El torso, cuello, cabeza y piernas suman exactamente 180 cm.

[La lámina de construcción](assets/meshy/bruce-proportions-180cm.svg) distingue el maniquí de medidas de la referencia visual. Usar el maniquí para dimensiones y las vistas Meshy para rostro, pelo, ropa e identidad. Las ilustraciones existentes deben comprobarse con estas cotas; para vistas idénticas, generar todas desde un único modelo 3D.

## Láminas de escala de los seis trajes

Cada traje tiene el mismo formato que Bruce: fondo claro, cuatro vistas, suelas alineadas a 0 cm y parte superior de la silueta a 1,80 m. Las líneas cian marcan las alturas objetivo de hombros, codos, caderas, muñecas, dedos y rodillas.

| Traje | Lámina |
| --- | --- |
| Casero | [suit-homemade-scale-180cm.svg](assets/suits/suit-homemade-scale-180cm.svg) |
| Normal | [suit-standard-scale-180cm.svg](assets/suits/suit-standard-scale-180cm.svg) |
| Alienígena | [suit-alien-scale-180cm.svg](assets/suits/suit-alien-scale-180cm.svg) |
| Neón | [suit-neon-scale-180cm.svg](assets/suits/suit-neon-scale-180cm.svg) |
| Roquero | [suit-rocker-scale-180cm.svg](assets/suits/suit-rocker-scale-180cm.svg) |
| Cómic | [suit-comic-scale-180cm.svg](assets/suits/suit-comic-scale-180cm.svg) |

[Ver las seis láminas en la galería](index.html#tema=trajes&buscar=medidas). Los PNG `suit-*-turnaround.png` contienen las cuatro vistas ilustradas que alimentan estas guías. El SVG normaliza la altura de cada silueta y dibuja las cotas desde `bruce-proportions.json`; no modifica las medidas del cuerpo automáticamente. Las cotas son objetivos de construcción para contrastar el dibujo y el modelo 3D.

Las nuevas vistas se generaron con la herramienta integrada. Los prompts y correcciones están en `prompts/suit-*-turnaround*.prompt.txt`. Se conservan las láminas originales de materiales y detalles en `assets/suits/`.

## Personaje, guantes y skins

| Lámina | Archivo vigente | Qué muestra |
| --- | --- | --- |
| Bruce sin guantes | [assets/characters/bruce-without-gloves.png](assets/characters/bruce-without-gloves.png) | Identidad y proporciones unificadas con Meshy, ropa cotidiana, computador y altura total de 1,80 m. |
| Bruce con guantes | [assets/characters/bruce-with-gloves-v2.png](assets/characters/bruce-with-gloves-v2.png) | Ropa cotidiana, hilos de energía y escudo. |
| Guantes | [assets/equipment/gloves-v2.png](assets/equipment/gloves-v2.png) | Diseño independiente, hilos, escudo, núcleo y nanobots formando una manga. |
| Skin casera | [assets/suits/suit-homemade.png](assets/suits/suit-homemade.png) | Primer traje de ropa vieja, costuras, azul, bufanda y cuello de tela. |
| Skin normal | [assets/suits/suit-standard.png](assets/suits/suit-standard.png) | Evolución tecnológica del traje, hilos y formación con nanobots. |
| Skin alienígena | [assets/suits/suit-alien.png](assets/suits/suit-alien.png) | Apariencia alienígena adaptada al héroe, con los mismos guantes. |
| Skin neón | [suit-neon-v4.png](assets/suits/suit-neon-v4.png) | Pecho limpio, azul oscuro y luces cian y magenta en el contorno del traje. |
| Skin roquera | [suit-rocker-v2.png](assets/suits/suit-rocker-v2.png) | Chaqueta de cuero, tachuelas, bufanda y pelo castaño puntiagudo visible sobre la máscara. |
| Skin cómic | [suit-comic-v3.png](assets/suits/suit-comic-v3.png) | Estructura del traje normal con tinta gruesa, sombras negras planas y puntos de impresión pronunciados. |
| Origen | [assets/story/bruce-origin-one-year.png](assets/story/bruce-origin-one-year.png) | Invasión vista desde el taller, un año de desarrollo y guantes terminados. |

Los guantes conservan sus placas claras, articulaciones oscuras y núcleos cian, y destacan con todas las skins. El azul y el contraste del traje casero proceden de las ideas; la bufanda naranja y los detalles violetas de la skin alienígena son propuestas visuales de estas láminas.

![Skin casera](assets/suits/suit-homemade.png)

La skin cómic utiliza el mismo diseño del traje normal: máscara, paneles, azul predominante y zonas oscuras, con tratamiento de tinta y halftone. Sus versiones anteriores se conservan en el archivo. El acabado actual refuerza los contornos, sombras planas, tramas de puntos y líneas de acción.

La skin neón deja el pecho limpio, sin araña ni emblema central. Mantiene el traje oscuro, las luces cian y magenta en hombros, brazos, costados y piernas, y los guantes de Bruce. Las propuestas anteriores se conservan en el archivo.

## Menú principal

[La propuesta del menú](assets/menus/main-menu.png) presenta las tres capas de Aster City, a web-arachnid con su traje normal y las opciones Nueva partida, Continuar, Trajes, Opciones y Salir. La selección usa cian. Es una lámina de interfaz para orientar el diseño del juego.

## Aster City: tres capas verticales

| Lámina | Archivo vigente | Criterio |
| --- | --- | --- |
| Ciudad completa | [assets/environments/aster-city-three-layers.png](assets/environments/aster-city-three-layers.png) | Capas apiladas en vertical: subterránea, intermedia y alienígena. |
| Capa subterránea | [assets/environments/aster-city-under-v2.png](assets/environments/aster-city-under-v2.png) | Barrio pobre con neón bajo un techo de roca y estructuras de soporte. |
| Capa intermedia | [assets/environments/aster-city-rich-v2.png](assets/environments/aster-city-rich-v2.png) | Zona rica, construcciones minimalistas de ladrillo y espacios amplios. |
| Capa alienígena | [assets/environments/aster-city-alien-01-panorama.png](assets/environments/aster-city-alien-01-panorama.png) | Ciudad en el cielo, solo alienígenas, plataformas abiertas y naves. |

![Aster City en tres capas](assets/environments/aster-city-three-layers.png)

## Revisión del material anterior

| Material anterior | Resultado de la revisión |
| --- | --- |
| `assets/characters/bruce-without-gloves.png` | Se actualiza para coincidir con la identidad y las proporciones de Meshy v2; la versión anterior se conserva en el archivo. |
| `assets/archive/characters/bruce-with-gloves.png`, `assets/archive/equipment/gloves.png` | Sustituidos como referencias vigentes por sus versiones v2, que muestran las nuevas habilidades. |
| `assets/archive/suits/first-suit.png` | Su diseño avanzado sirve de base a `assets/suits/suit-standard.png`. El primer traje ahora es `assets/suits/suit-homemade.png`. |
| `assets/archive/environments/aster-city-under-01-panorama.png`, `assets/archive/environments/aster-city-under-02-commercial-street.png`, `assets/archive/environments/aster-city-under-03-rooftops-and-metro.png` | Conservados como exploraciones de ambiente y neón. Su cielo abierto no corresponde a la capa subterránea actual. |
| `assets/archive/environments/aster-city-rich-01-panorama.png`, `assets/archive/environments/aster-city-rich-02-square.png`, `assets/archive/environments/aster-city-rich-03-terraces.png` | Conservados como exploraciones anteriores. La referencia vigente usa arquitectura más simple y ladrillo. |
| `assets/archive/environments/aster-city-connection-panorama.png` | Sustituido como referencia geográfica por la vista de tres capas verticales. |
| `assets/archive/meshy/bruce-for-meshy.png` y las cinco vistas anteriores | Las versiones originales y v2 están archivadas; las cuatro vistas v3 son las referencias actuales. |

## Instrucciones de generación

Se utilizó la herramienta integrada de generación y edición de imágenes. Los prompts completos y las correcciones están guardados en [prompts/](prompts/), con el mismo nombre base que cada lámina. [manifest.json](manifest.json) relaciona archivos, referencias y prompts.

Las láminas de personaje, skins y origen conservan la identidad de Bruce. Las cuatro vistas Meshy v3 son ahora la referencia para revisar las longitudes de brazos y piernas de nuevas ilustraciones. La altura total de Bruce es 1,80 m, desde las suelas hasta la parte superior de la cabeza. Las versiones previas a esta unificación se conservan en `assets/archive/`.

Estas láminas desarrollan visualmente las ideas existentes; los detalles de formas y materiales que todavía no están definidos en `ideas.md` se mantienen como propuestas de diseño.

