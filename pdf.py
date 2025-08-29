import os
import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2

try:
    # tkinterDnD2 is needed for drag-and-drop
    from tkinterdnd2 import TkinterDnD, DND_FILES
except ImportError:
    messagebox.showerror("Missing Library", "Please install tkinterDnD2:\n\npip install tkinterdnd2")
    raise

def select_files():
    """Open file dialog to select multiple PDFs."""
    files = filedialog.askopenfilenames(
        title="Select PDF files",
        filetypes=[("PDF Files", "*.pdf")]
    )
    if files:
        add_files(files)

def add_files(files):
    """Add selected or dropped files to the listbox."""
    for f in files:
        f = f.strip("{}")  # Handle spaces in file paths
        if f.lower().endswith(".pdf"):
            file_list.insert(tk.END, f)

def merge_pdfs():
    """Merge selected PDF files into one."""
    files = list(file_list.get(0, tk.END))
    if not files:
        messagebox.showwarning("No Files", "Please select at least one PDF.")
        return
    
    # Ask where to save merged file
    output_file = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")],
        title="Save Merged PDF As"
    )
    
    if output_file:
        merger = PyPDF2.PdfMerger()
        try:
            for pdf in files:
                merger.append(pdf)
            merger.write(output_file)
            merger.close()
            messagebox.showinfo("Success", f"Merged PDF saved as:\n{output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to merge PDFs:\n{e}")

def sort_files():
    """Sort files alphabetically in the listbox."""
    files = list(file_list.get(0, tk.END))
    files.sort()
    file_list.delete(0, tk.END)
    for f in files:
        file_list.insert(tk.END, f)

def clear_files():
    """Clear all files from the listbox."""
    file_list.delete(0, tk.END)

# TkinterDnD GUI Setup
root = TkinterDnD.Tk()
root.title("PDF Merger Tool 📄 ")
root.geometry("600x400")

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="📂 Select PDFs", command=select_files).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="🔀 Sort Files", command=sort_files).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="🗑 Clear All", command=clear_files).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="📌 Merge PDFs", command=merge_pdfs, bg="lightgreen").grid(row=0, column=3, padx=5)

# Listbox for files
file_list = tk.Listbox(root, width=70, height=15, selectmode=tk.MULTIPLE)
file_list.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Enable drag-and-drop
file_list.drop_target_register(DND_FILES)
file_list.dnd_bind("<<Drop>>", lambda e: add_files(e.data.split()))

# Run the app
root.mainloop()
