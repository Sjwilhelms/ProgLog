import os
import sys
import fileinput

def rename_project(old_name, new_name):
    """
    Rename all references to the old project name in the codebase.
    """
    # Files to check (extend as needed)
    files_to_check = [
        'manage.py',
        'config/wsgi.py',
        'config/asgi.py',
        'config/settings/base.py',
        'config/settings/dev.py',
        'config/settings/prod.py',
        'env.py',
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"Checking {file_path}...")
            with fileinput.FileInput(file_path, inplace=True) as file:
                for line in file:
                    print(line.replace(old_name, new_name), end='')
    
    print(f"Project renamed from '{old_name}' to '{new_name}'")
    print("Remember to update your database name if necessary!")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python rename_project.py old_name new_name")
        sys.exit(1)
    
    old_name = sys.argv[1]
    new_name = sys.argv[2]
    rename_project(old_name, new_name)