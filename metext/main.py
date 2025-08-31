import tkinter as tk # Import tkinter toolkit
from tkinter import filedialog, messagebox, ttk 

class App(tk.Tk):   # App inherits tk
    def __init__(self):                 
        super().__init__()              # Initialize the Tk base class
        self.title("metext")            # Set window title
        self.geometry("900x600")        # Set window size (Width x Height)
        self.grab_current = None        # Track the current file path
        self._build_ui()                # Construct layout & widgets
        self._bind_keys()               # Register keyboard shortcuts

    def _build_ui(self):
        pass    # Create widgets

    def _bind_keys(self):
        pass    # Create shortcuts

if __name__ == "__main__":      # run only when executed directly, not when imported
    app = App()                 # Create the app window
    app.mainloop()              # Start Tk's event loop 

