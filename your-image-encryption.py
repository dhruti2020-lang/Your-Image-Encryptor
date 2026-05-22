import tkinter as tk
from tkinter import filedialog, messagebox
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import os

# -----------------------------
# Global Variables
# -----------------------------
selected_file = ""
encrypted_data_global = None
decrypted_data_global = None
encrypted_extension = ".enc"

# -----------------------------
# Theme Colors
# -----------------------------
BG_COLOR = "#050505"
FG_COLOR = "#39FF14"
BTN_COLOR = "#0D0D0D"
BTN_ACTIVE = "#1AFF00"
ENTRY_BG = "#101010"
FONT_STYLE = ("Consolas", 16)
TITLE_FONT = ("Consolas", 26, "bold")
SUB_FONT = ("Consolas", 18, "bold")

# -----------------------------
# AES Functions
# -----------------------------
def generate_key(password, salt):
    return PBKDF2(password, salt, dkLen=32)


def encrypt_image(file_path, password):
    global encrypted_data_global

    try:
        salt = get_random_bytes(16)
        key = generate_key(password.encode(), salt)

        cipher = AES.new(key, AES.MODE_CBC)

        with open(file_path, 'rb') as file:
            image_data = file.read()

        encrypted_data = cipher.encrypt(pad(image_data, AES.block_size))

        encrypted_data_global = salt + cipher.iv + encrypted_data

        messagebox.showinfo("Success", "Image encrypted successfully!\nNow click DOWNLOAD to save encrypted image.")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def decrypt_image(file_path, password):
    global decrypted_data_global

    try:
        with open(file_path, 'rb') as file:
            salt = file.read(16)
            iv = file.read(16)
            encrypted_data = file.read()

        key = generate_key(password.encode(), salt)

        cipher = AES.new(key, AES.MODE_CBC, iv)

        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

        decrypted_data_global = decrypted_data

        messagebox.showinfo("Success", "Image decrypted successfully!\nNow click DOWNLOAD to save decrypted image.")

    except Exception as e:
        messagebox.showerror("Error", "Wrong key or corrupted file!\n\n" + str(e))

# -----------------------------
# File Selection
# -----------------------------
def select_encrypt_file():
    global selected_file

    selected_file = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
    )

    encrypt_file_label.config(text=os.path.basename(selected_file))


def select_decrypt_file():
    global selected_file

    selected_file = filedialog.askopenfilename(
        title="Select Encrypted File",
        filetypes=[("Encrypted Files", "*.enc")]
    )

    decrypt_file_label.config(text=os.path.basename(selected_file))

# -----------------------------
# Download Functions
# -----------------------------
def download_encrypted():
    global encrypted_data_global

    if encrypted_data_global is None:
        messagebox.showwarning("Warning", "No encrypted image available!")
        return

    save_path = filedialog.asksaveasfilename(
        title="Save Encrypted Image",
        defaultextension=".enc",
        filetypes=[("Encrypted Files", "*.enc")]
    )

    if save_path:
        with open(save_path, 'wb') as file:
            file.write(encrypted_data_global)

        messagebox.showinfo("Downloaded", "Encrypted image saved successfully!")


def download_decrypted():
    global decrypted_data_global

    if decrypted_data_global is None:
        messagebox.showwarning("Warning", "No decrypted image available!")
        return

    save_path = filedialog.asksaveasfilename(
        title="Save Decrypted Image",
        defaultextension=".jpg",
        filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")]
    )

    if save_path:
        with open(save_path, 'wb') as file:
            file.write(decrypted_data_global)

        messagebox.showinfo("Downloaded", "Decrypted image saved successfully!")

# -----------------------------
# Encryption Action
# -----------------------------
def start_encryption():
    password = encrypt_key_entry.get()

    if not selected_file:
        messagebox.showwarning("Warning", "Please upload an image!")
        return

    if not password:
        messagebox.showwarning("Warning", "Please enter encryption key!")
        return

    encrypt_image(selected_file, password)

