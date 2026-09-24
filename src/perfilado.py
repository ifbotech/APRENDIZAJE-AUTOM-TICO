"""Perfilado de los archivos de desembarques de pesca marítima (MAGyP).

Lee uno o más CSV del portal de datos abiertos, genera un reporte Markdown por
archivo en ``reports/`` y las figuras en ``docs/entrega_inicial/assets/fig/``.
Si se pasan varios archivos, el reporte del último incluye una comparación de
categorías contra los anteriores (útil para unificar 2010-2018 con 2019).

Uso:
    python src/perfilado.py data/raw/captura-puerto-flota-2019.csv
    python src/perfilado.py data/raw/<archivo-2010-2018>.csv data/raw/captura-puerto-flota-2019.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
DIR_REPORTES = RAIZ / "reports"
DIR_FIGURAS = RAIZ / "docs" / "entrega_inicial" / "assets" / "fig"
DIR_FUENTES = RAIZ / "docs" / "entrega_inicial" / "assets" / "fonts"

COLUMNAS = [
    "fecha", "flota", "puerto", "provincia", "provincia_id", "departamento",
    "departamento_id", "latitud", "longitud", "categoria", "especie",
    "especie_agrupada", "captura",
]
# Una fila = captura de una especie (dentro de una agrupación), de un tipo de
# flota, desembarcada en un puerto, en un mes.
CLAVE_REGISTRO = ["fecha", "flota", "puerto", "especie", "especie_agrupada"]
CLAVE_SERIE = ["flota", "puerto", "especie", "especie_agrupada"]

# Paleta: azul institucional UGR para la serie, grises neutros para ejes/texto.
AZUL = "#0157a4"
TINTA = "#0b0b0b"
TINTA_2 = "#52514e"
TINTA_MUTED = "#898781"
GRILLA = "#e1e0d9"
EJE = "#c3c2b7"
FONDO = "#ffffff"


# --------------------------------------------------------------------------
# Lectura
# --------------------------------------------------------------------------
def leer_csv(ruta: Path) -> tuple[pd.DataFrame, str, str]:
    """Lee el CSV probando UTF-8 y luego Latin-1 (el portal publica en Latin-1)."""
    crudo = ruta.read_bytes()
    fin_linea = "CRLF (Windows)" if b"\r\n" in crudo[:10_000] else "LF (Unix)"
    for codificacion in ("utf-8-sig", "latin-1"):
        try:
            crudo.decode(codificacion)
        except UnicodeDecodeError:
            continue
        df = pd.read_csv(
            ruta,
            encoding=codificacion,
            # Los códigos tienen ceros a la izquierda ("06", "06357"): van como texto.
            dtype={"provincia_id": str, "departamento_id": str},
        )
        return df, codificacion, fin_linea
    raise ValueError(f"No se pudo decodificar {ruta}")


def preparar(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega columnas auxiliares de fecha (no modifica las originales)."""
    d = df.copy()
    d["_fecha"] = pd.to_datetime(d["fecha"].astype(str).str.slice(0, 7), format="%Y-%m", errors="coerce")
    d["_periodo"] = d["_fecha"].dt.year * 12 + d["_fecha"].dt.month
    return d


# --------------------------------------------------------------------------
# Formato
# --------------------------------------------------------------------------
def num(x: float, dec: int = 0) -> str:
    """Formato numérico en castellano: 41.340 / 2.680,5."""
    if pd.isna(x):
        return "-"
    s = f"{x:,.{dec}f}"
    return s.replace(",", "_").replace(".", ",").replace("_", ".")


def pct(x: float, dec: int = 1) -> str:
    return f"{num(100 * x, dec)} %"


def tabla(filas: list[list], encabezados: list[str], alinear: str | None = None) -> str:
    """Tabla Markdown. `alinear` es un string con 'l'/'r' por columna."""
    alinear = alinear or "l" * len(encabezados)
    sep = ["---:" if a == "r" else "---" for a in alinear]
    lineas = ["| " + " | ".join(encabezados) + " |", "| " + " | ".join(sep) + " |"]
    for f in filas:
        lineas.append("| " + " | ".join(str(v) for v in f) + " |")
    return "\n".join(lineas)


