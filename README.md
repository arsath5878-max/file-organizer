# File Organizer

This is a simple Python project that organizes files into folders based on their extensions.

## Features

- Select a folder
- Preview files
- Organize files
- Handle duplicate file names
- Show file counts
- Undo the last organization
- Multiple files can be undone one operation at a time

## Project files

```text
File_Organizer/
│
├── main.py
├── gui.py
├── organizer.py
├── config.py
├── history.py
└── README.md
```

## Run the project

Open the project folder in VS Code.

Run:

```bash
python main.py
```

No external packages are needed.

## Basic process

```text
Select Folder
      ↓
Preview
      ↓
Check Extension
      ↓
Find Category
      ↓
Create Folder
      ↓
Move File
      ↓
Save History
```

## Important

Use a test folder first because the program actually moves files.