# -----------------------------
# Decryption Action
# -----------------------------
def start_decryption():
    password = decrypt_key_entry.get()

    if not selected_file:
        messagebox.showwarning("Warning", "Please upload encrypted image!")
        return

    if not password:
        messagebox.showwarning("Warning", "Please enter decryption key!")
        return

    decrypt_image(selected_file, password)

# -----------------------------
# Window Navigation
# -----------------------------
def open_encrypt_window():
    main_frame.pack_forget()
    encrypt_frame.pack(fill="both", expand=True)


def open_decrypt_window():
    main_frame.pack_forget()
    decrypt_frame.pack(fill="both", expand=True)


def go_home(frame):
    frame.pack_forget()
    main_frame.pack(fill="both", expand=True)

# -----------------------------
# Main Window
# -----------------------------
root = tk.Tk()
root.title("AES Image Encryptor & Decryptor")
root.geometry("700x500")
root.configure(bg=BG_COLOR)

# -----------------------------
# Main Menu Frame
# -----------------------------
main_frame = tk.Frame(root, bg=BG_COLOR)
main_frame.pack(fill="both", expand=True)

main_title = tk.Label(
    main_frame,
    text="YOUR IMAGE ENCRYPTOR",
    bg=BG_COLOR,
    fg=FG_COLOR,
    font=TITLE_FONT
)
main_title.pack(pady=50)

question_label = tk.Label(
    main_frame,
    text="Do you want to Encrypt or Decrypt your image?",
    bg=BG_COLOR,
    fg=FG_COLOR,
    font=SUB_FONT
)
question_label.pack(pady=20)

encrypt_button = tk.Button(
    main_frame,
    text="ENCRYPT IMAGE",
    command=open_encrypt_window,
    bg=BTN_COLOR,
    fg=FG_COLOR,
    activebackground=BTN_ACTIVE,
    activeforeground="black",
    width=25,
    height=2,
    font=("Consolas", 16)
)
encrypt_button.pack(pady=20)


decrypt_button = tk.Button(
    main_frame,
    text="DECRYPT IMAGE",
    command=open_decrypt_window,
    bg=BTN_COLOR,
    fg=FG_COLOR,
    activebackground=BTN_ACTIVE,
    activeforeground="black",
    width=25,
    height=2,
    font=("Consolas", 16)
)
decrypt_button.pack(pady=20)

# -----------------------------
# Encryption Frame
# -----------------------------
encrypt_frame = tk.Frame(root, bg=BG_COLOR)

enc_title = tk.Label(
    encrypt_frame,
    text="IMAGE ENCRYPTION",
    bg=BG_COLOR,
    fg=FG_COLOR,
    font=TITLE_FONT
)
enc_title.pack(pady=20)

upload_btn = tk.Button(
    encrypt_frame,
    text="UPLOAD IMAGE",
    command=select_encrypt_file,
    bg=BTN_COLOR,
    fg=FG_COLOR,
    activebackground=BTN_ACTIVE,
    activeforeground="black",
    width=20,
    font=("Consolas", 16)
)
upload_btn.pack(pady=10)

encrypt_file_label = tk.Label(
    encrypt_frame,
    text="No file selected",
    bg=BG_COLOR,
    fg=FG_COLOR,
    font=("Consolas", 16)
)
encrypt_file_label.pack(pady=5)

key_label = tk.Label(
    encrypt_frame,
    text="ENTER ENCRYPTION KEY",
    bg=BG_COLOR,
    fg=FG_COLOR,
    font=("Consolas", 16)
)
key_label.pack(pady=10)

encrypt_key_entry = tk.Entry(
    encrypt_frame,
    width=35,
    bg=ENTRY_BG,
    fg=FG_COLOR,
    insertbackground=FG_COLOR,
    font=("Consolas", 16)
)
encrypt_key_entry.pack(pady=10)

