import os
import pandas as pd

def load_data(input_file):
    """Cargar archivo CSV desde la ruta especificada"""
    return pd.read_csv(input_file, sep=";", index_col=None)

def _create_output_directory(output_directory):
    """Crear o limpiar el directorio de salida"""
    if os.path.exists(output_directory):
        for file in os.listdir(output_directory):
            os.remove(os.path.join(output_directory, file))
        os.rmdir(output_directory)
    os.makedirs(output_directory)

def _save_output(output_directory, filename, df):
    """Guardar el DataFrame en el directorio especificado"""
    df.to_csv(f"{output_directory}/{filename}.csv", index=False, sep=";")

def clean_data(df):
    """Limpieza completa de los datos"""
    df = df.copy()

    # Eliminar columna Unnamed: 0 si existe
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # Transformar columnas numéricas a entero
    df["monto_del_credito"] = (df["monto_del_credito"].str.strip()
                                                  .str.strip("$")
                                                  .str.replace(".00", "")
                                                  .str.replace(",", "")
                                                  .astype(int))
    df["comuna_ciudadano"] = df["comuna_ciudadano"].astype(int)

    # Limpieza de columnas de texto
    df["sexo"] = df["sexo"].str.strip().str.lower()
    df["tipo_de_emprendimiento"] = df["tipo_de_emprendimiento"].str.strip().str.lower()
    df["línea_credito"] = (df["línea_credito"].str.strip()
                                            .str.lower()
                                            .str.replace(" ", "")
                                            .str.translate(str.maketrans("", "", "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")))
    df["idea_negocio"] = (df["idea_negocio"].str.strip()
                                              .str.lower()
                                              .str.replace("á", "a")
                                              .str.replace("é", "e")
                                              .str.replace("í", "i")
                                              .str.replace("ó", "o")
                                              .str.replace("ú", "u")
                                              .str.replace(" ", "")
                                              .str.translate(str.maketrans("", "", "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")))
    df["barrio"] = (df["barrio"].str.lower()
                                    .str.replace("_", " ")
                                    .str.replace("-", " "))

    # Convertir fechas
    df["fecha_de_beneficio"] = pd.to_datetime(df["fecha_de_beneficio"], dayfirst=True, errors="coerce")

    # Eliminar duplicados y filas con valores faltantes
    df = df.dropna().drop_duplicates()

    return df

def pregunta_01():
    """Proceso principal para limpiar y guardar el archivo de solicitudes de crédito"""
    file_input_path = "files/input/solicitudes_de_credito.csv"
    file_output_path = "files/output/solicitudes_de_credito.csv"

    try:
        # Cargar datos
        data = pd.read_csv(file_input_path, sep=";", engine='python')

        # Limpiar datos
        data_cleaned = clean_data(data)

        # Crear directorio de salida si no existe
        os.makedirs(os.path.dirname(file_output_path), exist_ok=True)

        # Guardar el archivo limpio
        data_cleaned.to_csv(file_output_path, index=False, sep=";")

        print("Archivo limpio guardado en:", file_output_path)

    except pd.errors.ParserError as e:
        print("Error al procesar el archivo CSV. Verifica el delimitador o formato.")
        print("Detalle del error:", e)

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en {file_input_path}")

    except Exception as e:
        print(f"Se produjo un error: {e}")

pregunta_01()
