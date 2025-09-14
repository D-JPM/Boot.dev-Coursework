import tkinter as tk # Import tkinter toolkit
from tkinter import filedialog, messagebox, ttk 

class App(tk.Tk):   # App inherits tk
    def __init__(self):                 
        super().__init__()              # Initialize the Tk base class
        self.title("metext")            # Set window title
        self.geometry("900x600")        # Set window size (Width x Height)
        self.current_path = None        # Track the current file path
        self.modified = False           # Does the buffer have unsaved changes
        self._build_ui()                # Construct layout & widgets
        self.protocol("WM_DELETE_WINDOW", self._on_close) # When the window close button is clicked, call _on_close handler
        self._bind_keys()               # Register keyboard shortcuts

        # Binds
        self.text.bind("<<Modified>>", self._on_text_modified) # When text is modified, call handler
        self.text.bind("<KeyRelease>", self._update_status) # After any key release, refresh status bar
        self.text.bind("<ButtonRelease-1>", self._update_status) # After left mouse click release, refresh status bar

        self.text.edit_modified(False)  # Reset Tkinters inetnal modified flag to "clean"
        self._update_title()            # Set initial window title (reflecting current state)
        self._update_status()           # Render initial status text (line:column, Saved/Modified) 

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
        
        # Status Bar
        status_frame = tk.Frame(self)                                           # Container at the bottom for status widgets
        status_frame.pack(side="bottom", fill="x")                              # Dock to bottom; stretch horizontally
        self.status = tk.Label(status_frame, anchor="w")                        # Left-aligned text label for status 
        self.status.pack(side="left", fill="x", expand=True)                    # Let label expand to fill the frame  

    def _on_close(self):
        if not self._maybe_confirm_discard(): # If there are unsaved changes and user cancels, abort closing
            return # Otherwise, close the window and end the app
        self.destroy()

    def _update_status(self, even=None):
        index = self.text.index("insert")                                       # Current cursor index as "line.column" (e.g., "12.34")
        line, col = index.split(".")                                            # Split into line and column strings
        state = "Modifed" if self.modified else "Saved"                         # Show unsaved/saved state
        self.status.config(text=f"Ln {line}, col {int(col)+1} | {state}")       # Display 1-based column

    def _update_title(self):
        name = self.current_path if self.current_path else "None Loaded"
        self.title(f"metext - {name}")

    def _on_text_modified(self, event=None):
        if self.text.edit_modified():           # Check Tkinters internal "modified" state
            self.modified = True                # mark app-level flag as dirty.unsaved
            self.text.edit_modified(False)      # immediatley clear Tk's flag (we get future events)
            self._update_title()                # Refresh title to show the asterisk
            self._update_status()               # Reflect Modified in status bar

    def _update_title(self):
        name = self.current_path if self.current_path else "Untitled"   # Show filename or placeholder
        star = " *" if self.modified else ""                            # Show "*" when unsaved
        self.title(f"metext - {name}{star}")                            # Supply the composed title
    
    def _action_new(self):
        if not self._maybe_confirm_discard():   # If User cancels stop this action
            return
        # Clear the text area and reset file state
        self.text.delete("1.0", "end")
        self.current_path = None
        self._update_title()
        self._update_status()

    def _action_open(self):
        if not self._maybe_confirm_discard():   # If User cancels stop this action
            return
        # Ask user to pick a file: empty string if cancelled
        path = filedialog.askopenfilename(
            title="Open file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not path:
            return # Cancelled
        try:
            # Open the selected file for reading as text (UTF-8) and ensure it closes automatically
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()                                              # Read entire file into a string
        except Exception as e:
            # If anything goes wrong (missing file etc..), show an error dialog
            messagebox.showerror("Open Error", str(e))
            return                                                              # Abort the open action on error

        self.text.delete("1.0", "end")                                          # Remove all text from line 1, char 0 to the end
        self.text.insert("1.0", content)                                        # Insert loaded file content at the very start
        self.text.mark_set("insert", "1.0")                                     # Move the text cursor to start
        self.text.see("insert")                                                 # Scroll view so the cursor postiion is visible
        self.current_path = path                                                # Remember which file is currently open    
        self._update_title()                                                    # Refresh window title to show file name/path
        self._update_status()

    def _maybe_confirm_discard(self):
        if not self.modified:                                                       # If there are no unsaved changes
            return True                                                             # Proceed without asking
        # Ask the user if changes can be discared; True = proceed, False = cancel
        return messagebox.askyesno("Unsaved changes", "Discard unsaved changes?")   

    def _action_save(self):
        # If no file path yet, delegate to "Save As"
        if self.current_path is None:
            return self._action_save_as()
        
        try:                                                                    
            content = self.text.get("1.0", "end-1c")                            # Get all text from the editor, excluding the trailing newline Tk adds
            with open(self.current_path, "w", encoding="utf-8") as f:           # Open the current file for writing (UTF-8) and ensure it closes
                f.write(content)                                                # Write editor content to disk
        except Exception as e:                                                                  
            messagebox.showerror("Save Error", str(e))                          # Show and error dialog if saving fails (permissions, disk, etc...)                    
            return
        
        
        self._update_title()                                                      # Refresh the window title (e.g. clear modified marker later)
        self._update_status()

    def _action_save_as(self):
        path = filedialog.asksaveasfilename(                                    # Ask the user for a traget path; empty string if they cancel
            title="Save As",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not path:
            return                                                              # User Cancelled
        
        try:
            content = self.text.get("1.0", "end-1c")                            # Get editor content (without trailing newline)
            with open(path, "w", encoding="utf-8") as f:                        # Write content to the chosen path
                f.write(content)
        except Exception as e:
            messagebox.showerror("Save As Error", str(e))                       # Show an error dialog if writing fails
            return
        # Update current file path and refresh title
        self.current_path = path
        self._update_title()
        self._update_status()

    def _bind_keys(self):
        self.bind("<Control-n>", lambda e: self._action_new())                  # Bind Ctrl+N "New"
        self.bind("<Control-o>", lambda e: self._action_open())                 # Bind Ctrl+N "Open"
        self.bind("<Control-s>", lambda e: self._action_save())                 # Bind Ctrl+N "Save"
        self.bind("<Control-S>", lambda e: self._action_save_as())              # Bind Ctrl+N "Save As"             


if __name__ == "__main__":      # run only when executed directly, not when imported
    app = App()                 # Create the app window
    app.mainloop()              # Start Tk's event loop 