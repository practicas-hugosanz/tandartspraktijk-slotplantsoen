# Tandartspraktijk Slotplantsoen · web renovada

Rediseño de **praktijkslotplantsoen.nl** (clínica dental en Meppel, Países Bajos).
Todo el contenido está en neerlandés. HTML + CSS + JS puro, sin WordPress, jQuery
ni plugins: la página carga en una fracción del peso de la antigua.

**Estética:** la de su Instagram y su logo — azul marino profundo `#1b2134`, dorado
champán `#c8b992` (el color del logo), titulares en serif *Playfair Display* con la
palabra clave en cursiva dorada, y *Work Sans* (la fuente que ya usaba la web antigua)
para el texto. Fotos reales del equipo y de la fachada; iconos de tratamientos tomados
de la web original y recoloreados en dorado.

---

## Cómo verla en local

Las URLs son "limpias" (`/behandelingen/bleken/`), así que hace falta un servidor:

```bash
python -m http.server 8000
```

y abrir http://localhost:8000. (En el panel de Claude existe la config `slotplantsoen`.)

## Cómo editar

Todo el HTML se **genera** con `_build/build.py`. No edites los `index.html` a mano:

- Textos de los 10 tratamientos y el equipo → `_build/content.py`
- Plantillas, home, resto de páginas, SEO, formularios → `_build/build.py`
- Estilos → `assets/css/style.css` · Interacción → `assets/js/main.js`

Después de cualquier cambio:

```bash
python -I _build/build.py
```

`_build/assets.py` convierte las fotos originales a WebP, crea favicons, logos y la
imagen para redes (`og-slotplantsoen.jpg`). Solo hace falta si cambian las fotos.

---

## SEO — lo que lleva

- **Mismas URLs que la web antigua** (`/behandelingen/implantaten/`, `/homepage/ons-team/`,
  `/cbct-rontgen/`…), así no se pierde el posicionamiento ganado. Las que desaparecen
  (`/invisalign/`, `/intake-gebitsprothese`, `/homepage/`) redirigen con 301 en `.htaccess`
  y además tienen una página de redirección por si el hosting no usa Apache.
- Title y meta description únicos por página, orientados a búsquedas locales
  ("tandarts Meppel", "implantaten Meppel", "Invisalign Meppel", "spoed tandarts Meppel"…).
- Un solo `<h1>` por página, migas de pan, enlazado interno entre tratamientos.
- **Datos estructurados (JSON-LD):** `Dentist` con dirección, coordenadas, horario,
  teléfono, servicios, zona (Meppel, Nijeveen, Havelte, Staphorst…), Instagram y Google
  Maps; `MedicalWebPage` + `FAQPage` + `BreadcrumbList` en cada tratamiento; `Person` para
  los 14 miembros del equipo; `JobPosting` para la vacante.
- `sitemap.xml`, `robots.txt`, canonical, hreflang `nl-NL`, Open Graph con imagen propia.
- Rendimiento: imágenes WebP con `width`/`height`, lazy loading, fuentes locales
  precargadas, sin librerías externas. Bueno para Core Web Vitals.
- Privacidad (AVG/GDPR): sin cookies de seguimiento; Google Maps solo se carga al pulsar
  "Kaart laden". Por eso **no hace falta banner de cookies**.

## Después de publicar

1. Subir los archivos al hosting (incluido `.htaccess`) y comprobar que la web carga en
   `https://praktijkslotplantsoen.nl/`.
2. En **Google Search Console**: enviar `sitemap.xml` y pedir la indexación de la home.
3. En **Google Business Profile**: poner la web, y revisar que el horario coincide
   (Google muestra "abre a las 8:15" el miércoles; la web dice 8:00).

---

## Vídeo de fondo del hero

El hero de la home admite un vídeo de fondo (silenciado, en bucle, con botón de pausa y
pausado automáticamente si el visitante pide menos movimiento). Mientras no haya vídeo se
muestra `assets/img/hero-poster.webp` (la fachada).

Para activarlo, convierte el vídeo de la clínica y vuelve a generar la web:

```bash
mkdir -p assets/video
ffmpeg -i ORIGINAL.mp4 -an -t 20 -vf "scale=1920:-2,fps=25" -c:v libx264 -crf 26 -preset slow -pix_fmt yuv420p -movflags +faststart assets/video/hero.mp4
ffmpeg -i ORIGINAL.mp4 -an -t 20 -vf "scale=1920:-2,fps=25" -c:v libvpx-vp9 -crf 36 -b:v 0 assets/video/hero.webm
python -I _build/build.py
```

Lo ideal: horizontal, 10 a 20 segundos, sin texto encima, planos tranquilos de la praktijk
(sala, equipo trabajando, detalles). Que pese menos de 3 MB.

## Pendiente de confirmar con la clínica

1. **Formularios.** Ahora mismo validan en el navegador y abren el correo del paciente
   con el mensaje ya escrito para `info@praktijkslotplantsoen.nl` (funciona sin servidor).
   Para que se envíen directamente, añade `data-endpoint="URL"` al `<form>` en
   `build.py` (función `form_wrap`) con un PHP propio o un servicio tipo Formspree.
2. **BSN:** la web antigua lo pedía en el formulario de inscripción. Se ha quitado a
   propósito (dato sensible por correo); se anota en la primera visita. Confirmar.
3. **Número de urgencias 0900-8602**: copiado de la web antigua, no he podido
   verificarlo. Comprobar que sigue siendo el de la guardia de la zona.
4. **Opiniones:** se muestra la nota real de Google (4,3 · 29 reseñas) con enlace a
   Maps. Cuando cambie, actualizar en `build.py` (busca `4,3`). No se ha añadido
   `aggregateRating` al schema porque Google no lo admite para reseñas propias.
5. **Textos nuevos:** las preguntas frecuentes y algunas explicaciones (p. ej. sobre
   amalgama, blanqueamiento o Invisalign) son contenido general de odontología escrito
   para SEO. Que la clínica los revise antes de publicar.
6. **Privacyverklaring:** texto base conforme a AVG/WGBO; revisarlo con la clínica.
7. Logos de **KNMT / "de lieve tandarts"** estaban entre los archivos de la web antigua
   pero no se han puesto: añadirlos solo si la clínica confirma la afiliación.

## Estructura

```
index.html                      Home
behandelingen/                  Índice + 10 tratamientos (URLs originales)
homepage/                       Over de praktijk, team, spoed, tarieven, verzekering, huisregels
afspraak-maken/  inschrijven-als-nieuwe-patient/  contact/
cbct-rontgen/  doorverwijzing-cbct-scan-voor-behandelaars/
kinderen-en-de-tandarts/  angst-voor-de-tandarts/  vacatures/  privacyverklaring/
404.html  sitemap.xml  robots.txt  site.webmanifest  .htaccess  favicon.ico
assets/  css · js · fonts (Playfair Display, Work Sans — OFL) · img
_build/  build.py · content.py · assets.py   (no se publica: bloqueado en .htaccess)
```
