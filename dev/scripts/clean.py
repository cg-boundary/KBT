import os
import shutil

def cleaning_addon_directory():
    print("<----------------- Cleaning PyCache ----------------->")
    deleted = {}
    for root, dirs, files in os.walk(".", topdown=False):
        for file in files:
            if file.endswith(".pyc") or file.endswith(".blend1"):
                path = os.path.join(root, file)
                os.remove(path)
                deleted.setdefault(root, []).append(f"[F] {file}")
        for directory in dirs:
            if directory == "__pycache__":
                path = os.path.join(root, directory)
                shutil.rmtree(path)
                deleted.setdefault(root, []).append(f"[D] {directory}")

    def print_tree(base, indent=""):
        items = deleted.get(base, [])
        for i, item in enumerate(items):
            connector = "└── " if i == len(items)-1 else "├── "
            print(indent + connector + item)
        for entry in sorted(os.listdir(base)):
            path = os.path.join(base, entry)
            if os.path.isdir(path):
                if path in deleted or any(path in k for k in deleted):
                    print(indent + "├── " + f"[DIR] {entry}")
                    print_tree(path, indent + "│   ")
    print_tree(".")

cleaning_addon_directory()
