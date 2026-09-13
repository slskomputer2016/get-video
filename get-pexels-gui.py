# ============================================================
# IMPORT LIBRARY
# ============================================================
import os,random,string
import shutil
import sys
import re
import requests,datetime
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
#from deep_translator import GoogleTranslator


# ============================================================
# FUNGSI PROSES
# ============================================================
def download_file(url, save_path):
    x=1
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(8192):
                file.write(chunk)
        print(f"(info) - File downloaded successfully.")
        x=x+1
    else:
        print("(info) - Failed to download the file.")

#get_video_combo(string,dropdown,file,folder)



# ============================================================
# FUNGSI PILIH FILE
# ============================================================

def pilih_file():
    file = filedialog.askopenfilename(
        title="Pilih File",
        filetypes=[
            ("Semua File", "*.*"),
            ("Video", "*.mp4 *.avi *.mkv"),
            ("Audio", "*.mp3 *.wav")
        ]
    )
    if file:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, file)


# ============================================================
# FUNGSI PILIH FOLDER
# ============================================================

def pilih_folder():
    folder = filedialog.askdirectory(
        title="Pilih Folder"
    )
    if folder:
        entry_folder.delete(0, tk.END)
        entry_folder.insert(0, folder)

def quit_app():
    root.destroy()



def get_video_combo(t_search,orientation,folder,auth_key):
    #t_search = GoogleTranslator(source="id",target="en")
    #karakter = string.ascii_letters + string.digits
    #teks_acak = ''.join(random.choices(karakter, k=8))
    video_hasil = t_search.replace(" ", "_")


    #'WHMp7lbDRzdEJ7fctwnr6TRZe0keuUVsHkweUX5smr3I5flGbF3owWDa'
    #+------------------------------------------------------+
    url = "https://api.pexels.com/videos/search"
    headers = {
      "Authorization": auth_key
    }
    params = {
      "query": t_search,
      "orientation": orientation,
      "per_page": 50
    }
    response = requests.get(url, headers=headers, params=params)
    json_data = response.json()
    links = []
    for i in range(50):
        link = json_data['videos'][i]['video_files'][0]['link']
        download_file(link,f'{folder}/{video_hasil}_{orientation}_{i}.mp4')

def proses():
    #file = entry_file.get()
    folder = entry_folder.get()
    #angka = int(entry_angka.get())
    auth_key = entry_key.get()
    string = entry_string.get()
    dropdown = combo_posisi.get()
    print("====================================")
    print("HASIL INPUT")
    print("====================================")
    #print("File     :", file)
    print("Folder   :", folder)
    #print("Angka    :", angka)
    print("String   :", string)
    print("Dropdown :", dropdown)
    print("====================================")

    get_video_combo(string,dropdown,folder,auth_key)







# ============================================================
# WINDOW UTAMA
# ============================================================
# Membuat window utama
root = tk.Tk()
# Judul aplikasi
root.title("Aplikasi Download Video")
# Ukuran window
root.geometry("750x500")
# Tidak bisa di-resize
root.resizable(False, False)




# ============================================================
# PEMBUATAN INPUTAN
# ============================================================

# Label "Pilih Folder"
tk.Label(
    root,
    text="Pilih Folder           ",
    font=("Arial", 11)
).place(
    x=30,
    y=80
)
# Entry untuk lokasi folder
entry_folder = tk.Entry(
    root,
    width=50,
    font=("Arial", 10)
)

entry_folder.place(
    x=180,
    y=80
)
# Tombol pilih folder
btn_folder = tk.Button(
    root,
    text="Folder",
    width=12,
    command=pilih_folder
)
btn_folder.place(
    x=600,
    y=77
)




# ============================================================
# INPUT STRING
# ============================================================

# Label string
tk.Label(
    root,
    text="Auth Pexels        ",
    font=("Arial", 11)
).place(
    x=30,
    y=150
)


# Entry string
entry_key = tk.Entry(
    root,
    width=50,
    font=("Arial", 10)
)

entry_key.place(
    x=180,
    y=150
)


# Nilai awal string
entry_key.insert(
    0,
    ""
)






# Label string
tk.Label(
    root,
    text="Kata kunci         ",
    font=("Arial", 11)
).place(
    x=30,
    y=220
)

# Entry string
entry_string = tk.Entry(
    root,
    width=50,
    font=("Arial", 10)
)

entry_string.place(
    x=180,
    y=220
)


# Nilai awal string
entry_string.insert(
    0,
    ""
)




# ============================================================
# INPUT DROPDOWN
# ============================================================

# Label dropdown
tk.Label(
    root,
    text="Orientation          ",
    font=("Arial", 11)
).place(
    x=30,
    y=300
)
# Membuat Combobox / Dropdown
combo_posisi = ttk.Combobox(
    root,
    # Pilihan yang tersedia
    values=[
        "landscape",
        "portrait",
    ],

    # Lebar dropdown
    width=18,

    # Dropdown hanya bisa memilih pilihan
    # yang sudah tersedia
    state="readonly"
)
# Menentukan posisi dropdown
combo_posisi.place(
    x=180,
    y=300
)

# Menentukan pilihan awal
# index 0 = "Atas"
combo_posisi.current(0)

# ============================================================
# BUTTON PROSES
# ============================================================
btn_proses = tk.Button(
    root,
    text="Proses",
    width=20,
    height=2,
    command=proses
)

btn_proses.place(
    x=250,
    y=350
)

btn_quit = tk.Button(
    root,
    text="Keluar",
    width=20,
    height=2,
    command=quit_app
)

btn_quit.place(
    x=420,
    y=350
)


# ============================================================
# INPUT FILE
# ============================================================
# tk.Label(
#     root,
#     text="Pilih File:",
#     font=("Arial", 11)
# ).place(
#     x=30,
#     y=30
# )
# # Entry untuk lokasi file
# entry_file = tk.Entry(
#     root,
#     width=65,
#     font=("Arial", 10)
# )

# entry_file.place(
#     x=120,
#     y=30
# )


# # Tombol pilih file
# btn_file = tk.Button(
#     root,
#     text="Pilih File",
#     width=12,
#     command=pilih_file
# )
# btn_file.place(
#     x=600,
#     y=27
# )




# ============================================================
# INPUT ANGKA
# ============================================================

# Label angka
# tk.Label(
#     root,
#     text="Angka:",
#     font=("Arial", 11)
# ).place(
#     x=30,
#     y=130
# )
# # Entry angka
# entry_angka = tk.Entry(
#     root,
#     width=20,
#     font=("Arial", 10)
# )

# entry_angka.place(
#     x=120,
#     y=130
# )
# # Nilai awal angka
# entry_angka.insert(0, "10")









# ============================================================
# MENJALANKAN GUI
# ============================================================
# Menjalankan event loop Tkinter
root.mainloop()
