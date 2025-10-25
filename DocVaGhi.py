

import csv
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# --- HÀM ĐỌC FILE CSV ---
def doc_file_csv():
    filepath = filedialog.askopenfilename(
        title="Chọn file CSV để mở",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    if not filepath:
        return

    try:
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)

        if not rows:
            messagebox.showwarning("Thông báo", "File CSV rỗng.")
            return

        # Xóa dữ liệu cũ
        for col in tree.get_children():
            tree.delete(col)
        tree["columns"] = rows[0]
        tree["show"] = "headings"

        # Tạo tiêu đề cột
        for col in rows[0]:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        # Thêm dữ liệu vào bảng
        for row in rows[1:]:
            tree.insert("", tk.END, values=row)

        messagebox.showinfo("Thành công", f"Đã đọc file:\n{filepath}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể đọc file:\n{e}")

# --- HÀM GHI FILE CSV ---
def ghi_file_csv():
    filepath = filedialog.asksaveasfilename(
        title="Lưu file CSV mới",
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    if not filepath:
        return

    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Lấy tiêu đề cột
            columns = tree["columns"]
            writer.writerow(columns)

            # Lấy dữ liệu từ Treeview
            for item in tree.get_children():
                row = tree.item(item)["values"]
                writer.writerow(row)

        messagebox.showinfo("Thành công", f"Đã ghi file:\n{filepath}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể ghi file:\n{e}")

# --- GIAO DIỆN TKINTER ---
root = tk.Tk()
root.title("ỨNG DỤNG ĐỌC & GHI FILE CSV")
root.geometry("1000x600")

# Tiêu đề
label = tk.Label(root, text="ỨNG DỤNG ĐỌC & GHI FILE CSV", font=("Arial", 14, "bold"))
label.pack(pady=10)

# Nút chức năng
frame_btn = tk.Frame(root)
frame_btn.pack(pady=10)

btn_doc = tk.Button(frame_btn, text="📂 Đọc file CSV", width=20, command=doc_file_csv)
btn_doc.pack(side=tk.LEFT, padx=20)

btn_ghi = tk.Button(frame_btn, text="💾 Ghi ra file CSV mới", width=20, command=ghi_file_csv)
btn_ghi.pack(side=tk.LEFT, padx=20)

# Bảng hiển thị CSV
frame_table = tk.Frame(root)
frame_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Thanh cuộn
scrollbar_y = tk.Scrollbar(frame_table, orient=tk.VERTICAL)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

scrollbar_x = tk.Scrollbar(frame_table, orient=tk.HORIZONTAL)
scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

tree = ttk.Treeview(frame_table, yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
tree.pack(fill=tk.BOTH, expand=True)

scrollbar_y.config(command=tree.yview)
scrollbar_x.config(command=tree.xview)

root.mainloop()
