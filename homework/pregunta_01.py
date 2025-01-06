import pandas as pd
import os

def clean_data(df):
    """Limpieza completa de los datos"""
    df = df.copy()

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
    df["barrio"] = df["barrio"].str.lower().str.replace("_", " ").str.replace("-", " ")

    # Convertir fechas
    df["fecha_de_beneficio"] = pd.to_datetime(df["fecha_de_beneficio"], dayfirst=True, errors="coerce")

    # Eliminar duplicados y filas con valores faltantes
    df = df.dropna().drop_duplicates()

    return df


def pregunta_01():
    """
    Realiza la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    Elimina duplicados y filas con datos faltantes. Guarda el resultado limpio 
    en "files/output/solicitudes_de_credito_limpio.csv".
    """

    file_input_path = "files/input/solicitudes_de_credito.csv"
    file_output_path = "files/output/solicitudes_de_credito.csv"

    try:
        
        data = pd.read_csv(file_input_path, sep=None, engine='python')

        data_cleaned = clean_data(data)
       
        os.makedirs(os.path.dirname(file_output_path), exist_ok=True)

        # Guardar el archivo limpio
        data_cleaned.to_csv(file_output_path, index=False)

        print("Archivo limpio guardado en:", file_output_path)
    
    except pd.errors.ParserError as e:
        print("Error al procesar el archivo CSV. Verifica el delimitador o formato.")
        print("Detalle del error:", e)
    
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en {file_input_path}")
    
    except Exception as e:
        print(f"Se produjo un error: {e}")

pregunta_01()