# --------------------------------------------------------------------------
# Chequeos de consistencia de `captura`
# --------------------------------------------------------------------------
def _eta2(y: pd.Series, grupos: pd.Series) -> float:
    """Proporción de la varianza de y explicada por las medias de cada grupo."""
    media = y.mean()
    total = ((y - media) ** 2).sum()
    g = y.groupby(grupos.values)
    return float((g.size() * (g.mean() - media) ** 2).sum() / total)


def _lag1(d: pd.DataFrame, y: pd.Series) -> tuple[float, int]:
    """Correlación entre y(t) e y(t-1) dentro de cada serie, para meses consecutivos."""
    t = d[CLAVE_SERIE + ["_periodo"]].copy()
    t["_y"] = y.values
    t = t.sort_values(CLAVE_SERIE + ["_periodo"])
    grupos = t.groupby(CLAVE_SERIE, sort=False)
    y_prev = grupos["_y"].shift(1)
    consecutivo = (t["_periodo"] - grupos["_periodo"].shift(1)) == 1
    if consecutivo.sum() < 3:
        return float("nan"), int(consecutivo.sum())
    return float(np.corrcoef(t.loc[consecutivo, "_y"], y_prev[consecutivo])[0, 1]), int(consecutivo.sum())


def consistencia(d: pd.DataFrame, n_perm: int = 20, semilla: int = 0) -> dict:
    """Compara la estructura de log10(captura) contra una referencia con capturas permutadas.

    Si los valores de captura estuvieran asignados al azar entre las filas, la
    especie, la flota o el mes anterior no aportarían información. Los valores
    reales se reportan junto a esa referencia (media ± desvío de `n_perm` permutaciones).
    """
    d = d[d["captura"] > 0]
    y = np.log10(d["captura"].astype(float))
    rng = np.random.default_rng(semilla)
    dims = ["especie", "flota", "puerto"]
    real = {k: _eta2(y, d[k]) for k in dims}
    r_real, n_pares = _lag1(d, y)
    perm = {k: [] for k in dims + ["lag1"]}
    for _ in range(n_perm):
        yp = pd.Series(rng.permutation(y.values), index=y.index)
        for k in dims:
            perm[k].append(_eta2(yp, d[k]))
        perm["lag1"].append(_lag1(d, yp)[0])
    ref = {k: (float(np.mean(v)), float(np.std(v))) for k, v in perm.items()}
    medianas = d.groupby("especie")["captura"].agg(["size", "median", "sum"]).sort_values("sum", ascending=False)
    return {"eta2": real, "lag1": r_real, "n_pares": n_pares, "ref": ref, "medianas": medianas, "n_perm": n_perm}


# --------------------------------------------------------------------------
# Figuras
# --------------------------------------------------------------------------
def _estilo_matplotlib():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager

    familia = "DejaVu Sans"
    for ttf in sorted(DIR_FUENTES.glob("Inter-*.ttf")):
        font_manager.fontManager.addfont(str(ttf))
        familia = "Inter"
    plt.rcParams.update({
        "font.family": familia,
        "font.size": 9,
        "axes.edgecolor": EJE,
        "axes.labelcolor": TINTA_2,
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": False,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": GRILLA,
        "grid.linewidth": 0.8,
        "xtick.color": TINTA_MUTED,
        "ytick.color": TINTA_MUTED,
        "xtick.labelcolor": TINTA_2,
        "ytick.labelcolor": TINTA_2,
        "ytick.left": False,
        "figure.facecolor": FONDO,
        "axes.facecolor": FONDO,
        "savefig.facecolor": FONDO,
        "svg.fonttype": "path",
    })
    return plt


MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


