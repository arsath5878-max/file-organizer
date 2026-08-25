from pathlib import Path
import shutil
from config import file_types


def get_category(extension):
    # Check which category contains the extension
    for category, extensions in file_types.items():
        if extension in extensions:
            return category

    return "Others"


def get_new_name(folder, file):
    # Create a new name if the same file already exists
    new_file = folder / file.name

    if not new_file.exists():
        return new_file

    number = 1

    while True:
        name = file.stem + "_" + str(number) + file.suffix
        new_file = folder / name

        if not new_file.exists():
            return new_file

        number += 1


def preview_folder(folder_path):
    # Show where the files will be moved
    folder = Path(folder_path)
    files = []

    for file in folder.iterdir():

        if file.is_file():
            category = get_category(file.suffix.lower())

            files.append({
                "name": file.name,
                "category": category
            })

    return files


def organize_folder(folder_path):
    # Move files into their category folders
    folder = Path(folder_path)

    moved_files = []
    count = {}

    for file in folder.iterdir():

        if not file.is_file():
            continue

        extension = file.suffix.lower()
        category = get_category(extension)

        # Create category folder
        new_folder = folder / category
        new_folder.mkdir(exist_ok=True)

        # Get a safe file name
        new_file = get_new_name(new_folder, file)

        # Move the file
        shutil.move(str(file), str(new_file))

        moved_files.append({
            "old": str(file),
            "new": str(new_file)
        })

        # Count files
        if category not in count:
            count[category] = 0

        count[category] += 1

    return moved_files, count
