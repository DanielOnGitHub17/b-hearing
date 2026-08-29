import os
import re

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

migration_pattern = re.compile(r"^\d+.*\.py$")

for root, dirs, files in os.walk(PROJECT_ROOT):
    if "migrations" in dirs:
        migration_dir = os.path.join(root, "migrations")
        for f in os.listdir(migration_dir):
            if migration_pattern.match(f):
                file_path = os.path.join(migration_dir, f)
                print("Deleting:", file_path)
                os.remove(file_path)

print("Done.")
