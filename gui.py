import tkinter as tk
from tkinter import filedialog, Label, Button

from pdf2txt import generate_prompt

def browse_file():
    """
    Opens a file dialog to select a file and updates the label with the selected file path.
    """
    global pdf_filepath
    filepath = filedialog.askopenfilename(
        initialdir="./",  # You can set an initial directory
        title="Select a PDF",
        filetypes=(("PDF files", "*.pdf"), ("all files", "*.*"))
    )
    if filepath:
        pdf_filepath = filepath
        # Update the label to show the selected file path
        file_path_label.config(text=f"Selected File: {filepath}", wraplength=400)

def generate(pdf_file):#, prompt, txt_file):
    
    success, msg = generate_prompt(pdf_file=pdf_filepath)
    
    if not success:
        generate_label.config(text=msg, wraplength=400)
    else:
        generate_label.config(text=f"Prompt generated: {msg}", wraplength=400)

# --- Create the main window ---
root = tk.Tk()
root.title("File Browser GUI")
root.geometry("500x400") # Set a default size for the window

# --- Create and configure widgets ---

# A frame to hold the content with some padding
content_frame = tk.Frame(root, padx=10, pady=10)
content_frame.pack(expand=True, fill='both')

# Label to display the selected file path
# It starts with an instructional message
file_path_label = Label(
    content_frame,
    text="No file selected.",
    pady=20
)
file_path_label.pack()

pdf_filepath = ""

# Button to trigger the file browser dialog
browse_button = Button(
    content_frame,
    text="Browse for File",
    command=browse_file
)
browse_button.pack(pady=10)

# Button to trigger txt conversion
generate_button = Button(
    content_frame,
    text="Generate Prompt",
    command=lambda: generate(pdf_file=pdf_filepath)
)
generate_button.pack(pady=10)

# Label to display generation process
generate_label = Label(
    content_frame,
    text="No prompt generated.",
    pady=20
)
generate_label.pack()

# --- Start the GUI event loop ---
root.mainloop()
