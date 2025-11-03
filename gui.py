import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, Label, Button
from tkinter import font as tkFont

import pyperclip
import webbrowser
from papersummary.main import run, SUPPORTED_FILETYPES, DEFAULT_PROMPT
from papersummary.utils import add_regex_filter

FILE_BROWSER_FILTER = (
    ("Supported Files", add_regex_filter(SUPPORTED_FILETYPES)), 
    ("all files", "*.*")
)

def browse_file():
    """
    Opens a file dialog to select a file and updates the label with the selected file path.
    """
    global filepath
    selected_path = filedialog.askopenfilename(
        initialdir="./",
        title="Select a File",
        filetypes=FILE_BROWSER_FILTER
    )
    if selected_path:
        filepath = selected_path
        # Update the label to show the selected file path
        file_path_label.config(text=f"{filepath}", wraplength=400)

def generate(filepath: str, prompt: str, copy_to_clipoard: bool):#, txt_file):
    global output_to_copy
    # Check if a file has actually been selected
    if not filepath:
        generate_label.config(text="Please select a file first.", wraplength=400)
        return # <--- Stop execution if no file
    
    try:
    
        results = run(
            file_paths=[filepath], 
            prompt=prompt,
            copy_to_clipoard=copy_to_clipoard
        )

        success, msg, output = results[0]
    
        if not success:
            generate_label.config(text=msg, wraplength=400)
        else:
            generate_label.config(text=f"Prompt generated: {msg}", wraplength=400)
            output_to_copy = output
    except Exception as e:
        print(f"Unknown Exception: {e}")
        generate_label.config(text=f"Error! Please contact the developers: \n{e}", wraplength=400)

def copy_output(output: str):
    try:
        if len(output) > 0:
            pyperclip.copy(output)
            generate_label.config(text=f"{generate_label['text']}\nCopied prompt to clipboard.", wraplength=400)
        else:
            generate_label.config(text=f"{generate_label['text']}\nPlease click Generate Prompt first.", wraplength=400)
    except Exception as e:
        print(f"Unknown Exception: {e}")
        generate_label.config(text=f"{generate_label['text']}\n\nError in trying to copy to clipbaord! Please contact the developers: \n{e}", wraplength=400)

def open_link(event):
    """Opens the specified URL in the default web browser."""
    webbrowser.open_new("https://github.com/ereoh/papersummary")

# --- Create the main window ---
root = tk.Tk()
root.title("papersummary")
root.geometry("700x1000") # Set a default size for the window

# Variables
filepath = ""
clipboard = tk.BooleanVar(value=False)
output_to_copy = ""

# A frame to hold the content with some padding
content_frame = tk.Frame(root, padx=10, pady=10)
content_frame.pack(expand=True, fill='both')


# File Browsing
file_browse_frame = tk.Frame(content_frame)
file_browse_frame.pack(pady=10)

# Button to trigger the file browser dialog
browse_button = Button(
    file_browse_frame,
    text="Browse for File",
    command=browse_file
)
browse_button.pack(side='right', padx=(10, 0))

# display chosen file
file_path_label = Label(
    file_browse_frame,
    text="No file selected.",
    wraplength=350,
    justify='left'
)
file_path_label.pack(side='left', fill='x', expand=True)

# Options
options_frame = tk.Frame(content_frame)
options_frame.pack(pady=10)

# clipboard_check = tk.Checkbutton(
#     options_frame,
#     text="Copy to Clipboard",
#     variable=clipboard
# )
# clipboard_check.pack(anchor='w', padx=5, pady=(10, 0)) # anchor='w' (west) aligns it left
# TODO: Output file to txt file

# Prompt Text Box
prompt_label = tk.Label(
    options_frame,
    text="Prompt (optional):"
)
prompt_label.pack(anchor='w', padx=5)
prompt_text = tk.Text(options_frame, height=3, wrap='word')
prompt_text.pack(fill='x', padx=5, pady=(0, 5))
prompt_text.insert(tk.END, DEFAULT_PROMPT)


separator = ttk.Separator(content_frame, orient='horizontal')
separator.pack(fill='x', pady=10)

# Button to trigger txt conversion
generate_button = Button(
    content_frame,
    text="Generate Prompt",
    command=lambda: generate(
        filepath=filepath,
        prompt=prompt_text.get("1.0", tk.END).strip(),
        copy_to_clipoard = clipboard.get()
    )
)
generate_button.pack(pady=10)

# Label to display generation process
generate_label = Label(
    content_frame,
    text="No prompt generated.",
    pady=20
)
generate_label.pack()

# Copy output to clipboard
copy_button = Button(
    content_frame,
    text="Copy Output to Clipboard",
    command=lambda: copy_output(
        output=output_to_copy
    )
)
copy_button.pack(pady=10)

# Footer
footer_frame = tk.Frame(root, bg="#f0f0f0")
footer_frame.pack(
    side=tk.BOTTOM, 
    fill=tk.X  # Make the frame fill the entire width
)
footer_font = tkFont.Font(family="Helvetica", size=10, slant="italic")
link_font = tkFont.Font(family="Helvetica", size=10, underline=True)

# Developer Credits
author_label = tk.Label(
    footer_frame,
    text="Created by Ere Oh",
    font=footer_font,
    fg="grey",
    bg="#f0f0f0" # Match the frame background
)
# Pack it to the left side of the footer_frame
author_label.pack(side=tk.LEFT, padx=(10, 10)) # Add 10px padding on the left
# Link to Github page
link_label = tk.Label(
    footer_frame,
    text="Github",
    font=link_font,
    fg="blue",
    cursor="hand2",
    bg="#f0f0f0"
)
link_label.pack(side=tk.LEFT)

link_label.bind("<Button-1>", open_link)

# --- Start the GUI event loop ---
root.mainloop()
