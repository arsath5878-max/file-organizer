import tkinter as tk
from tkinter import filedialog, messagebox

from organizer import preview_folder, organize_folder
from history import save_history, undo_last


def start_app():

    window = tk.Tk()
    window.title("File Organizer")
    window.geometry("750x600")

    selected_folder = tk.StringVar()

    # ---------------- TITLE ----------------

    title = tk.Label(
        window,
        text="File Organizer",
        font=("Arial", 22, "bold")
    )
    title.pack(pady=20)

    # ---------------- FOLDER ----------------

    folder_frame = tk.Frame(window)
    folder_frame.pack(pady=10)

    tk.Label(
        folder_frame,
        text="Folder:"
    ).pack(side="left")

    folder_box = tk.Entry(
        folder_frame,
        textvariable=selected_folder,
        width=55
    )
    folder_box.pack(side="left", padx=10)

    # ---------------- TEXT BOX ----------------

    output = tk.Text(
        window,
        width=85,
        height=20
    )
    output.pack(pady=15)

    # ---------------- FUNCTIONS ----------------

    def choose_folder():

        folder = filedialog.askdirectory()

        if folder:
            selected_folder.set(folder)

            output.insert(
                tk.END,
                "Selected: " + folder + "\n"
            )


    def preview():

        folder = selected_folder.get()

        if not folder:
            messagebox.showwarning(
                "Warning",
                "Please select a folder."
            )
            return

        try:
            files = preview_folder(folder)
        except Exception as error:
            messagebox.showerror(
                "Error",
                str(error)
            )
            return

        output.delete("1.0", tk.END)

        if not files:
            output.insert(
                tk.END,
                "No files found.\n"
            )
            return

        output.insert(
            tk.END,
            "Preview\n"
        )
        output.insert(
            tk.END,
            "------------------------------\n"
        )

        for file in files:

            output.insert(
                tk.END,
                file["name"]
                + " -> "
                + file["category"]
                + "\n"
            )

        output.insert(
            tk.END,
            "\nTotal files: "
            + str(len(files))
            + "\n"
        )


    def organize():

        folder = selected_folder.get()

        if not folder:
            messagebox.showwarning(
                "Warning",
                "Please select a folder."
            )
            return

        files = preview_folder(folder)

        if not files:
            messagebox.showinfo(
                "Info",
                "No files to organize."
            )
            return

        answer = messagebox.askyesno(
            "Confirm",
            "Do you want to organize these files?"
        )

        if not answer:
            return

        try:
            moved_files, count = organize_folder(folder)
            save_history(moved_files)

        except Exception as error:
            messagebox.showerror(
                "Error",
                str(error)
            )
            return

        output.delete("1.0", tk.END)

        output.insert(
            tk.END,
            "Files organized successfully!\n"
        )
        output.insert(
            tk.END,
            "------------------------------\n"
        )

        for category in count:
            output.insert(
                tk.END,
                category
                + ": "
                + str(count[category])
                + " file(s)\n"
            )

        output.insert(
            tk.END,
            "\nTotal: "
            + str(len(moved_files))
            + " file(s)\n"
        )

        messagebox.showinfo(
            "Complete",
            "Files organized successfully!"
        )


    def undo():

        restored = undo_last()

        if restored == 0:
            messagebox.showinfo(
                "Undo",
                "Nothing to undo."
            )
            return

        output.insert(
            tk.END,
            "\nUndo completed. "
            + str(restored)
            + " file(s) restored.\n"
        )

        messagebox.showinfo(
            "Undo",
            str(restored)
            + " file(s) restored."
        )


    # ---------------- BUTTONS ----------------

    buttons = tk.Frame(window)
    buttons.pack(pady=10)

    tk.Button(
        buttons,
        text="Browse",
        width=15,
        command=choose_folder
    ).pack(side="left", padx=5)

    tk.Button(
        buttons,
        text="Preview",
        width=15,
        command=preview
    ).pack(side="left", padx=5)

    tk.Button(
        buttons,
        text="Organize",
        width=15,
        command=organize
    ).pack(side="left", padx=5)

    tk.Button(
        buttons,
        text="Undo",
        width=15,
        command=undo
    ).pack(side="left", padx=5)

    tk.Button(
        buttons,
        text="Exit",
        width=10,
        command=window.destroy
    ).pack(side="left", padx=5)

    # Start the window
    window.mainloop()
