import pandas as pd
import os

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

        data.columns = data.columns.str.strip()

        data_cleaned = data.drop_duplicates()

        data_cleaned = data_cleaned.dropna(how='any')

       
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
