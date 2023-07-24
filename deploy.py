import sys
import pandas as pd
import subprocess

def merge_branches_to_deploy(deploy_branch, branches_to_merge):
    try:
        # Actualizar la rama del deploy a la última versión
        subprocess.run(["git", "checkout", deploy_branch])
        subprocess.run(["git", "pull"])

        for branch in branches_to_merge:
            # Asegurarse de estar en la rama principal antes de fusionar
            subprocess.run(["git", "checkout", deploy_branch])
            
            # Fusionar la rama especificada con la rama del deploy
            merge_result = subprocess.run(["git", "merge", branch], capture_output=True)
            
            if merge_result.returncode != 0:
                # Ocurrió un conflicto en el merge
                print(f"Hubo un conflicto al fusionar la rama '{branch}' en '{deploy_branch}'")
                print("Por favor, resuelva los conflictos y luego continúe.")
                return
            
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando Git: {e}")

def main():
    if len(sys.argv) < 3:
        print("Uso: python script.py <ruta_del_archivo.csv> <nombre_de_la_rama_del_deploy>")
        sys.exit(1)

    # Ruta del archivo CSV
    csv_file_path = sys.argv[1]

    # Lee el archivo CSV con las ramas a fusionar
    df = pd.read_csv(csv_file_path)

    # Nombre de la rama del deploy
    deploy_branch = sys.argv[2]

    # Obtiene la lista de ramas desde el archivo
    branches_to_merge = df["Branches"].tolist()

    # Fusionar las ramas especificadas con la rama del deploy
    merge_branches_to_deploy(deploy_branch, branches_to_merge)

if __name__ == "__main__":
    main()
