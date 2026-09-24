"""Tabla de coordenadas por puerto para completar latitud y longitud faltantes.

Como los puertos son pocos (20 en 2019, 23 en 2010-2018), las coordenadas se
manejan con una tabla de referencia, una fila por puerto:

1. Armar la tabla: toma las coordenadas que el dataset ya trae para cada
   puerto (cada puerto tiene siempre el mismo par) y deja en blanco los que no
   tienen ninguna.

       python src/coordenadas.py data/raw/captura-puerto-flota-2019.csv [otro.csv ...]

2. Buscar a mano las coordenadas de los puertos que quedaron en blanco (por
   ejemplo en Google Maps u OpenStreetMap) y anotarlas en
   data/referencias/coordenadas_puertos.csv, con la fuente en la columna
   `fuente`. Al volver a correr el paso 1, esos valores se conservan.

3. Completar el dataset desde el código de limpieza:

       from coordenadas import completar_coordenadas
       df = completar_coordenadas(df)

   Agrega la columna `coordenadas_origen` (original / tabla / sin dato) para
   saber qué filas se completaron.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from perfilado import RAIZ, leer_csv

TABLA = RAIZ / "data" / "referencias" / "coordenadas_puertos.csv"
COLUMNAS_TABLA = ["puerto", "provincia", "latitud", "longitud", "fuente", "registros", "registros_sin_coordenadas", "nota"]
NOTA_AGREGADO = "Agrupa varios puertos de la provincia: no tiene una ubicación única."


def armar_tabla(dfs: list[pd.DataFrame], previa: pd.DataFrame | None = None) -> pd.DataFrame:
    """Una fila por puerto con las coordenadas del dataset; conserva las cargadas a mano en `previa`."""
    datos = pd.concat(dfs, ignore_index=True)
    filas = []
    for puerto, g in datos.groupby("puerto"):
        con = g.dropna(subset=["latitud", "longitud"])
        fila = {
            "puerto": puerto,
            "provincia": g["provincia"].iloc[0],
            "latitud": np.nan,
            "longitud": np.nan,
            "fuente": "",
            "registros": len(g),
            "registros_sin_coordenadas": len(g) - len(con),
            "nota": "",
        }
        if len(con):
            # Cada puerto tiene un único par de coordenadas; si hubiera más de uno, se toma el más frecuente.
            lat, lon = con.groupby(["latitud", "longitud"]).size().idxmax()
            fila.update(latitud=lat, longitud=lon, fuente="dataset")
        elif str(puerto).lower().startswith("otros puertos"):
            fila["nota"] = NOTA_AGREGADO
        filas.append(fila)
    tabla = pd.DataFrame(filas, columns=COLUMNAS_TABLA)

    if previa is not None and len(previa):
        manual = previa[(previa["fuente"].fillna("") != "dataset") & previa["latitud"].notna() & previa["longitud"].notna()]
        manual = manual.set_index("puerto")
        for i, fila in tabla.iterrows():
            if fila["fuente"] != "dataset" and fila["puerto"] in manual.index:
                m = manual.loc[fila["puerto"]]
                tabla.loc[i, ["latitud", "longitud", "fuente"]] = [m["latitud"], m["longitud"], m["fuente"]]
                if pd.notna(m.get("nota")) and m.get("nota"):
                    tabla.loc[i, "nota"] = m["nota"]
    return tabla.sort_values("registros", ascending=False).reset_index(drop=True)


def completar_coordenadas(df: pd.DataFrame, ruta_tabla: Path = TABLA) -> pd.DataFrame:
    """Completa latitud y longitud faltantes con la tabla de referencia, sin tocar las que ya están."""
    tabla = pd.read_csv(ruta_tabla).drop_duplicates("puerto").set_index("puerto")
    out = df.copy()
    faltan = out["latitud"].isna() | out["longitud"].isna()
    lat = out["puerto"].map(tabla["latitud"])
    lon = out["puerto"].map(tabla["longitud"])
    completar = faltan & lat.notna() & lon.notna()
    out.loc[completar, "latitud"] = lat[completar]
    out.loc[completar, "longitud"] = lon[completar]
    out["coordenadas_origen"] = np.select([~faltan, completar], ["original", "tabla"], default="sin dato")
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("archivos", nargs="+", type=Path, help="CSV de desembarques")
    args = parser.parse_args()

    dfs = [leer_csv(ruta)[0] for ruta in args.archivos]
    previa = pd.read_csv(TABLA) if TABLA.exists() else None
    tabla = armar_tabla(dfs, previa)
    TABLA.parent.mkdir(parents=True, exist_ok=True)
    tabla.to_csv(TABLA, index=False, float_format="%.6f")
    print(f"Tabla de coordenadas: {TABLA.relative_to(RAIZ)} ({len(tabla)} puertos)")

    sin = tabla[tabla["latitud"].isna()]
    if len(sin):
        print("Puertos sin coordenadas en la tabla:")
        for _, f in sin.iterrows():
            extra = f" ({f['nota']})" if f["nota"] else " -> buscar y anotar en la tabla"
            print(f"  - {f['puerto']}: {f['registros_sin_coordenadas']} registros{extra}")

    for ruta, df in zip(args.archivos, dfs):
        completo = completar_coordenadas(df)
        conteo = completo["coordenadas_origen"].value_counts()
        print(f"{ruta.name}: " + ", ".join(f"{k} = {v}" for k, v in conteo.items()))


if __name__ == "__main__":
    main()