def fig_registros_por_mes(d: pd.DataFrame, destino: Path) -> Path | None:
    """Registros por mes. Solo tiene sentido para archivos de un único año."""
    anios = d["_fecha"].dt.year.dropna().unique()
    if len(anios) != 1:
        return None
    plt = _estilo_matplotlib()
    conteo = d.groupby(d["_fecha"].dt.month).size().reindex(range(1, 13))
    fig, ax = plt.subplots(figsize=(6.4, 2.5), dpi=200)
    x = np.arange(12)
    ax.bar(x, conteo.fillna(0).values, width=0.62, color=AZUL, zorder=2)
    ax.set_xticks(x, MESES)
    ax.set_ylim(0, max(conteo.max() * 1.22, 10))
    ax.tick_params(axis="x", length=0)
    ax.set_axisbelow(True)
    # Rótulos selectivos: el máximo, el mínimo y los meses sin datos.
    validos = conteo.dropna()
    for mes in {validos.idxmax(), validos.idxmin()}:
        ax.text(mes - 1, conteo[mes] + conteo.max() * 0.03, num(conteo[mes]), ha="center", va="bottom",
                fontsize=8.5, color=TINTA, fontweight="semibold")
    for mes in conteo[conteo.isna()].index:
        ax.text(mes - 1, conteo.max() * 0.04, "sin\ndatos", ha="center", va="bottom", fontsize=7.5, color=TINTA_MUTED)
    ax.set_ylabel("registros")
    fig.tight_layout()
    fig.savefig(destino, bbox_inches="tight")
    plt.close(fig)
    return destino


def fig_distribucion_captura(d: pd.DataFrame, destino: Path) -> Path:
    plt = _estilo_matplotlib()
    y = np.log10(d.loc[d["captura"] > 0, "captura"].astype(float))
    fig, ax = plt.subplots(figsize=(6.4, 2.6), dpi=200)
    bordes = np.arange(0, np.ceil(y.max() * 4) / 4 + 0.25, 0.25)
    alturas, _, _ = ax.hist(y, bins=bordes, color=AZUL, rwidth=0.86, zorder=2)
    ticks = np.arange(0, int(np.floor(y.max())) + 1)
    ax.set_xticks(ticks, [num(10 ** t) for t in ticks])
    ax.set_xlim(-0.25, bordes[-1] + 0.25)
    ax.tick_params(axis="x", length=0, labelsize=8)
    ax.set_xlabel("captura por registro (kg, escala logarítmica)")
    ax.set_ylabel("registros")
    ax.set_axisbelow(True)
    # Espacio libre sobre las barras para que los rótulos no las tapen.
    tope = alturas.max() * 1.38
    ax.set_ylim(0, tope)
    for valor, texto, desplaz in [(d["captura"].median(), "mediana", -0.08), (d["captura"].mean(), "media", 0.08)]:
        xv = np.log10(valor)
        ax.axvline(xv, color=TINTA_2, linewidth=0.9, zorder=3)
        ax.text(xv + desplaz, tope * 0.98, f"{texto}\n{num(valor)} kg", ha="right" if desplaz < 0 else "left",
                va="top", fontsize=8, color=TINTA)
    fig.tight_layout()
    fig.savefig(destino, bbox_inches="tight")
    plt.close(fig)
    return destino


def fig_meses_con_registro(d: pd.DataFrame, destino: Path) -> Path:
    """Cantidad de series especie-puerto según cuántos meses del período tienen registros."""
    plt = _estilo_matplotlib()
    total_meses = int(d["_periodo"].max() - d["_periodo"].min() + 1)
    meses = d.groupby(["especie", "puerto"])["_periodo"].nunique()
    conteo = meses.value_counts().reindex(range(1, total_meses + 1), fill_value=0)
    fig, ax = plt.subplots(figsize=(6.4, 2.4), dpi=200)
    ax.bar(conteo.index, conteo.values, width=0.62 if total_meses <= 24 else 0.9, color=AZUL, zorder=2)
    if total_meses <= 24:
        ax.set_xticks(conteo.index)
    ax.tick_params(axis="x", length=0)
    ax.set_xlabel(f"meses con al menos un registro (sobre {total_meses})")
    ax.set_ylabel("series especie-puerto")
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(destino, bbox_inches="tight")
    plt.close(fig)
    return destino


