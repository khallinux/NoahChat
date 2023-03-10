
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from api_key import API_KEY
class ApiKey:
    def __init__(self):
        self.file_path = "api_key.py"
        self.api_key = None
        self.get_api_key()
    def get_api_key(self):
        self.api_key = str(API_KEY)

        if not self.api_key:
            # If the API key is empty, prompt the user to enter it with a custom dialog
            root = tk.Tk()
            root.withdraw()

            # Create a custom dialog with an entry widget and edit menu options
            dialog = tk.Toplevel()
            dialog.title("API Key")
            dialog.geometry("300x100")
            dialog.resizable(False, False)
            label = tk.Label(dialog, text="Please enter your API key:")
            label.pack(pady=5)

            entry = tk.Entry(dialog, width=50)
            entry.pack(padx=10, pady=5)
            entry.focus_set()
            root.protocol("WM_DELETE_WINDOW",lambda :on_closing)

            def on_closing():
                if messagebox.askokcancel("Quit", "Do you want to quit?"):
                    root.destroy()
            # Define the edit menu options for the entry widget
            def cut():
                entry.event_generate("<<Cut>>")

            def copy():
                entry.event_generate("<<Copy>>")

            def paste():
                entry.delete(0,END)
                entry.event_generate("<<Paste>>")

            def select_all():
                entry.event_generate("<<SelectAll>>")

            def delete():
                entry.event_generate("<Delete>")

            def update_context_menu():
                # enable or disable the copy, cut, delete, and select-all options based on whether text is selected
                if isinstance(entry, Entry):
                    if len(entry.get()) > 0:
                        edit_menu.entryconfigure("Cut", state=NORMAL)
                        edit_menu.entryconfigure("Copy", state=NORMAL)
                        edit_menu.entryconfigure("Paste", state=NORMAL)
                        edit_menu.entryconfigure("Delete", state=NORMAL)
                        edit_menu.entryconfigure("Select All", state=NORMAL)
                    else:
                        edit_menu.entryconfigure("Cut", state=DISABLED)
                        edit_menu.entryconfigure("Copy", state=DISABLED)
                        edit_menu.entryconfigure("Paste", state=NORMAL)
                        edit_menu.entryconfigure("Delete", state=DISABLED)
                        edit_menu.entryconfigure("Select All", state=NORMAL)
            # Create the edit menu
            edit_menu = tk.Menu(dialog, tearoff=0)
            edit_menu.add_command(label="Cut", command=cut)
            edit_menu.add_command(label="Copy", command=copy)
            edit_menu.add_command(label="Paste", command=paste)
            edit_menu.add_command(label="Select All", command=select_all)
            edit_menu.add_command(label="Delete", command=delete)
            def hide_context_menu( event):
                # hide the context menu if it's currently shown
                if edit_menu:
                    edit_menu.unpost()
            # Bind the edit menu options to the entry widget
            entry.bind("<Button-3>", lambda event: edit_menu.post(event.x_root, event.y_root))
            entry.bind("<Control-Key-x>", lambda event: cut())
            entry.bind("<Control-Key-c>", lambda event: copy())
            entry.bind("<Control-Key-v>", lambda event: paste())
            entry.bind("<Control-Key-a>", lambda event: select_all())
            entry.bind("<Delete>", lambda event: delete())
            entry.bind("<Button-1>", hide_context_menu)
            entry.bind("<KeyRelease>",lambda event: update_context_menu())

            def on_ok():
                # Save the entered API key and close the dialog
                self.api_key = entry.get()
                if self.api_key.strip() != "":
                    # Write the API key to the file if it is not empty
                    with open(self.file_path, "w") as f:
                        f.write("API_KEY = '{}'".format(self.api_key))
                    dialog.destroy()
                else:
                    messagebox.showwarning("API Key", "Please enter a valid API key.")

            button = tk.Button(dialog, text="OK", command=on_ok)
            button.pack(pady=5)
            dialog.bind("<Return>", lambda event: on_ok())
            dialog.bind("<Escape>", lambda event: dialog.destroy())
            dialog.grab_set()
            dialog.wait_window()
            # Disable the edit menu options if the entry widget is empty
    def __str__(self):
        return self.api_key

