import os
import sys
import tkinter as tk
from tkinter import ttk
import math
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json

# 遊戲數據（根據你的指定，Set 15 2025年數據）
COST_TIERS = [1, 2, 3, 4, 5]
COPIES_PER_CHAMP = {1: 30, 2: 25, 3: 18, 4: 10, 5: 9}
NUM_CHAMPS_PER_TIER = {1: 15, 2: 13, 3: 12, 4: 13, 5: 8}

# 等級抽卡機率
DROP_RATES = {
    1: [1.00, 0.00, 0.00, 0.00, 0.00],
    2: [1.00, 0.00, 0.00, 0.00, 0.00],
    3: [0.75, 0.25, 0.00, 0.00, 0.00],
    4: [0.55, 0.30, 0.15, 0.00, 0.00],
    5: [0.45, 0.33, 0.20, 0.02, 0.00],
    6: [0.30, 0.40, 0.25, 0.05, 0.00],
    7: [0.19, 0.30, 0.40, 0.10, 0.01],
    8: [0.17, 0.24, 0.32, 0.24, 0.03],
    9: [0.15, 0.18, 0.25, 0.30, 0.12],
    10: [0.05, 0.10, 0.20, 0.40, 0.25],
}

XP_TO_NEXT = {
    1: 0, 2: 2, 3: 6, 4: 10, 5: 20, 6: 36, 7: 48, 8: 76, 9: 84, 10: 0,
}

