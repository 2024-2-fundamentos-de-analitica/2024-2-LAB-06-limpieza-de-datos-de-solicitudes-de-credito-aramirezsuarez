import os
import pandas as pd
from unidecode import unidecode

def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"
    """

    # Crear la carpeta "output" si no existe
    output_dir = "./files/output"
    os.makedirs(output_dir, exist_ok=True)

    # Leer el archivo
    df = pd.read_csv("./files/input/solicitudes_de_credito.csv", sep=";", index_col=0)
    df.dropna(inplace=True)

    # Columnas de texto
    txt_columns = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "línea_credito",
    ]
    for column in txt_columns:
        df[column] = df[column].apply(
            lambda x: unidecode(str(x))
            .lower()
            .strip()
            .strip("-")
            .strip("_")
            .replace(" ", "_")
            .replace("-", "_")
        )

    # Convertir fechas al formato YYYY-MM-DD
    df["fecha_de_beneficio"] = df["fecha_de_beneficio"].apply(
        lambda x: (
            "/".join([y for y in reversed(x.split("/"))])
            if len(x.split("/")[0]) == 4
            else x
        )
    )

    # Normalizar idea de negocio
    df["idea_negocio"] = df["idea_negocio"].apply(
        lambda x: (
            "_".join(x.split("_")[:-1]).strip("_")
            if x.split("_")[-1] in ("de", "en", "el", "y")
            else x
        )
    )

    # Convertir monto_del_credito a número
    df["monto_del_credito"] = (
        df["monto_del_credito"]
        .apply(lambda x: str(x).replace("$ ", "").replace(",", "").split(".")[0])
        .astype(int)
    )

    # Corregir estrato y comuna
    df["estrato"] = (
        df["estrato"].astype(str).str.replace("[^0-9]", "", regex=True).astype(int)
    )
    df["comuna_ciudadano"] = (
        df["comuna_ciudadano"].apply(lambda x: str(int(x)).replace("0", "")).astype(int)
    )

    # Corregir barrios
    df["barrio"] = df["barrio"].apply(
        lambda x: str(x).replace("no.", "no_").replace("no ", "no_").replace("__", "_")
    )

    # Corregir caracteres faltantes
    df["barrio"] = df["barrio"].apply(
        lambda x: str(x)
        .replace(".", "")
        .replace("?", "e")
        .replace("?", "n")
        .replace("narieo", "narino")
    )

    # Corregir linea credito
    df["línea_credito"] = df["línea_credito"].apply(
        lambda x: str(x).replace("soli_diaria", "solidaria").replace("cap.", "cap_")
    )

    # Eliminar duplicados
    df.drop_duplicates(inplace=True)

    conteo_barrios = df["línea_credito"].value_counts()
    print(conteo_barrios)

    # Guardar el archivo limpio
    df.to_csv(f"{output_dir}/solicitudes_de_credito.csv", sep=";", index=False)

pregunta_01()
