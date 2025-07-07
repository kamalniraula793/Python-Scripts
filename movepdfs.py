import os
import shutil
from pathlib import Path

# Define the destination folder
desktop = Path.home() / "Desktop"
destination_folder = desktop / "All pdfs"
destination_folder.mkdir(exist_ok=True)

# List of folders to search for PDFs
folders_to_search = [
    Path.home() / "Downloads",
    Path.home() / "Documents",
    Path.home() / "Desktop"
]

# Copy all PDFs to destination
for folder in folders_to_search:
    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(".pdf"):
                source_path = Path(root) / file
                destination_path = destination_folder / file

                # Avoid overwriting files with same names
                if destination_path.exists():
                    base, ext = os.path.splitext(file)
                    counter = 1
                    while True:
                        new_filename = f"{base}_{counter}{ext}"
                        new_dest = destination_folder / new_filename
                        if not new_dest.exists():
                            destination_path = new_dest
                            break
                        counter += 1

                # Copy the file
                shutil.copy2(source_path, destination_path)
                print(f"Copied: {source_path} -> {destination_path}")

