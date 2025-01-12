import tkinter as tk
from tkinter import ttk
from models.types import Contest, Sheet_Contest, Selected_Mapping
from typing import List

def create_mapping_window(contest_data: List[Contest], sheet_contest: List[Sheet_Contest]) -> Selected_Mapping:
    """
    創建 UI 界面，讓使用者將比賽名稱映射到 Google Sheet 欄位。
    :param contest_data: 比賽資料列表，包含 contest_id 和 contest_name。
    :param sheet_contest: Google Sheet 欄位資料列表，包含 grid_name 和 col。
    :return: 使用者選擇的映射結果，鍵為欄位名稱，值為對應的比賽 ID 列表。
    """
    # 初始化主視窗
    root = tk.Tk()
    root.title("比賽與欄位映射")
    
    # 選擇的映射結果
    selected_mapping = {sheet['col']: [] for sheet in sheet_contest}
    
    def toggle_selection(row: int, col: int):
        """
        處理按鈕的點擊事件，用於選擇或取消比賽與欄位的映射。
        """
        contest_id = contest_data[row]['contest_id']
        sheet_col = sheet_contest[col]['col']
        button = buttons[row][col]
        
        if button.cget("bg") == "gray":  # 已選擇，取消
            button.config(bg="white")
            selected_mapping[sheet_col].remove(contest_id)
        else:  # 未選擇，添加
            button.config(bg="gray")
            selected_mapping[sheet_col].append(contest_id)
    
    # 動態生成表頭
    tk.Label(root, text="比賽名稱", borderwidth=1, relief="solid").grid(row=0, column=0, sticky="nsew")
    for col_idx, sheet in enumerate(sheet_contest, start=1):
        tk.Label(root, text=sheet['grid_name'], borderwidth=1, relief="solid").grid(row=0, column=col_idx, sticky="nsew")
    
    # 動態生成按鈕表格
    buttons = []
    for row_idx, contest in enumerate(contest_data, start=1):
        # 比賽名稱列
        tk.Label(root, text=contest['contest_name'], borderwidth=1, relief="solid").grid(row=row_idx, column=0, sticky="nsew")
        
        # 每個比賽的按鈕
        row_buttons = []
        for col_idx in range(len(sheet_contest)):
            btn = tk.Button(root, text="", bg="white", command=lambda r=row_idx-1, c=col_idx: toggle_selection(r, c))
            btn.grid(row=row_idx, column=col_idx+1, sticky="nsew")
            row_buttons.append(btn)
        buttons.append(row_buttons)
    
    # 提交按鈕
    def submit():
        root.destroy()
    
    tk.Button(root, text="提交", command=submit, bg="lightblue").grid(row=len(contest_data)+1, column=0, columnspan=len(sheet_contest)+1, sticky="nsew")
    
    # 動態調整格子大小
    for i in range(len(contest_data) + 2):
        root.grid_rowconfigure(i, weight=1)
    for j in range(len(sheet_contest) + 1):
        root.grid_columnconfigure(j, weight=1)
    
    # 啟動主事件迴圈
    root.mainloop()
    
    return selected_mapping

def create_selector_window(contests: List[Contest]) -> List[Contest]:
    def submit_selection():
        nonlocal selected_contests
        selected_indices = listbox.curselection()
        selected_contests = [contests[idx] for idx in selected_indices]
        root.destroy()

    # 創建主視窗
    root = tk.Tk()
    root.title("Contest Selector")
    root.geometry("500x400")
    selected_contests = []

    # 樣式設置
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel", font=("Helvetica", 14), padding=10)
    style.configure("TButton", font=("Helvetica", 12), padding=5)
    style.configure("TListbox", font=("Helvetica", 12), padding=5)

    # 標題
    title_label = ttk.Label(root, text="請選擇比賽：")
    title_label.pack(pady=10)

    # 創建帶滾動條的 Listbox
    frame = ttk.Frame(root)
    frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = tk.Listbox(frame, selectmode="extended", font=("Helvetica", 12), width=50, height=10, yscrollcommand=scrollbar.set)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=listbox.yview)

    # 填充 Listbox
    for contest in contests:
        listbox.insert(tk.END, contest['contest_name'])

    # 提交按鈕
    submit_button = ttk.Button(root, text="提交", command=submit_selection)
    submit_button.pack(pady=20)

    root.mainloop()
    return selected_contests