def fig_lag1(d: pd.DataFrame, destino: Path) -> Path:
    """log10(captura) del mes t contra el mes t-1, dentro de la misma serie."""
    plt = _estilo_matplotlib()
    d = d[d["captura"] > 0]
    t = d[CLAVE_SERIE + ["_periodo"]].copy()
    t["_y"] = np.log10(d["captura"].astype(float)).values
    t = t.sort_values(CLAVE_SERIE + ["_periodo"])
    g = t.groupby(CLAVE_SERIE, sort=False)
    t["_prev"] = g["_y"].shift(1)
    t = t[(t["_periodo"] - g["_periodo"].shift(1)) == 1]
    fig, ax = plt.subplots(figsize=(3.6, 3.4), dpi=200)
    ax.scatter(t["_prev"], t["_y"], s=6, color=AZUL, alpha=0.35, linewidths=0, zorder=2)
    lim = (0, np.ceil(max(t["_y"].max(), t["_prev"].max())))
    ax.plot(lim, lim, color=TINTA_MUTED, linewidth=0.8, zorder=1)
    ax.set_xlim(lim)
    ax.set_ylim(lim)
    ax.grid(True, axis="both")
    ticks = np.arange(0, lim[1] + 1, 2)
    ax.set_xticks(ticks, [num(10 ** v) for v in ticks], fontsize=7)
    ax.set_yticks(ticks, [num(10 ** v) for v in ticks], fontsize=7)
    ax.set_xlabel("captura mes t-1 (kg, log)")
    ax.set_ylabel("captura mes t (kg, log)")
    fig.tight_layout()
    fig.savefig(destino, bbox_inches="tight")
    plt.close(fig)
    return destino


