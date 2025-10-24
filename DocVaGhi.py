

import csv
import tkinter as tk
from tkinter import filedialog, messagebox

# --- HÀM MỞ FILE CSV ---
def mo_file():
    filepath = filedialog.askopenfilename(
        title="Chọn file CSV để mở",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    if not filepath:
        return

    try:
        # Mở file CSV đúng cách theo docs (newline='', delimiter=',', quotechar='"')
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            text.delete("1.0", tk.END)
            for row in reader:
                # Ghép các cột bằng dấu phẩy để hiển thị trong ô văn bản
                text.insert(tk.END, ', '.join(row) + '\n')

        messagebox.showinfo("Thành công", f"Đã mở file CSV:\n{filepath}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể đọc file:\n{e}")

# --- HÀM GHI FILE CSV ---
def ghi_file():
    filepath = filedialog.asksaveasfilename(
        title="Lưu file CSV mới",
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    if not filepath:
        return

    try:
        # Mở file ở chế độ ghi (newline='' tránh dòng trống thừa)
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(
                csvfile,
                delimiter=',',
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL
            )

            # Lấy dữ liệu trong ô văn bản
            data = text.get("1.0", tk.END).strip().split("\n")
            for line in data:
                # Mỗi dòng tách theo dấu phẩy thành list
                writer.writerow([col.strip() for col in line.split(",")])

        messagebox.showinfo("Thành công", f"Đã ghi file CSV:\n{filepath}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể ghi file:\n{e}")

# --- GIAO DIỆN TKINTER ---
root = tk.Tk()
root.title("Đọc & Ghi File CSV (theo Python.org)")
root.geometry("800x500")

# Frame chứa nút
frame = tk.Frame(root)
frame.pack(pady=10)

btn_open = tk.Button(frame, text="📂 Mở CSV", width=15, command=mo_file)
btn_open.pack(side=tk.LEFT, padx=10)

btn_save = tk.Button(frame, text="💾 Ghi CSV", width=15, command=ghi_file)
btn_save.pack(side=tk.LEFT, padx=10)

# Ô hiển thị nội dung file
text = tk.Text(root, wrap=tk.NONE)
text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Thanh cuộn dọc
scroll = tk.Scrollbar(text, command=text.yview)
scroll.pack(side=tk.RIGHT, fill=tk.Y)
text.config(yscrollcommand=scroll.set)

root.mainloop()
