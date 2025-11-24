import csv
import random
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from avl_model import AVLTree

# ===================== GLOBAL =====================
avl = AVLTree()
root_node = None
columns = []
original_rows = []
primary_key_index = 0  # mặc định dùng cột đầu làm khóa chính

# ===================== OUTPUT =====================
def append_output(msg: str):
    output_text.config(state="normal")
    output_text.insert("end", msg + "\n")
    output_text.see("end")
    output_text.config(state="disabled")

def clear_output():
    output_text.config(state="normal")
    output_text.delete("1.0", "end")
    output_text.config(state="disabled")

# ===================== CSV =====================
def doc_file_csv(filepath, limit=None):
    global root_node, original_rows, primary_key_index
    root_node = None
    original_rows = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if not row:
                continue
            original_rows.append(row)

    nodes_inserted = 0
    for i, row in enumerate(original_rows):
        try:
            key_raw = row[primary_key_index]
        except IndexError:
            continue
        try:
            key = int(key_raw)
        except Exception:
            key = key_raw
        root_node = avl.insert(root_node, key, row)
        nodes_inserted += 1
        if limit and nodes_inserted >= limit:
            break

    append_output(f"✅ Đọc CSV thành công ({len(original_rows)} dòng, chèn {nodes_inserted} node vào cây)")
    hien_thi_du_lieu()
    update_canvas_levels()

