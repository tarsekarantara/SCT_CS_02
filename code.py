import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

def process_image(path, key, mode):
    img = Image.open(path).convert("RGB")  # Ensure RGB mode
    pix = img.load()
    w, h = img.size
    delta = -1 if mode == "decrypt" else 1

    # Reverse pixel swap first in decryption
    if mode == "decrypt":
        for i in range(0, w - 1, 2):
            for j in range(h):
                pix[i, j], pix[i + 1, j] = pix[i + 1, j], pix[i, j]

    # Pixel manipulation
    for i in range(w):
        for j in range(h):
            r, g, b = pix[i, j]
            r = (r + delta * 30) % 256 ^ (key % 256)
            g = (g + delta * 20) % 256 ^ (key * 2 % 256)
            b = (b + delta * 10) % 256 ^ (key * 3 % 256)
            pix[i, j] = (r, g, b)

    # Swap pixels after encryption
    if mode == "encrypt":
        for i in range(0, w - 1, 2):
            for j in range(h):
                pix[i, j], pix[i + 1, j] = pix[i + 1, j], pix[i, j]

    # Save with mode suffix
    base, _ = os.path.splitext(path)
    out_path = f"{base}_{mode}.png"
    img.save(out_path, format="PNG")
    return out_path

def browse_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
    if file_path:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, file_path)

def run(mode):
    path = entry_file.get()
    key_text = entry_key.get()
    if not path or not key_text.isdigit():
        return messagebox.showwarning("Missing Input", "Please select an image and enter a numeric key.")
    try:
        key = int(key_text)
        out_path = process_image(path, key, mode)
        messagebox.showinfo("Success", f"{mode.title()}ion complete!\nSaved as: {out_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process image:\n{e}")

# GUI Setup
root = tk.Tk()
root.title("Image Encryptor")
root.geometry("400x220")
tk.Label(root, text="Select Image File (.jpg/.png):").pack(pady=5)
entry_file = tk.Entry(root, width=50); entry_file.pack()
tk.Button(root, text="Browse", command=browse_image).pack(pady=5)
tk.Label(root, text="Enter Numeric Key:").pack()
entry_key = tk.Entry(root); entry_key.pack(pady=5)
tk.Button(root, text="Encrypt", width=15, command=lambda: run("encrypt")).pack(pady=5)
tk.Button(root, text="Decrypt", width=15, command=lambda: run("decrypt")).pack(pady=5)
root.mainloop()