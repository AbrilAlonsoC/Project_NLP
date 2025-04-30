import os
import glob

def convertir_txt_a_md(origen, destino):
    """
    Go through all .txt files in 'origen' and create .md files in 'destino' copying their content.
    """
    # Create the destination folder if it doesn't exist
    os.makedirs(destino, exist_ok=True)
    
    # Search for all .txt files in the source directory
    archivos_txt = glob.glob(os.path.join(origen, "*.txt"))
    
    for archivo in archivos_txt:
        # Obtain the base name of the file (e.g., "script1.txt")
        nombre_archivo = os.path.basename(archivo)
        # Get the file name without extension (e.g., "script1")
        nombre_sin_ext, _ = os.path.splitext(nombre_archivo)
        # Define the new file name with .md extension
        archivo_md = os.path.join(destino, nombre_sin_ext + ".md")
        
        # Read the content of the .txt file and write it to the .md file
        with open(archivo, 'r', encoding='utf-8') as f_in:
            contenido = f_in.read()
            
        with open(archivo_md, 'w', encoding='utf-8') as f_out:
            f_out.write(contenido)
            
        print(f"Convertido: {archivo} --> {archivo_md}")

if __name__ == "__main__":
    # Folder where the .txt files are located
    carpeta_origen = r".\data\scripts_friends"
    # Folder where the .md files will be created
    carpeta_destino = r".\data\scripts_friends_md"
    
    convertir_txt_a_md(carpeta_origen, carpeta_destino)
