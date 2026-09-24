"""Genera los PDF de la entrega inicial con Chromium/Chrome/Edge en modo headless.

- Documento:    docs/propuesta_proyecto.md             -> docs/entrega_inicial/Entrega_Inicial_Grupo12.pdf
- Presentación: docs/entrega_inicial/presentacion.html -> docs/entrega_inicial/Presentacion_Entrega_Inicial_Grupo12.pdf

La portada del documento se arma con el encabezado del .md (lo que está antes
del primer título "## "): el título "# ...", "Grupo N", la fecha
("24 de septiembre de 2026") y la lista de integrantes.

Uso:
    python src/generar_pdf.py                 # ambos
    python src/generar_pdf.py documento
    python src/generar_pdf.py presentacion
    CHROME="/ruta/al/navegador" python src/generar_pdf.py   # si no encuentra el navegador

Requisitos: `pip install markdown` y Google Chrome, Chromium o Microsoft Edge instalado.
Alternativa sin script: abrir el HTML en el navegador e imprimir a PDF (sin encabezados).
"""

from __future__ import annotations

import argparse
import base64
import glob
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
DIR_ENTREGA = RAIZ / "docs" / "entrega_inicial"

DOCUMENTO_MD = RAIZ / "docs" / "propuesta_proyecto.md"
DOCUMENTO_PDF = DIR_ENTREGA / "Entrega_Inicial_Grupo12.pdf"
PRESENTACION_HTML = DIR_ENTREGA / "presentacion.html"
PRESENTACION_PDF = DIR_ENTREGA / "Presentacion_Entrega_Inicial_Grupo12.pdf"

