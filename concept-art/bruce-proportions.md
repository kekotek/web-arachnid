# Proporciones maestras de Bruce

Estas son las medidas de diseño de Bruce: un joven de 18 años, delgado, de **1,80 m** de altura total. Fijan las proporciones que debe conservar el cuerpo en todas las vistas y skins.

Las longitudes de las extremidades se miden entre centros de articulación. La longitud de la mano termina en la punta del dedo medio. Los anchos corresponden al cuerpo; la ropa y los guantes pueden añadir volumen exterior.

## Longitudes y medidas principales

| Parte | Medida | Cómo medir |
| --- | --- | --- |
| Altura total | 180 cm | Desde las suelas hasta la parte superior de la cabeza de referencia. |
| Cabeza | 26 cm | Desde la parte superior de la cabeza de referencia hasta el mentón. |
| Cuello | 8 cm | Desde el mentón hasta la línea de articulación de los hombros. |
| Torso | 51 cm | Desde la línea de articulación de los hombros hasta la de las caderas. |
| Brazo superior | 32 cm | Desde el centro del hombro hasta el centro del codo. |
| Antebrazo | 26 cm | Desde el centro del codo hasta el centro de la muñeca. |
| Mano | 18 cm | Desde la muñeca hasta la punta del dedo medio. |
| Brazo completo | 76 cm | Hombro a punta del dedo medio: 32 + 26 + 18. |
| Muslo | 46 cm | Desde el centro de la cadera hasta el centro de la rodilla. |
| Rodilla a tobillo | 41 cm | Desde el centro de la rodilla hasta el centro del tobillo. |
| Tobillo al suelo | 8 cm | Distancia vertical hasta las suelas; incluye pie y calzado. |
| Pierna hasta el suelo | 95 cm | Desde la articulación de la cadera hasta el suelo. |
| Largo del pie | 27 cm | Desde el talón hasta el dedo más largo; no se suma como altura. |
| Ancho exterior de hombros | 42 cm | Ancho frontal del cuerpo; distinto de la separación entre articulaciones. |
| Separación entre articulaciones de hombros | 36 cm | Distancia entre los dos centros de hombro. |
| Envergadura | 188 cm | Con ambos brazos extendidos horizontalmente: 36 + 2 × 76. |

La altura se cierra exactamente: **26 + 8 + 51 + 46 + 41 + 8 = 180 cm**. El largo horizontal del pie no se suma a esta altura. La cabeza ocupa aproximadamente una séptima parte de la altura total.

## Alturas en reposo, con brazos junto al cuerpo

| Punto | Altura |
| --- | --- |
| Parte superior de la cabeza | 180 cm |
| Mentón | 154 cm |
| Hombros | 146 cm |
| Codos | 114 cm |
| Cintura | 106 cm |
| Articulación de las caderas | 95 cm |
| Entrepierna | 90 cm |
| Muñecas | 88 cm |
| Puntas de los dedos | 70 cm |
| Rodillas | 49 cm |
| Tobillos | 8 cm |
| Suelo | 0 cm |

## Pose A obligatoria para modelado: brazos a 45°

Los brazos rectos se separan 45° del torso vertical en el plano frontal. Hombro, codo, muñeca y mano conservan sus longitudes. En los perfiles, la misma pose se ve con escorzo.

| Punto | Altura en pose A |
| --- | --- |
| Hombros | 146 cm |
| Codos | 123,37 cm |
| Muñecas | 104,99 cm |
| Puntas de los dedos | 92,26 cm |

Altura del punto = 146 cm − longitud acumulada del brazo × cos(45°). Las cotas de 114, 88 y 70 cm corresponden a brazos verticales en reposo; no se usan para la pose A.

La separación entre puntas de los dedos en pose A es 143,48 cm. La envergadura de 188 cm corresponde a brazos horizontales.


## Anchos y profundidades

| Parte | Ancho | Profundidad |
| --- | --- | --- |
| Cabeza, sin volumen lateral del pelo | 17,5 cm | 21 cm |
| Silueta lateral máxima del pelo | 23 cm | — |
| Cuello | 10 cm | — |
| Pecho | 32 cm | 22 cm |
| Cintura | 26 cm | — |
| Caderas | 30 cm | 20 cm |
| Mano | 8,5 cm | — |
| Brazo superior | 6 cm | — |
| Antebrazo | 5 cm | — |
| Muslo | 11 cm | — |
| Rodilla a tobillo | 8,5 cm | — |
| Pie | 10 cm | — |

## Reglas para mantener la coherencia

- Las longitudes de brazos y piernas se miden entre centros de articulación; la mano, desde la muñeca hasta la punta del dedo medio.
- La cabeza se mide verticalmente desde el límite superior de la referencia hasta el mentón. El eje completo termina en las suelas.
- Izquierda y derecha comparten las mismas longitudes. El bolso permanece en la cadera izquierda.
- Los trajes y los guantes cambian el volumen exterior, pero no alargan huesos ni cambian la posición de las articulaciones.
- En una pose flexionada o en perspectiva cambia la altura aparente; las longitudes de cada segmento se conservan.
- Las vistas de control usan cámara ortográfica, escala común y línea de suelo compartida.
- Las medidas del maniquí gobiernan el cuerpo; las referencias de modelado 3D gobiernan el rostro, el peinado, la ropa y la identidad visual.
- El arte conceptual de control y las referencias de modelado utilizan pose A, con ambos brazos rectos a 45 grados del torso vertical en el plano frontal. Los perfiles muestran la misma pose con escorzo; no girar los brazos hacia delante. Las alturas de codos, muñecas y dedos se derivan de estas longitudes mediante trigonometría.

- La fuente única de medidas es [bruce-proportions.json](bruce-proportions.json). Si cambia una medida, se debe regenerar la ficha y comprobar que la suma de alturas sigue siendo 180 cm.
- El maniquí fija medidas objetivo. Las ilustraciones existentes se usan para la identidad visual; deben compararse con estas cotas al revisar sus proporciones.
- Para obtener vistas exactamente iguales del personaje, usar un único modelo 3D con estas dimensiones y girar la cámara.

## Lámina de construcción

[Abrir la lámina de proporciones](assets/characters/bruce/body-reference/bruce-proportions-180cm.svg).
