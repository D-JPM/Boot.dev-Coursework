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

    def _open_find_dialog(self):
        # If a Find window already exists, bring it to fron instead of creating another
        if hasattr(self, "_find_win") and self._find_win and self._find_win.winfo_exists():
            self._find_win.lift()   # Raise to top
            return
        
        self._find_win = tk.Toplevel(self)      # Create a child window
        self._find_win.title("Find/Replace")    # Window title
        self._find_win.transient(self)          # Keep on top of main window
        self._find_win.resizable(False, False)  # Fixed size dialog

        # "Find:" label and entry
        tk.Label(self._find_win, text="Find:").grid(row=0, column=0, padx=6, pady=6, sticky="e")
        self._find_var = tk.StringVar()         # Variable to hold the search pattern
        entry_find = tk.Entry(self._find_win, textvariable=self._find_var, width=30)
        entry_find.grid(row=0, column=1, padx=6, pady=6)
        entry_find.focus_set()                  # Focus the find box so you can type immediately

        # Buttons for find actions
        tk.Button(self._find_win, text="Find Next", command=self._find_next).grid(row=0, column=2, padx=6, pady=6)
        tk.Button(self._find_win, text="Close", command=self._find_win.destroy).grid(row=0, column=3, padx=6, pady=6)

        # "Replace:" label and entry
        tk.Label(self._find_win, text="Replace:").grid(row=1, column=0, padx=6, pady=6, sticky="e")
        self._repl_var = tk.StringVar()         # Variable for replacement text
        entry_repl = tk.Entry(self._find_win, textvariable=self._repl_var, width=30)
        entry_repl.grid(row=1, column=1, padx=6, pady=6)

        # Buttons for replace actions
        tk.Button(self._find_win, text="Replace", command=self._replace_one).grid(row=1, column=2, padx=6, pady=6)
        tk.Button(self._find_win, text="Replace All", command=self._replace_all).grid(row=1, column=3, padx=6, pady=6)
                  
        entry_find.bind("<Return>", lambda e: self._find_next())
      
    def _find_next(self):
        # Get the search pattern; if dialog isn't open or field empty, do nothing
        pattern = (self._find_var.get() if hasattr(self, "_find_var") else "").strip()
        if not pattern:
            return
        
        # Remove any previous highlight so we can show only the current match
        self.text.tag_remove("find_highlight", "1.0", "end")

        # Start searching just after the current cursor position to find the "next" match
        start = self.text.index("insert +1c")
        pos = self.text.search(pattern, start, stopindex="end", nocase=False)
        
        if not pos:
           pos = self.text.search(pattern, "1.0", stopindex="end", nocase=False)
           if not pos:
                return
        
        # Compute the end index by advancing pattern length in characters
        end = f"{pos}+{len(pattern)}c"

        # Add a tag to gighlight the found text range and configure its appearance
        self.text.tag_add("find_highlight", pos, end)
        self.text.tag_config("find_highlight", background="#ffd54f") # Light yellow 

        # Move the cursor to the end of the match and ensure it;s visible
        self.text.mark_set("insert", end)
        self.text.see("insert")

    def _bind_keys(self):
        self.bind("<Control-n>", lambda e: self._action_new())                  # Bind Ctrl+n "New"
        self.bind("<Control-o>", lambda e: self._action_open())                 # Bind Ctrl+o "Open"
        self.bind("<Control-s>", lambda e: self._action_save())                 # Bind Ctrl+s "Save"
        self.bind("<Control-S>", lambda e: self._action_save_as())              # Bind Ctrl+S "Save As"
        self.bind("<Control-f>", lambda e: self._open_find_dialog())             # Bind Ctrl+f "Find"      


if __name__ == "__main__":      # run only when executed directly, not when imported
    app = App()                 # Create the app window
    app.mainloop()              # Start Tk's event loop 