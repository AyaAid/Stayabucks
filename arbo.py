import os

def display_directory_tree(root_dir, indent=""):
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)
        if os.path.isdir(item_path):
            if not item == '.git':  # Exclure le répertoire .git
                print(f"{indent}├── {item}/")
                display_directory_tree(item_path, indent + "│   ")
        else:
            print(f"{indent}├── {item}")

# Chemin du répertoire à afficher
directory_path = "/Users/ramjoh/documents_local/API_cours/Stayabucks/"

# Afficher l'arborescence du répertoire
display_directory_tree(directory_path)
