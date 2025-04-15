import os
import glob

def convertir_txt_a_md(origen, destino):
    """
    Recorre todos los archivos .txt en 'origen' y crea archivos .md en 'destino' copiando su contenido.
    """
    # Crear la carpeta destino si no existe
    os.makedirs(destino, exist_ok=True)
    
    # Buscar todos los archivos .txt en la carpeta de origen
    archivos_txt = glob.glob(os.path.join(origen, "*.txt"))
    
    for archivo in archivos_txt:
        # Obtener solo el nombre del archivo sin ruta
        nombre_archivo = os.path.basename(archivo)
        # Extraer el nombre sin extensión
        nombre_sin_ext, _ = os.path.splitext(nombre_archivo)
        # Definir la ruta del nuevo archivo con extensión .md
        archivo_md = os.path.join(destino, nombre_sin_ext + ".md")
        
        # Leer el contenido del archivo TXT y escribirlo en el nuevo archivo MD
        with open(archivo, 'r', encoding='utf-8') as f_in:
            contenido = f_in.read()
            
        with open(archivo_md, 'w', encoding='utf-8') as f_out:
            f_out.write(contenido)
            
        print(f"Convertido: {archivo} --> {archivo_md}")

if __name__ == "__main__":
    # Carpeta origen con los archivos .txt
    carpeta_origen = r".\data\scripts_friends"
    # Carpeta destino donde se guardarán los archivos .md. Puedes cambiar el nombre de la carpeta destino.
    carpeta_destino = r".\data\scripts_friends_md"
    
    convertir_txt_a_md(carpeta_origen, carpeta_destino)