def ghi_file_csv():
    if not columns:
        append_output("⚠️ Chưa có dữ liệu để ghi.")
        return
    file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if file:
        with open(file, 'w', newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            def traverse(r):
                if r:
                    traverse(r.left)
                    writer.writerow(r.row)
                    traverse(r.right)
            traverse(root_node)
        append_output(f"✅ Ghi CSV thành công: {file}")

def chon_khoa_chinh_popup():
    global primary_key_index
    pop = tk.Toplevel(win)
    pop.title("Chọn khóa chính")
    pop.geometry("320x160")
    tk.Label(pop, text="Chọn cột làm khóa chính:", font=("Arial", 12)).pack(pady=8)
    combo = ttk.Combobox(pop, values=columns, state="readonly")
    combo.pack(pady=5, padx=10, fill="x")
    combo.current(primary_key_index if 0 <= primary_key_index < len(columns) else 0)

    def ok():
        idx = combo.current()
        if idx >= 0:
            global primary_key_index
            primary_key_index = idx
            append_output(f"🔑 **Khóa chính được chọn: {columns[primary_key_index]}**")
        pop.destroy()

    tk.Button(pop, text="Xác nhận", bg="#C8E6C9", command=ok).pack(pady=8)

def mo_file_csv(limit=None):
    global columns
    filepath = filedialog.askopenfilename(title="Chọn file CSV", filetypes=[("CSV Files", "*.csv")])
    if not filepath:
        return
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        columns[:] = next(reader)
    tree_table["columns"] = columns
    tree_table["show"] = "headings"
    for col in columns:
        tree_table.heading(col, text=col)
        tree_table.column(col, width=120, anchor="center")

    chon_khoa_chinh_popup()
    doc_file_csv(filepath, limit)
    append_output(f"📂 Đã mở file: {filepath}")

def mo_file_10node():
    global root_node, original_rows, primary_key_index
    if not original_rows:
        append_output("⚠️ Vui lòng mở file CSV trước khi đọc 10 node ngẫu nhiên.")
        return
    sample_rows = original_rows if len(original_rows) <= 10 else random.sample(original_rows, 10)
    root_node = None
    nodes_inserted = 0
    for row in sample_rows:
        try:
            key_raw = row[primary_key_index]
        except IndexError:
            continue
        try:
            key = int(key_raw)
        except Exception:
            key = key_raw
        root_node = avl.insert(root_node, key, row)
        nodes_inserted += 1

    tree_table.delete(*tree_table.get_children())
    for r in sample_rows:
        tree_table.insert("", "end", values=r)

    update_canvas_levels()
    append_output(f"🎲 Đã lấy ngẫu nhiên 10 node và chèn {nodes_inserted} node vào cây & hiển thị trên bảng.")

# ===================== TREE =====================
def traverse_tree(r, rows=None):
    if rows is None:
        rows = []
    if r:
        traverse_tree(r.left, rows)
        rows.append(r.row)
        traverse_tree(r.right, rows)
    return rows

def hien_thi_du_lieu():
    tree_table.delete(*tree_table.get_children())
    if root_node:
        for r in traverse_tree(root_node):
            tree_table.insert("", "end", values=r)

# ===================== HIỂN THỊ CÂY THEO TẦNG K =====================
def update_canvas_levels():
    canvas.delete("all")
    if not root_node:
        canvas.create_text(600, 100, text="🌱 Cây rỗng", font=("Arial", 13))
        return

    try:
        k = int(level_entry.get())
        if k <= 0:
            raise ValueError
    except Exception:
        canvas.create_text(600, 100, text="⚠️ Nhập tầng hợp lệ (>=1)", font=("Arial", 13, "bold"), fill="red")
        return

    def get_level_nodes(root, level):
        if not root:
            return []
        if level == 1:
            return [root]
        return get_level_nodes(root.left, level - 1) + get_level_nodes(root.right, level - 1)

    level_nodes = get_level_nodes(root_node, k)
    if not level_nodes:
        canvas.create_text(600, 100, text=f"❌ Không có node ở tầng {k}", font=("Arial", 13, "bold"), fill="red")
        return

    width = max(int(canvas["width"]), 1200)
    node_r = 25
    y = 150
    n = len(level_nodes)
    gap = max(60, min(150, width // max(1, n + 1)))
    total_width = (n - 1) * gap
    start_x = max(60, (width - total_width) // 2)

    for i, node in enumerate(level_nodes):
        x = start_x + i * gap
        canvas.create_oval(x - node_r, y - node_r, x + node_r, y + node_r, fill="#CDE8E5", outline="black")
        # dùng khóa chính để hiển thị
        canvas.create_text(x, y, text=str(node.row[primary_key_index]), font=("Arial", 10, "bold"))

    canvas.create_text(width // 2, 40, text=f"🌿 Các node ở tầng {k}", font=("Arial", 14, "bold"), fill="#333")
    canvas.config(scrollregion=canvas.bbox("all"))

# ===================== TREE OPERATIONS =====================
def duyet_LNR(): _duyet(avl.inorder, "LNR")
def duyet_NLR(): _duyet(avl.preorder, "NLR")
def duyet_LRN(): _duyet(avl.postorder, "LRN")
def _duyet(func, name):
    if not root_node:
        append_output("⚠️ Cây rỗng.")
        return
    res = []
    func(root_node, res)
    append_output(f"📘 Duyệt {name}: {', '.join(res)}")

def dem_chieu_cao():
    append_output(f"🌳 Chiều cao cây: {avl.get_height(root_node) if root_node else 0}")

def dem_node():
    def count(r): return 0 if not r else 1 + count(r.left) + count(r.right)
    append_output(f"🔢 Tổng số node: {count(root_node)}")

def dem_node_la():
    append_output(f"🍃 Số node lá: {avl.count_leaves(root_node)}")

def giai_phong_cay():
    global root_node
    root_node = None
    hien_thi_du_lieu()
    update_canvas_levels()
    append_output("♻️ Cây đã được giải phóng.")

# ===================== POPUP =====================
def them_node_popup():
    global root_node, primary_key_index
    if not columns:
        messagebox.showwarning("⚠️", "Chưa có cột dữ liệu, mở CSV trước!")
        return
    popup = tk.Toplevel(win)
    popup.title("Thêm Node mới")
    popup.geometry("400x400")
    tk.Label(popup, text="Nhập thông tin node mới:", font=("Arial", 12, "bold")).pack(pady=5)

    frame = tk.Frame(popup)
    frame.pack(fill="both", expand=True, padx=5, pady=5)
    canvas_inner = tk.Canvas(frame)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas_inner.yview)
    scrollable_frame = tk.Frame(canvas_inner)
    scrollable_frame.bind("<Configure>", lambda e: canvas_inner.configure(scrollregion=canvas_inner.bbox("all")))
    canvas_inner.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas_inner.configure(yscrollcommand=scrollbar.set)
    canvas_inner.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    entries = {}
    for col in columns:
        row_frame = tk.Frame(scrollable_frame)
        row_frame.pack(fill="x", pady=2)
        tk.Label(row_frame, text=col, width=15, anchor="w").pack(side="left")
        ent = tk.Entry(row_frame)
        ent.pack(side="right", fill="x", expand=True)
        entries[col] = ent

    def add_node():
        global root_node, primary_key_index
        key_raw = entries[columns[primary_key_index]].get()
        try:
            key = int(key_raw)
        except Exception:
            key = key_raw
        if avl.search(root_node, key):
            messagebox.showwarning("⚠️", f"Node với khóa {key} đã tồn tại!")
            return
        row = [entries[col].get() for col in columns]
        root_node = avl.insert(root_node, key, row)
        hien_thi_du_lieu()
        update_canvas_levels()
        append_output(f"➕ Node với khóa={key} đã thêm")
        popup.destroy()

    tk.Button(popup, text="Thêm node", bg="#C8E6C9", command=add_node).pack(pady=5)

def xoa_node_popup():
    global root_node
    if not columns:
        append_output("⚠️ Chưa có dữ liệu để xóa node.")
        return
    id_del = simpledialog.askstring("Xóa node", f"Nhập giá trị khóa ({columns[primary_key_index] if columns else 'key'}):")
    if not id_del:
        return
    try:
        key = int(id_del)
    except Exception:
        key = id_del
    if avl.search(root_node, key):
        root_node = avl.delete(root_node, key)
        hien_thi_du_lieu()
        update_canvas_levels()
        append_output(f"➖ Node {key} đã xóa")
    else:
        append_output(f"⚠️ Node {key} không tồn tại")

def tim_node_popup():
    if not columns:
        append_output("⚠️ Chưa có dữ liệu để tìm node.")
        return
    id_find = simpledialog.askstring("Tìm node", f"Nhập giá trị khóa ({columns[primary_key_index] if columns else 'key'}):")
    if not id_find:
        return
    try:
        key = int(id_find)
    except Exception:
        key = id_find
    node = avl.search(root_node, key)
    result_win = tk.Toplevel(win)
    result_win.title(f"Tìm {key}")
    result_win.geometry("400x250")
    tree = ttk.Treeview(result_win, columns=columns, show="headings")
    tree.pack(fill="both", expand=True, padx=5, pady=5)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")
    if node:
        tk.Label(result_win, text=f"✅ Node {key} tìm thấy", font=("Arial", 12, "bold")).pack(pady=5)
        tree.insert("", "end", values=node.row)
        append_output(f"🔍 Node {key}: {node.row}")
    else:
        tk.Label(result_win, text=f"❌ Node {key} không tồn tại", font=("Arial", 12, "bold"), fg="red").pack(pady=20)
        append_output(f"⚠️ Node {key} không tồn tại")

# ===================== GUI =====================
win = tk.Tk()
win.title("🌿 AVL TREE 🌿")
win.geometry("1350x950")
win.config(bg="#f9f9f7")

tk.Label(win, text="🌿 AVL TREE 🌿", font=("Arial", 16, "bold"), bg="#f9f9f7").pack(pady=8)

notebook = ttk.Notebook(win)
notebook.pack(fill="both", expand=True, padx=8, pady=4)

tab1 = tk.Frame(notebook, bg="#f9f9f7")
notebook.add(tab1, text="📂 Dataset")
frame_top = tk.Frame(tab1, bg="#f9f9f7"); frame_top.pack(fill="x", padx=8, pady=4)

btn_cfg = [
    ("Đọc CSV", mo_file_csv, "#BBDEFB"),
    ("Ghi CSV", ghi_file_csv, "#E8F5E9"),
    ("Thêm node", them_node_popup, "#C8E6C9"),
    ("Xóa node", xoa_node_popup, "#FFCDD2"),
    ("Tìm kiếm", tim_node_popup, "#FFE082"),
]
for text, cmd, color in btn_cfg:
    tk.Button(frame_top, text=text, bg=color, width=14, command=cmd).pack(side="left", padx=3)

scroll_y = tk.Scrollbar(tab1, orient=tk.VERTICAL)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
tree_table = ttk.Treeview(tab1, yscrollcommand=scroll_y.set, height=20)
tree_table.pack(fill="both", expand=True)
scroll_y.config(command=tree_table.yview)

tab2 = tk.Frame(notebook, bg="#f9f9f7")
notebook.add(tab2, text="Cây + Kết quả")

control_frame = tk.Frame(tab2, bg="#f9f9f7"); control_frame.pack(fill="x", pady=4)
tk.Label(control_frame, text="Số tầng hiển thị:", bg="#f9f9f7").pack(side="left", padx=5)
level_entry = tk.Entry(control_frame, width=10); level_entry.pack(side="left")
btn_cfg2 = [
    ("Hiển thị", update_canvas_levels, "#C8E6C9"),
    ("Duyệt LNR", duyet_LNR, "#FFE082"),
    ("Duyệt NLR", duyet_NLR, "#FFE082"),
    ("Duyệt LRN", duyet_LRN, "#FFE082"),
    ("Chiều cao", dem_chieu_cao, "#E8F5E9"),
    ("Đếm node", dem_node, "#E8F5E9"),
    ("Đếm nút lá", dem_node_la, "#C8E6C9"),
    ("Giải phóng cây", giai_phong_cay, "#FFCDD2"),
    ("Xóa output", clear_output, "#FFCDD2"),
    ("Đọc 10 node", mo_file_10node, "#BBDEFB"),
]
for text, cmd, color in btn_cfg2:
    tk.Button(control_frame, text=text, bg=color, command=cmd).pack(side="left", padx=5)

canvas_frame = tk.Frame(tab2); canvas_frame.pack(fill="both", expand=True)
canvas_x = tk.Scrollbar(canvas_frame, orient="horizontal"); canvas_x.pack(side="bottom", fill="x")
canvas_y = tk.Scrollbar(canvas_frame, orient="vertical"); canvas_y.pack(side="right", fill="y")
canvas = tk.Canvas(canvas_frame, width=1200, height=350, bg="#fff",
                   xscrollcommand=canvas_x.set, yscrollcommand=canvas_y.set)
canvas.pack(fill="both", expand=True)
canvas_x.config(command=canvas.xview); canvas_y.config(command=canvas.yview)

out_frame = tk.Frame(tab2, bg="#EDE7D9"); out_frame.pack(fill="both", expand=True, padx=8, pady=6)
output_text = tk.Text(out_frame, height=20, bg="#FFF8E1", font=("Consolas", 12),
                      state="disabled", relief="solid", bd=2)
output_text.pack(fill="both", expand=True, padx=10, pady=6, side="left")
scroll_y_out = tk.Scrollbar(out_frame, orient="vertical", command=output_text.yview)
scroll_y_out.pack(side="right", fill="y")
scroll_x_out = tk.Scrollbar(out_frame, orient="horizontal", command=output_text.xview)
scroll_x_out.pack(side="bottom", fill="x")
output_text.config(yscrollcommand=scroll_y_out.set, xscrollcommand=scroll_x_out.set, wrap="none")

append_output("Chương trình sẵn sàng. Hãy đọc CSV để khởi tạo cây.")
win.mainloop()