# 資源路徑處理（用於 PyInstaller 打包）
def resource_path(relative_path):
    """獲取打包後的資源路徑"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# 載入語言數據
def load_language_data():
    """載入語言配置文件"""
    path = resource_path("languages.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# 計算每個費用階層的總張數
def get_total_copies_per_tier():
    """計算每個費用階層的總棋子張數"""
    return {cost: NUM_CHAMPS_PER_TIER[cost] * COPIES_PER_CHAMP[cost] for cost in COST_TIERS}

# 計算下一次抽到特定棋子的期望抽數
def expected_slots_to_next(remaining, tier_pool, p_tier):
    """計算下一次抽到特定棋子的期望抽數"""
    if remaining <= 0:
        return 0
    p_specific = p_tier * (remaining / tier_pool)
    return 1 / p_specific if p_specific > 0 else float('inf')

# 計算期望金幣數
def calculate_expected_gold(level, cost, owned, outside):
    """計算在當前等級抽到三星的期望金幣數"""
    if owned >= 9:
        return 0
    initial_copies = COPIES_PER_CHAMP[cost]
    remaining = initial_copies - owned - outside
    needed = 9 - owned
    if remaining < needed:
        return float('inf')

    num_champs = NUM_CHAMPS_PER_TIER[cost]
    full_tier_pool = num_champs * initial_copies
    current_tier_pool = full_tier_pool - (initial_copies - remaining)

    p_tier = DROP_RATES.get(level, [0] * 5)[cost - 1]

    expected_slots = 0
    for _ in range(needed):
        expected_slots += expected_slots_to_next(remaining, current_tier_pool, p_tier)
        remaining -= 1
        current_tier_pool -= 1

    slots_per_roll = 5
    expected_rolls = expected_slots / slots_per_roll
    gold_per_roll = 2
    return math.ceil(expected_rolls * gold_per_roll)

# 計算升級成本
def calculate_upgrade_cost(xp_to_next):
    """計算升級所需的金幣成本"""
    if xp_to_next <= 0:
        return 0
    buys_needed = math.ceil(xp_to_next / 4)
    return buys_needed * 4

# 模擬三星累積機率
def simulate_3star_probability(level, cost, owned, outside, max_gold=100, trials=1000):
    """使用 Monte Carlo 模擬計算三星累積機率"""
    initial_copies = COPIES_PER_CHAMP[cost]
    num_champs = NUM_CHAMPS_PER_TIER[cost]
    full_tier_pool = num_champs * initial_copies
    p_tier = DROP_RATES.get(level, [0] * 5)[cost - 1]

    gold_steps = list(range(0, max_gold + 1, 2))
    probabilities = []

    for gold in gold_steps:
        rolls = gold // 2
        slots = rolls * 5
        success = 0
        for _ in range(trials):
            current_owned = owned
            current_outside = outside
            current_pool = full_tier_pool - current_outside
            for _ in range(slots):
                if current_pool <= 0 or current_owned >= 9:
                    break
                p_specific = p_tier * ((initial_copies - current_owned - current_outside) / current_pool)
                if random.random() < p_specific:
                    current_owned += 1
                    current_pool -= 1
                else:
                    current_pool -= 1
                if current_owned >= 9:
                    success += 1
                    break
        probabilities.append(success / trials * 100)

    return gold_steps, probabilities

# 主應用類
class TFTApp:
    def __init__(self, root):
        """初始化應用"""
        self.root = root
        self.language_data = load_language_data()
        self.language = "zh"  # 預設語言
        self.texts = self.language_data[self.language]

        self.root.title(self.texts["title"])
        self.lang_btn = ttk.Button(root, text=self.texts["btn_switch"], command=self.switch_language)
        self.lang_btn.pack(pady=5)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        self.create_table_tab()

    def switch_language(self):
        """切換語言"""
        self.language = "en" if self.language == "zh" else "zh"
        self.texts = self.language_data[self.language]
        self.root.title(self.texts["title"])
        self.lang_btn.config(text=self.texts["btn_switch"])
        self.notebook.forget(0)
        self.create_table_tab()

    def create_table_tab(self):
        """創建計算結果標籤頁"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=self.texts["tab_result"])

        # 創建表格
        columns = [self.texts["table_cost"], self.texts["table_total"]] + \
                  [f"{self.texts['level_prefix']}{lvl}" for lvl in range(1, 11)]
        tree = ttk.Treeview(tab, columns=columns, show="headings", height=4)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=60 if "Lv" in col else 70, anchor="center")
        tree.column(columns[0], width=50, anchor="center")

        total_copies = get_total_copies_per_tier()
        for cost in COST_TIERS:
            row = [cost, total_copies[cost]]
            for lvl in range(1, 11):
                row.append(f"{DROP_RATES.get(lvl, [0] * 5)[cost - 1] * 100:.0f}%")
            tree.insert("", "end", values=row)

        tree.pack(fill="x", padx=10, pady=5)

        # 創建輸入框區域
        input_frame = ttk.LabelFrame(tab, text=self.texts["input_title"], padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(input_frame, text=self.texts["label_cost"]).grid(row=0, column=0, padx=5, pady=2)
        self.cost_entry = ttk.Entry(input_frame, width=10)
        self.cost_entry.grid(row=0, column=1, padx=5, pady=2)
        self.cost_entry.insert(0, "1")

        ttk.Label(input_frame, text=self.texts["label_owned"]).grid(row=0, column=2, padx=5, pady=2)
        self.owned_entry = ttk.Entry(input_frame, width=10)
        self.owned_entry.grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(input_frame, text=self.texts["label_outside"]).grid(row=1, column=0, padx=5, pady=2)
        self.outside_entry = ttk.Entry(input_frame, width=10)
        self.outside_entry.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(input_frame, text=self.texts["label_outside_othercopies"]).grid(row=1, column=2, padx=5, pady=2)
        self.outside_other_entry = ttk.Entry(input_frame, width=10)
        self.outside_other_entry.grid(row=1, column=3, padx=5, pady=2)

        ttk.Label(input_frame, text=self.texts["label_level"]).grid(row=2, column=0, padx=5, pady=2)
        self.level_entry = ttk.Entry(input_frame, width=10)
        self.level_entry.grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(input_frame, text=self.texts["label_money"]).grid(row=2, column=2, padx=5, pady=2)
        self.money_entry = ttk.Entry(input_frame, width=10)
        self.money_entry.grid(row=2, column=3, padx=5, pady=2)

        ttk.Label(input_frame, text=self.texts["label_xp"]).grid(row=3, column=0, padx=5, pady=2)
        self.xp_entry = ttk.Entry(input_frame, width=10)
        self.xp_entry.grid(row=3, column=1, padx=5, pady=2)

        calc_btn = ttk.Button(input_frame, text=self.texts["btn_calculate"], command=self.calculate)
        calc_btn.grid(row=4, column=0, columnspan=4, pady=10)

        # 創建結果區域
        self.result_frame = ttk.LabelFrame(tab, text=self.texts["result_title"], padding=10)
        self.result_frame.pack(fill="x", padx=10, pady=5)
        self.result_label = ttk.Label(self.result_frame, text="", justify="left", wraplength=400)
        self.result_label.pack(padx=5, pady=5)

        # 創建圖表區域
        self.chart_frame = ttk.LabelFrame(tab, text=self.texts["chart_title"], padding=10)
        self.chart_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.figure, self.ax = plt.subplots(figsize=(6, 3))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def calculate(self):
        """執行計算並更新顯示"""
        try:
            cost = int(self.cost_entry.get())
            owned = int(self.owned_entry.get())
            outside = int(self.outside_entry.get())
            level = int(self.level_entry.get())
            money = int(self.money_entry.get())
            xp_to_next = int(self.xp_entry.get())

            if cost not in COST_TIERS or level not in DROP_RATES:
                raise ValueError(self.texts["error"] + ": Invalid Input")

            exp_current = calculate_expected_gold(level, cost, owned, outside)
            upgrade_cost = calculate_upgrade_cost(xp_to_next)
            exp_next = calculate_expected_gold(level + 1, cost, owned, outside) if level < 10 else float('inf')

            total_if_upgrade = upgrade_cost + exp_next
            decision = self.texts["suggest_current"] if exp_current < total_if_upgrade else self.texts["suggest_upgrade"]

            enough = self.texts["yes"] if money >= min(exp_current, total_if_upgrade) else self.texts["no"]
            result = (
                f"{self.texts['suggest_current']}: {exp_current}\n"
                f"{self.texts['suggest_upgrade']}: {exp_next}\n"
                f"{self.texts['upgrade_cost']}: {upgrade_cost}\n"
                f"{self.texts['decision']}: {decision}\n"
                f"{self.texts['money_status']}: {money} {self.texts['gold']} {self.texts['enough']}: {enough}"
            )
            self.result_label.config(text=result)

            # 繪製圖表
            self.ax.clear()
            gold_steps, probabilities = simulate_3star_probability(level, cost, owned, outside)
            self.ax.plot(gold_steps, probabilities, marker="o", color="blue", linewidth=1.5)
            self.ax.set_xlabel(self.texts["chart_xlabel"])
            self.ax.set_ylabel(self.texts["chart_ylabel"])
            self.ax.set_title(f"{self.texts['chart_title']} (Cost {cost}, Level {level})")
            self.ax.grid(True, linestyle="--", alpha=0.7)
            self.ax.set_ylim(0, 100)
            self.canvas.draw()

        except ValueError as e:
            self.result_label.config(text=f"{self.texts['error']}: {e}")
            self.ax.clear()
            self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = TFTApp(root)
    root.mainloop()