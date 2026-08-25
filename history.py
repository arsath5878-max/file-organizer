from pathlib import Path
import json
import shutil


history_file = Path("history.json")


def get_history():
    # Read the previous operations
    if not history_file.exists():
        return []

    try:
        with open(history_file, "r") as file:
            return json.load(file)
    except:
        return []


def save_history(moved_files):
    # Add the latest operation to history
    history = get_history()

    history.append(moved_files)

    with open(history_file, "w") as file:
        json.dump(history, file, indent=4)


def undo_last():
    # Undo the last organization
    history = get_history()

    if not history:
        return 0

    last = history.pop()
    restored = 0

    for item in reversed(last):

        old_file = Path(item["old"])
        new_file = Path(item["new"])

        if not new_file.exists():
            continue

        # Make sure the old folder exists
        old_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        # Move the file back
        if not old_file.exists():
            shutil.move(
                str(new_file),
                str(old_file)
            )
        else:
            # If the old name is already used,
            # give the restored file another name
            number = 1

            while True:
                restore_file = old_file.parent / (
                    old_file.stem
                    + "_restored_"
                    + str(number)
                    + old_file.suffix
                )

                if not restore_file.exists():
                    break

                number += 1

            shutil.move(
                str(new_file),
                str(restore_file)
            )

        restored += 1

    # Save the remaining history
    with open(history_file, "w") as file:
        json.dump(history, file, indent=4)

    return restored
