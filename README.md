# 📝 To-Do List App (Tkinter GUI)

Aplikasi To-Do List ini dibuat menggunakan **Python + Tkinter** dengan fitur lengkap seperti:
- Tambah, edit, dan hapus task
- Filter berdasarkan status & kategori
- Sorting berdasarkan nama, prioritas, tanggal, kategori
- Pencarian real-time
- Progress bar penyelesaian task
- Penyimpanan otomatis ke file `tasks.json`
- GUI modern dengan ttk styling & `tkcalendar`

## 📁 Struktur Proyek

```
/
├─ Task.py              # Class model untuk Task
├─ TaskManager.py       # Manajemen task & JSON storage
├─ ToDoListApp.py       # GUI aplikasi utama dengan Tkinter
├─ tasks.json           # File penyimpanan task (otomatis dibuat)
└─ main.py              # Entry point menjalankan aplikasi
```

## 🚀 Cara Menjalankan

### 1️⃣ Instalasi Dependensi
Pastikan Python sudah terinstal. Kemudian jalankan:

```bash
pip install tkcalendar
```

### 2️⃣ Buat File `main.py` seperti ini:

```python
import tkinter as tk
from ToDoListApp import ToDoListApp

def main():
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

### 3️⃣ Jalankan Program

```bash
python main.py
```

## 🧠 Cara Kerja Aplikasi

### 🔹 Task.py
Mendefinisikan class Task dengan atribut:
- name, priority, due_date, category
- is_completed (status)
- method toggle_status(), update(), to_dict(), from_dict()

### 🔹 TaskManager.py
Mengelola daftar task:
- Menambah & menghapus task
- Menyimpan & membaca dari tasks.json
- Sorting & filtering

### 🔹 ToDoListApp.py
GUI utama dengan fitur:
| Fitur | Keterangan |
|------|-------------|
| Add Task | Form input task baru |
| Edit Task | Window pop-up untuk mengedit |
| Remove Task | Hapus task yang dipilih |
| Toggle Status | Klik dua kali pada item / tombol |
| Search | Ketik untuk filter langsung |
| Progress Bar | Menampilkan jumlah task selesai |
| Sorting | Klik header tabel |
| Filtering | Berdasarkan status & kategori |

## 🛠 Pengembangan Lanjutan (Ide Upgrade)
- Export ke Excel / PDF
- Reminder menggunakan notifikasi desktop
- Integrasi dengan database SQLite / PostgreSQL
- Multi-user login
- Mode gelap (dark mode)