# --------------------------------------------------------------------------
# Reporte
# --------------------------------------------------------------------------
def reporte(ruta: Path, df: pd.DataFrame, codificacion: str, fin_linea: str,
            anteriores: list[tuple[str, pd.DataFrame]], con_figuras: bool = True) -> str:
    d = preparar(df)
    nombre = ruta.stem
    md: list[str] = [f"# Perfilado de `{ruta.name}`", ""]
    md.append("> Reporte generado automáticamente por `src/perfilado.py`. Describe el archivo tal como fue "
              "publicado; no aplica ninguna limpieza.")
    md.append("")

    # 1. Estructura
    faltantes = [c for c in COLUMNAS if c not in df.columns]
    extra = [c for c in df.columns if c not in COLUMNAS]
    md += ["## 1. Estructura del archivo", ""]
    md.append(tabla([
        ["Codificación detectada", "UTF-8" if codificacion.startswith("utf") else "Latin-1 (ISO-8859-1)"],
        ["Fin de línea", fin_linea],
        ["Filas (registros)", num(len(df))],
        ["Columnas", num(df.shape[1])],
        ["Columnas esperadas ausentes", ", ".join(faltantes) or "ninguna"],
        ["Columnas no esperadas", ", ".join(extra) or "ninguna"],
        ["Fechas no interpretables", num(d["_fecha"].isna().sum())],
    ], ["Aspecto", "Valor"]))
    md.append("")

    # 2. Período
    por_mes = d.groupby(d["_fecha"].dt.to_period("M")).size()
    todos = pd.period_range(por_mes.index.min(), por_mes.index.max(), freq="M")
    sin_registros = [str(p) for p in todos if p not in por_mes.index]
    md += ["## 2. Período cubierto y registros por mes", ""]
    md.append(f"- Primer mes: **{por_mes.index.min()}** · último mes: **{por_mes.index.max()}** "
              f"({num(len(por_mes))} meses con datos).")
    md.append(f"- Meses del rango sin ningún registro: {', '.join(sin_registros) or 'ninguno'}.")
    md.append(f"- Registros por mes: mínimo {num(por_mes.min())} ({por_mes.idxmin()}), "
              f"mediana {num(por_mes.median(), 1)}, máximo {num(por_mes.max())} ({por_mes.idxmax()}).")
    md.append("")
    if len(por_mes) <= 24:
        md.append(tabla([[str(p), num(n)] for p, n in por_mes.items()], ["Mes", "Registros"], "lr"))
    else:
        por_anio = d.groupby(d["_fecha"].dt.year).agg(registros=("captura", "size"), meses=("_periodo", "nunique"))
        md.append(tabla([[int(a), num(r.registros), num(r.meses)] for a, r in por_anio.iterrows()],
                        ["Año", "Registros", "Meses con datos"], "lrr"))
    md.append("")

    # 3. Variables
    md += ["## 3. Variables", ""]
    filas = []
    for c in df.columns:
        s = df[c]
        ejemplo = s.dropna().iloc[0] if s.notna().any() else "-"
        filas.append([f"`{c}`", str(s.dtype), num(s.isna().sum()), pct(s.isna().mean()), num(s.nunique()), f"`{ejemplo}`"])
    md.append(tabla(filas, ["Variable", "Tipo leído", "Nulos", "% nulos", "Valores distintos", "Ejemplo"], "llrrrl"))
    md.append("")

    # 4. Categorías
    md += ["## 4. Categorías", ""]
    for c in ["flota", "categoria", "provincia", "especie_agrupada"]:
        vc = df[c].value_counts()
        md.append(f"**{c}** ({num(len(vc))} valores)")
        md.append("")
        md.append(tabla([[v, num(n), num(df.loc[df[c] == v, 'captura'].sum())] for v, n in vc.items()],
                        ["Valor", "Registros", "Captura total (kg)"], "lrr"))
        md.append("")
    puertos = (df.groupby("puerto")
                 .agg(provincia=("provincia", "first"), departamento=("departamento", "first"),
                      registros=("captura", "size"), sin_coord=("latitud", lambda s: s.isna().sum()),
                      latitud=("latitud", "first"), longitud=("longitud", "first"), kg=("captura", "sum"))
                 .sort_values("registros", ascending=False))
    md.append(f"**puerto** ({num(len(puertos))} valores)")
    md.append("")
    md.append(tabla([[p, r.provincia, r.departamento, num(r.registros), num(r.sin_coord), num(r.latitud, 4),
                      num(r.longitud, 4), num(r.kg)] for p, r in puertos.iterrows()],
                    ["Puerto", "Provincia", "Departamento", "Registros", "Sin coordenadas", "Latitud",
                     "Longitud", "Captura total (kg)"], "lllrrrrr"))
    md.append("")
    md.append(f"**especie**: {num(df['especie'].nunique())} valores distintos.")
    md.append("")
    largos = df["especie"].dropna().str.len()
    mas_largos = sorted(df.loc[largos.index[largos == largos.max()], "especie"].unique())
    md.append(f"Nombres de especie con la longitud máxima ({largos.max()} caracteres), posible truncamiento: "
              + ", ".join(f"`{e}`" for e in mas_largos) + ".")
    md.append("")

    # 5. Coordenadas faltantes
    sin = df[df["latitud"].isna() | df["longitud"].isna()]
    md += ["## 5. Coordenadas faltantes", ""]
    md.append(f"- Registros sin latitud o longitud: **{num(len(sin))}** ({pct(len(sin) / len(df))}).")
    if len(sin):
        g = sin.groupby(["puerto", "departamento"]).size()
        for (p, dep), n in g.items():
            con = df[(df["puerto"] == p) & df["latitud"].notna()]
            md.append(f"  - `{p}` (departamento `{dep}`): {num(n)} registros sin coordenadas; "
                      f"registros del mismo puerto con coordenadas: {num(len(con))}.")
    md.append("")

    # 6. Duplicados
    md += ["## 6. Duplicados", ""]
    dup_exactos = df.duplicated().sum()
    dup_clave = df.duplicated(CLAVE_REGISTRO).sum()
    dup_sin_agr = df.duplicated(["fecha", "flota", "puerto", "especie"]).sum()
    md.append(f"- Filas idénticas en todas las columnas: **{num(dup_exactos)}**.")
    md.append(f"- Filas repetidas según ({', '.join(CLAVE_REGISTRO)}): **{num(dup_clave)}**.")
    md.append(f"- Filas repetidas según (fecha, flota, puerto, especie), es decir, ignorando `especie_agrupada`: "
              f"**{num(dup_sin_agr)}**. Estas filas difieren en la agrupación de la especie.")
    md.append("")
    multi = df.groupby("especie")["especie_agrupada"].unique()
    multi = multi[multi.apply(len) > 1]
    md.append(f"Especies que aparecen en más de una `especie_agrupada`: **{num(len(multi))}**.")
    md.append("")
    if len(multi):
        md.append(tabla([[e, ", ".join(sorted(v))] for e, v in multi.items()], ["Especie", "Agrupaciones"]))
        md.append("")

    # 7. Captura
    c = df["captura"]
    q = c.quantile([0.25, 0.5, 0.75, 0.95, 0.99])
    md += ["## 7. Variable `captura` (kg)", ""]
    md.append(tabla([
        ["Mínimo", num(c.min())], ["Percentil 25", num(q[0.25], 1)], ["Mediana", num(q[0.5], 1)],
        ["Media", num(c.mean(), 1)], ["Percentil 75", num(q[0.75], 1)], ["Percentil 95", num(q[0.95], 1)],
        ["Percentil 99", num(q[0.99], 1)], ["Máximo", num(c.max())], ["Desvío estándar", num(c.std(), 1)],
        ["Valores ≤ 0", num((c <= 0).sum())], ["Suma total", f"{num(c.sum())} kg ({num(c.sum() / 1000)} t)"],
    ], ["Estadístico", "Valor"], "lr"))
    md.append("")
    md.append("Los 10 registros con mayor captura:")
    md.append("")
    top = df.sort_values("captura", ascending=False).head(10)
    md.append(tabla([[r.fecha, r.flota, r.puerto, r.especie, r.especie_agrupada, num(r.captura)] for r in top.itertuples()],
                    ["Fecha", "Flota", "Puerto", "Especie", "Agrupación", "Captura (kg)"], "lllllr"))
    md.append("")

    # 8. Completitud de series especie-puerto
    total_meses = int(d["_periodo"].max() - d["_periodo"].min() + 1)
    meses = d.groupby(["especie", "puerto"])["_periodo"].nunique()
    md += ["## 8. Meses con registros por serie especie-puerto", ""]
    md.append(f"- Series especie-puerto distintas: **{num(len(meses))}** (sumando todas las flotas y agrupaciones).")
    md.append(f"- Con registros en todos los meses del período ({total_meses}): **{num((meses == total_meses).sum())}** "
              f"({pct((meses == total_meses).mean())}).")
    mitad = total_meses // 2
    md.append(f"- Con registros en {mitad} meses o menos: **{num((meses <= mitad).sum())}** "
              f"({pct((meses <= mitad).mean())}).")
    md.append(f"- Con un único mes con registros: **{num((meses == 1).sum())}** ({pct((meses == 1).mean())}).")
    md.append("- El archivo no contiene capturas en cero: un mes sin actividad no aparece como fila.")
    md.append("")

    # 9. Consistencia
    k = consistencia(d)
    ref = k["ref"]
    md += ["## 9. Chequeos de consistencia de `captura`", ""]
    md.append("Se compara la estructura de log10(captura) con una referencia en la que los valores de captura se "
              f"permutan al azar entre las filas ({k['n_perm']} permutaciones, media ± desvío). Si un valor real "
              "queda cerca de su referencia, esa dimensión casi no aporta información sobre la captura.")
    md.append("")
    md.append(tabla([
        ["Correlación de log10(captura) entre meses consecutivos de una misma serie "
         f"(flota-puerto-especie-agrupación; {num(k['n_pares'])} pares)",
         num(k["lag1"], 3), f"{num(ref['lag1'][0], 3)} ± {num(ref['lag1'][1], 3)}"],
        ["Varianza de log10(captura) explicada por `especie` (η²)", pct(k["eta2"]["especie"]),
         f"{pct(ref['especie'][0])} ± {pct(ref['especie'][1])}"],
        ["Varianza de log10(captura) explicada por `flota` (η²)", pct(k["eta2"]["flota"]),
         f"{pct(ref['flota'][0])} ± {pct(ref['flota'][1])}"],
        ["Varianza de log10(captura) explicada por `puerto` (η²)", pct(k["eta2"]["puerto"]),
         f"{pct(ref['puerto'][0])} ± {pct(ref['puerto'][1])}"],
    ], ["Indicador", "Valor real", "Referencia permutada"], "lrr"))
    md.append("")
    md.append("Mediana de captura por registro de las 10 especies con mayor captura total:")
    md.append("")
    med = k["medianas"].head(10)
    md.append(tabla([[e, num(r["size"]), num(r["median"], 1), num(r["sum"])] for e, r in med.iterrows()],
                    ["Especie", "Registros", "Mediana (kg)", "Total (kg)"], "lrrr"))
    md.append("")

    # 10. Comparación con archivos anteriores
    for nombre_ant, df_ant in anteriores:
        md += [f"## Comparación de categorías con `{nombre_ant}`", ""]
        for col in ["flota", "puerto", "provincia", "categoria", "especie", "especie_agrupada"]:
            a, b = set(df_ant[col].dropna()), set(df[col].dropna())
            md.append(f"- **{col}**: solo en `{nombre_ant}`: {', '.join(sorted(a - b)) or 'ninguno'} · "
                      f"solo en `{ruta.name}`: {', '.join(sorted(b - a)) or 'ninguno'}.")
        md.append("")

    # Figuras
    if con_figuras:
        DIR_FIGURAS.mkdir(parents=True, exist_ok=True)
        figuras = [
            (fig_registros_por_mes(d, DIR_FIGURAS / f"{nombre}_registros_por_mes.png"), "Registros por mes"),
            (fig_distribucion_captura(d, DIR_FIGURAS / f"{nombre}_distribucion_captura.png"),
             "Distribución de la captura por registro"),
            (fig_meses_con_registro(d, DIR_FIGURAS / f"{nombre}_meses_con_registro.png"),
             "Series especie-puerto según meses con registros"),
            (fig_lag1(d, DIR_FIGURAS / f"{nombre}_captura_mes_anterior.png"),
             "Captura del mes t contra la del mes t-1 en la misma serie"),
        ]
        md += ["## Figuras", ""]
        for ruta_fig, titulo in figuras:
            if ruta_fig is not None:
                rel = Path("..") / ruta_fig.relative_to(RAIZ)
                md.append(f"**{titulo}**")
                md.append("")
                md.append(f"![{titulo}]({rel.as_posix()})")
                md.append("")
    return "\n".join(md)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("archivos", nargs="+", type=Path, help="CSV de desembarques a perfilar")
    parser.add_argument("--sin-figuras", action="store_true", help="no generar las figuras")
    args = parser.parse_args()

    DIR_REPORTES.mkdir(parents=True, exist_ok=True)
    leidos: list[tuple[str, pd.DataFrame]] = []
    for ruta in args.archivos:
        df, codificacion, fin_linea = leer_csv(ruta)
        texto = reporte(ruta, df, codificacion, fin_linea, anteriores=list(leidos), con_figuras=not args.sin_figuras)
        salida = DIR_REPORTES / f"perfilado_{ruta.stem}.md"
        salida.write_text(texto + "\n", encoding="utf-8")
        print(f"{ruta.name}: {len(df):,} filas -> {salida.relative_to(RAIZ)}")
        leidos.append((ruta.name, df))


if __name__ == "__main__":
    main()
