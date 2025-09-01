import tkinter as tk # Import tkinter toolkit
from tkinter import filedialog, messagebox, ttk 

class App(tk.Tk):   # App inherits tk
    def __init__(self):                 
        super().__init__()              # Initialize the Tk base class
        self.title("metext")            # Set window title
        self.geometry("900x600")        # Set window size (Width x Height)
        self.current_path = None        # Track the current file path
        self._build_ui()                # Construct layout & widgets
        self._bind_keys()               # Register keyboard shortcuts

    def _build_ui(self):
        menubar = tk.Menu(self)                                                 # Menubar container 
        file_menu = tk.Menu(menubar, tearoff=False)                             # Create "File" menu on the menubar (tearoff=False removes the dashed line)
        file_menu.add_command(label="New", command=self._action_new)            # Create Menu item New
        file_menu.add_command(label="Open", command=self._action_open)          # Create Menu item Open
        file_menu.add_command(label="Save", command=self._action_save)          # Create Menu item Save
        file_menu.add_command(label="Save As", command=self._action_save_as)    # Create Menu item Save As    
        file_menu.add_separator()                                               # Create divider between item groups
        file_menu.add_command(label="Exit", command=self.quit)                  # Create Menu item Exit

        menubar.add_cascade(label="File", menu=file_menu)                       # Attach the File menu to the menubar under the label "File"

        self.config(menu=menubar)                                               # Tell the window to use this menubar

        self.text = tk.Text(self, wrap="word", undo=True)                       # Create the central text editor widget (wrap="word": wraps at word boundaries; undo=True enables Crtl+Z history)

        self.text.pack(fill="both", expand=True)                                # Lay out the text widget to fill available space

    def _update_title(self):
        name = self.current_path if self.current_path else "None Loaded"
        self.title(f"metext - {name}")
    
    def _action_new(self):
        # Clear the text area and reset file state
        self.text.delete("1.0", "end")
        self.current_path = None
        self._update_title()

    def _action_open(self):
        pass

    def _action_save(self):
        pass

    def _action_save_as(self):
        pass

    def _bind_keys(self):
        self.bind("<Control-n>", lambda e: self._action_new())                  # Bind Ctrl+N "New"
        self.bind("<Control-o>", lambda e: self._action_open())                 # Bind Ctrl+N "Open"
        self.bind("<Control-s>", lambda e: self._action_save())                 # Bind Ctrl+N "Save"
        self.bind("<Control-S>", lambda e: self._action_save_as())              # Bind Ctrl+N "Save As"             


if __name__ == "__main__":      # run only when executed directly, not when imported
    app = App()                 # Create the app window
    app.mainloop()              # Start Tk's event loop 