encrypt_now_btn = tk.Button(
    encrypt_frame,
    text="ENCRYPT",
    command=start_encryption,
    bg=BTN_COLOR,
    fg=FG_COLOR,
    activebackground=BTN_ACTIVE,
    activeforeground="black",
    width=20,
    font=("Consolas", 16)
)
encrypt_now_btn.pack(pady=15)


download_enc_btn = tk.Button(
    encrypt_frame,
    text="DOWNLOAD ENCRYPTED FILE",
    command=download_encrypted,
    bg=BTN_COLOR,
    fg=FG_COLOR,
    activebackground=BTN_ACTIVE,
    activeforeground="black",
    width=28,
    font=("Consolas", 16)
)
download_enc_btn.pack(pady=10)

back_btn_encrypt = tk.Button(
    encrypt_frame,
    text="BACK TO HOME",
    command=lambda: go_home(encrypt_frame),
    bg=BTN_COLOR,
    fg=FG_COLOR,
    activebackground=BTN_ACTIVE,
    activeforeground="black",
    width=20,
    height=2,
    font=("Consolas", 16)
)
back_btn_encrypt.pack(pady=20)



# -----------------------------
# Decryption Frame
# -----------------------------
decrypt_frame = tk.Frame(root, bg=BG_COLOR)

dec_title = tk.Label(
    decrypt_frame,
    text="IMAGE DECRYPTION",
    bg=BG_COLOR,
    fg=FG_COLOR,
    font=TITLE_FONT
)
dec_title.pack(pady=20)

upload_dec_btn = tk.Button(
    decrypt_frame,
    text="UPLOAD ENCRYPTED IMAGE",
    command=select_decrypt_file,
    bg=BTN_COLOR,
    fg=FG_COLOR,
    activebackground=BTN_ACTIVE,
    activeforeground="black",
    width=25,
    font=("Consolas", 16)
)
upload_dec_btn.pack(pady=10)

decrypt_file_label = tk.Label(
    decrypt_frame,
    text="No file selected",
    bg=BG_COLOR,
    fg=FG_COLOR,
    font=("Consolas", 16)
)
decrypt_file_label.pack(pady=5)

key_dec_label = tk.Label(
    decrypt_frame,
    text="ENTER DECRYPTION KEY",
    bg=BG_COLOR,
    fg=FG_COLOR,
    font=("Consolas", 16)
)
key_dec_label.pack(pady=10)

decrypt_key_entry = tk.Entry(
    decrypt_frame,
    width=35,
    bg=ENTRY_BG,
    fg=FG_COLOR,
    insertbackground=FG_COLOR,
    font=("Consolas", 16)
)
decrypt_key_entry.pack(pady=10)


decrypt_now_btn = tk.Button(
    decrypt_frame,
    text="DECRYPT",
    command=start_decryption,
    bg=BTN_COLOR,
    fg=FG_COLOR,
    activebackground=BTN_ACTIVE,
    activeforeground="black",
    width=20,
    font=("Consolas", 16)
)
decrypt_now_btn.pack(pady=15)


download_dec_btn = tk.Button(
    decrypt_frame,
    text="DOWNLOAD DECRYPTED IMAGE",
    command=download_decrypted,
    bg=BTN_COLOR,
    fg=FG_COLOR,
    activebackground=BTN_ACTIVE,
    activeforeground="black",
    width=28,
    font=("Consolas", 16)
)
download_dec_btn.pack(pady=10)

back_btn2 = tk.Button(
    decrypt_frame,
    text="BACK",
    command=lambda: go_home(decrypt_frame),
    bg=BTN_COLOR,
    fg=FG_COLOR,
    activebackground=BTN_ACTIVE,
    activeforeground="black",
    width=15,
    font=("Consolas", 16)
)
back_btn2.pack(pady=20)

# -----------------------------
# Run Application
# -----------------------------
root.mainloop()