PLANTILLA = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>{titulo}</title>
<link rel="stylesheet" href="assets/documento.css">
</head>
<body>
{cuerpo}
</body>
</html>
"""


PORTADA = """<section class="portada">
<img class="logo" src="../img/logo_ugr.png" alt="Universidad del Gran Rosario">
<div class="institucion"><strong>Universidad del Gran Rosario</strong><br>Aprendizaje Automático · Trabajo Práctico Grupal 2026, 2.º cuatrimestre</div>
<div class="centro">
<p class="etiqueta">Entrega inicial</p>
<h1>{titulo}</h1>
<p class="bajada">Contexto y planteo del problema, descripción del dataset, acceso a los datos originales y propuesta de limpieza y preprocesamiento.</p>
</div>
<div class="equipo">
<div>
<p class="grupo">{grupo}</p>
<h2>Integrantes</h2>
<ul>
{integrantes}
</ul>
</div>
<div>
<h2>Fecha de entrega</h2>
<p>{fecha}</p>
<h2 style="margin-top: 5mm">Datos</h2>
<p>Desembarques de pesca marítima por puerto, flota y especie. Ministerio de Agricultura, Ganadería y Pesca (datos abiertos).</p>
</div>
</div>
</section>
"""


def separar_encabezado(texto: str) -> tuple[dict, str]:
    """Separa el encabezado del .md (antes del primer "## ") y extrae los datos de la portada."""
    lineas = texto.splitlines()
    corte = next((i for i, linea in enumerate(lineas) if linea.startswith("## ")), 0)
    encabezado = "\n".join(lineas[:corte])

    def limpiar(s: str) -> str:
        return re.sub(r"[*_`]", "", s).strip()

    titulo = next((limpiar(linea[2:]) for linea in lineas[:corte] if linea.startswith("# ")), "")
    integrantes = [limpiar(linea[2:]) for linea in lineas[:corte] if re.match(r"[-*] ", linea)]
    grupo = re.search(r"Grupo\s+\d+", encabezado)
    fecha = re.search(r"\d{1,2} de [a-záéíóú]+ de \d{4}", encabezado)
    datos = {
        "titulo": titulo,
        "integrantes": integrantes,
        "grupo": grupo.group(0) if grupo else "",
        "fecha": fecha.group(0) if fecha else "",
    }
    return datos, "\n".join(lineas[corte:])


def encontrar_navegador() -> str:
    if os.environ.get("CHROME"):
        return os.environ["CHROME"]
    for nombre in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome",
                   "msedge", "microsoft-edge"):
        ruta = shutil.which(nombre)
        if ruta:
            return ruta
    candidatos = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        *sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome"), reverse=True),
    ]
    for ruta in candidatos:
        if Path(ruta).exists():
            return ruta
    sys.exit("No se encontró Chrome/Chromium/Edge. Indicá la ruta con la variable de entorno CHROME.")


def _css_con_fuentes_embebidas(ruta_css: Path) -> str:
    """Devuelve el CSS con las fuentes como data URI (evita bloqueos de file:// en Chrome)."""
    css = ruta_css.read_text(encoding="utf-8")

    def reemplazar(m: re.Match) -> str:
        archivo = (ruta_css.parent / m.group(1)).resolve()
        datos = base64.b64encode(archivo.read_bytes()).decode("ascii")
        return f'url("data:font/woff2;base64,{datos}")'

    return re.sub(r'url\("([^"]+\.woff2)"\)', reemplazar, css)


def _autocontenido(html: str, base: Path) -> str:
    """Reemplaza cada <link rel="stylesheet"> por un <style> con el CSS y las fuentes embebidas."""
    def reemplazar(m: re.Match) -> str:
        return "<style>\n" + _css_con_fuentes_embebidas(base / m.group(1)) + "\n</style>"

    return re.sub(r'<link rel="stylesheet" href="([^"]+)">', reemplazar, html)


def imprimir_pdf(html: str, destino: Path) -> None:
    """Escribe el HTML junto a sus recursos (para que resuelvan las rutas relativas) y lo imprime a PDF."""
    navegador = encontrar_navegador()
    with tempfile.TemporaryDirectory() as perfil:
        fd, ruta_tmp = tempfile.mkstemp(suffix=".html", prefix=".tmp_", dir=DIR_ENTREGA)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(_autocontenido(html, DIR_ENTREGA))
            comando = [
                navegador, "--headless=new", "--disable-gpu", "--no-first-run",
                f"--user-data-dir={perfil}",
                "--no-pdf-header-footer", "--print-to-pdf-no-header",
                "--run-all-compositor-stages-before-draw", "--virtual-time-budget=10000",
                f"--print-to-pdf={destino}",
                Path(ruta_tmp).as_uri(),
            ]
            if hasattr(os, "geteuid") and os.geteuid() == 0:
                comando.insert(1, "--no-sandbox")
            if destino.exists():
                destino.unlink()
            subprocess.run(comando, check=True, capture_output=True, timeout=180)
        finally:
            Path(ruta_tmp).unlink(missing_ok=True)
    if not destino.exists() or destino.stat().st_size == 0:
        sys.exit(f"El navegador no generó {destino}")
    print(f"PDF generado: {destino.relative_to(RAIZ)} ({destino.stat().st_size / 1024:.0f} KB)")


def generar_documento() -> None:
    import markdown

    datos, texto = separar_encabezado(DOCUMENTO_MD.read_text(encoding="utf-8"))
    portada = PORTADA.format(
        titulo=html.escape(datos["titulo"]),
        grupo=html.escape(datos["grupo"]),
        fecha=html.escape(datos["fecha"]),
        integrantes="\n".join(f"<li>{html.escape(n)}</li>" for n in datos["integrantes"]),
    )
    cuerpo = markdown.markdown(texto, extensions=["tables", "attr_list", "md_in_html", "sane_lists"])
    pagina = PLANTILLA.format(titulo=html.escape(f"Entrega inicial · {datos['grupo']} · {datos['titulo']}"),
                              cuerpo=portada + cuerpo)
    imprimir_pdf(pagina, DOCUMENTO_PDF)


def generar_presentacion() -> None:
    imprimir_pdf(PRESENTACION_HTML.read_text(encoding="utf-8"), PRESENTACION_PDF)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("que", nargs="?", choices=["documento", "presentacion", "todo"], default="todo")
    args = parser.parse_args()
    if args.que in ("documento", "todo"):
        generar_documento()
    if args.que in ("presentacion", "todo") and PRESENTACION_HTML.exists():
        generar_presentacion()


if __name__ == "__main__":
    main()
