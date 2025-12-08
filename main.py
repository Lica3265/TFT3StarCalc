import os
import sys
import tkinter as tk
from tkinter import ttk
import math
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import matplotlib

# 遊戲數據（根據你的指定，Set 16 2025年數據 不計算需要解鎖的牌）
COST_TIERS = [1, 2, 3, 4, 5]
COPIES_PER_CHAMP = {1: 30, 2: 25, 3: 18, 4: 10, 5: 9}
# 常常會解鎖1~2張 先假設3張五費解鎖
NUM_CHAMPS_PER_TIER = {1: 15, 2: 14, 3: 16, 4: 14, 5: 7+3}

# 等級抽卡機率
DROP_RATES = {
    1: [1.00, 0.00, 0.00, 0.00, 0.00],
    2: [1.00, 0.00, 0.00, 0.00, 0.00],
    3: [0.75, 0.25, 0.00, 0.00, 0.00],
    4: [0.55, 0.30, 0.15, 0.00, 0.00],
    5: [0.45, 0.33, 0.20, 0.02, 0.00],
    6: [0.30, 0.40, 0.25, 0.05, 0.00],
    7: [0.19, 0.30, 0.40, 0.10, 0.01],
    8: [0.15, 0.20, 0.32, 0.30, 0.03],
    9: [0.10, 0.17, 0.25, 0.33, 0.15],
    10: [0.05, 0.10, 0.20, 0.40, 0.25],
}

XP_TO_NEXT = {
    1: 0, 2: 2, 3: 6, 4: 10, 5: 20, 6: 36, 7: 60, 8: 68, 9: 68, 10: 0,
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
        return float('inf')
    p_specific = p_tier * (remaining / tier_pool)
    return 1 / p_specific if p_specific > 0 else float('inf')

# 計算期望金幣數（支援不同目標張數）
def calculate_expected_gold(level, cost, owned, outside, outside_other=0, target_copies=9):
    """計算到指定張數的期望金幣數，預設目標為 9 張（3 星）"""
    if owned >= target_copies:
        return 0
    initial_copies = COPIES_PER_CHAMP[cost]
    remaining = max(0, initial_copies - owned - outside)
    needed = target_copies - owned
    if remaining < needed:
        return float('inf')

    num_champs = NUM_CHAMPS_PER_TIER[cost]
    full_tier_pool = num_champs * initial_copies
    current_tier_pool = max(0, full_tier_pool - outside - outside_other - owned)

    p_tier = DROP_RATES.get(level, [0]*5)[cost-1]

    expected_slots = 0
    for _ in range(needed):
        if remaining <= 0:
            return float('inf')
        p_specific = p_tier * (remaining / current_tier_pool) if current_tier_pool > 0 else 0
        expected_slots += 1 / p_specific if p_specific > 0 else float('inf')
        remaining -= 1
        current_tier_pool -= 1

    slots_per_roll = 5
    expected_rolls = expected_slots / slots_per_roll
    gold_per_roll = 2
    return math.ceil(expected_rolls * gold_per_roll)

# 計算到 2 星（3 張）的期望金幣
def calculate_expected_gold_to_2star(level, cost, owned, outside, outside_other=0):
    return calculate_expected_gold(level, cost, owned, outside, outside_other, target_copies=3)

# 計算升級成本
def calculate_upgrade_cost(xp_to_next):
    """計算升級所需的金幣成本"""
    if xp_to_next <= 0:
        return 0
    buys_needed = math.ceil(xp_to_next / 4)
    return buys_needed * 4

# 模擬到指定張數的累積機率
def simulate_probability(level, cost, owned, outside, outside_other=0, max_gold=100, trials=1000, target_copies=9):
    """使用 Monte Carlo 模擬計算到指定張數的累積機率，預設目標為 9 張（3 星）"""
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
            remaining = initial_copies - current_owned - current_outside
            current_pool = max(0, full_tier_pool - current_outside - outside_other)
            for _ in range(slots):
                if current_pool <= 0 or current_owned >= target_copies:
                    break
                if remaining <= 0:
                    break
                p_specific = p_tier * (remaining / current_pool) if current_pool > 0 else 0
                if random.random() < p_specific:
                    current_owned += 1
                    remaining -= 1
                    current_pool -= 1
                else:
                    current_pool -= 1
                if current_owned >= target_copies:
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
        matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Microsoft YaHei', 'SimHei', 'sans-serif']
        matplotlib.rcParams['axes.unicode_minus'] = False
        self.root.title(self.texts["title"])
        self.root.iconbitmap(default=resource_path("icon.ico"))
        self.lang_btn = ttk.Button(root, text=self.texts["btn_switch"], command=self.switch_language)
        self.lang_btn.pack(pady=5)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        self.create_input_tab()
        self.create_table_tab()

        # 綁定視窗關閉事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def switch_language(self):
        """切換語言"""
        self.language = "en" if self.language == "zh" else "zh"
        self.texts = self.language_data[self.language]
        self.root.title(self.texts["title"])
        self.lang_btn.config(text=self.texts["btn_switch"])

        for tab_id in self.notebook.tabs():
            self.notebook.forget(tab_id)
      
        self.create_input_tab()
        self.create_table_tab()

    def create_input_tab(self):
        """創建輸入與計算標籤頁"""
        tab1 = ttk.Frame(self.notebook)
        self.notebook.add(tab1, text=self.texts["tab_input"])

        # 創建輸入框區域
        input_frame = ttk.LabelFrame(tab1, text=self.texts["input_title"], padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(input_frame, text=self.texts["label_cost"]).grid(row=0, column=0, padx=5, pady=2)
        self.cost_entry = ttk.Entry(input_frame, width=10)
        self.cost_entry.grid(row=0, column=1, padx=5, pady=2)
        self.cost_entry.insert(0, "4")

        ttk.Label(input_frame, text=self.texts["label_owned"]).grid(row=0, column=2, padx=5, pady=2)
        self.owned_entry = ttk.Entry(input_frame, width=10)
        self.owned_entry.grid(row=0, column=3, padx=5, pady=2)
        self.owned_entry.insert(0, "7")

        ttk.Label(input_frame, text=self.texts["label_outside"]).grid(row=1, column=0, padx=5, pady=2)
        self.outside_entry = ttk.Entry(input_frame, width=10)
        self.outside_entry.grid(row=1, column=1, padx=5, pady=2)
        self.outside_entry.insert(0, "0")

        ttk.Label(input_frame, text=self.texts["label_outside_othercopies"]).grid(row=1, column=2, padx=5, pady=2)
        self.outside_other_entry = ttk.Entry(input_frame, width=10)
        self.outside_other_entry.grid(row=1, column=3, padx=5, pady=2)
        self.outside_other_entry.insert(0, "42")

        ttk.Label(input_frame, text=self.texts["label_level"]).grid(row=2, column=0, padx=5, pady=2)
        self.level_entry = ttk.Entry(input_frame, width=10)
        self.level_entry.grid(row=2, column=1, padx=5, pady=2)
        self.level_entry.insert(0, "8")

        ttk.Label(input_frame, text=self.texts["label_money"]).grid(row=2, column=2, padx=5, pady=2)
        self.money_entry = ttk.Entry(input_frame, width=10)
        self.money_entry.grid(row=2, column=3, padx=5, pady=2)
        self.money_entry.insert(0, "100")

        ttk.Label(input_frame, text=self.texts["label_xp"]).grid(row=3, column=0, padx=5, pady=2)
        self.xp_entry = ttk.Entry(input_frame, width=10)
        self.xp_entry.grid(row=3, column=1, padx=5, pady=2)
        self.xp_entry.insert(0, "20")

        calc_btn = ttk.Button(input_frame, text=self.texts["btn_calculate"], command=self.calculate)
        calc_btn.grid(row=4, column=0, columnspan=4, pady=10)

        # 創建結果區域
        self.result_frame = ttk.LabelFrame(tab1, text=self.texts["result_title"], padding=10)
        self.result_frame.pack(fill="x", padx=10, pady=5)
        self.result_label = ttk.Label(self.result_frame, text="", justify="left", wraplength=400)
        self.result_label.pack(padx=5, pady=5)

        # 創建圖表區域
        self.chart_frame = ttk.LabelFrame(tab1, text=self.texts["chart_title"], padding=10)
        self.chart_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.figure, self.ax = plt.subplots(figsize=(6, 3))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def create_table_tab(self):
        """創建概率與傷害計算標籤頁"""
        tab2 = ttk.Frame(self.notebook)
        self.notebook.add(tab2, text=self.texts["tab_table"])

        # 概率表格
        columns_prob = ["Level"] + [f"Cost {cost}" for cost in COST_TIERS]
        tree_prob = ttk.Treeview(tab2, columns=columns_prob, show="headings", height=10)
        for col in columns_prob:
            tree_prob.heading(col, text=col)
            tree_prob.column(col, width=50 if col == "Level" else 70, anchor="center")
        for lvl in range(1, 11):
            probabilities = [f"{DROP_RATES.get(lvl, [0] * 5)[cost - 1] * 100:.0f}%" for cost in COST_TIERS]
            tree_prob.insert("", "end", values=["Lv" + str(lvl)] + probabilities)
        tree_prob.pack(fill="x", padx=10, pady=5)

        # 階段傷害表格
        damage_data = {
            1: 0,
            2: 2,
            3: 6,
            4: 7,
            5: 10,
            6: 12,
            7: 17
        }
        columns_damage = ["Round", "Base Damage"]
        tree_damage = ttk.Treeview(tab2, columns=columns_damage, show="headings", height=7)
        for col in columns_damage:
            tree_damage.heading(col, text=col)
            tree_damage.column(col, width=100, anchor="center")
        cumulative = 0
        for round_num in range(1, 8):
            base_damage = damage_data.get(round_num, 17)  # 7+ 使用 17
            cumulative += base_damage
            tree_damage.insert("", "end", values=[f" Round {round_num}", f"+{base_damage} Damage"])
        tree_damage.pack(fill="x", padx=10, pady=10)

    def calculate(self):
        """執行計算並更新顯示"""
        try:
            cost = int(self.cost_entry.get())
            owned = int(self.owned_entry.get())
            outside = int(self.outside_entry.get())
            outside_other = int(self.outside_other_entry.get())
            level = int(self.level_entry.get())
            money = int(self.money_entry.get())
            xp_to_next = int(self.xp_entry.get())

            if cost not in COST_TIERS or level not in DROP_RATES:
                raise ValueError(self.texts["error"] + ": Invalid Input")

            # 計算到 2 星與 3 星的期望金幣
            exp_2star = calculate_expected_gold_to_2star(level, cost, owned, outside, outside_other)
            exp_3star = calculate_expected_gold(level, cost, owned, outside, outside_other)

            upgrade_cost = calculate_upgrade_cost(xp_to_next)
            exp_next = calculate_expected_gold(level + 1, cost, owned, outside, outside_other) if level < 10 else float('inf')

            total_if_upgrade = upgrade_cost + exp_next
            decision = self.texts["suggest_current"] if exp_3star < total_if_upgrade else self.texts["suggest_upgrade"]

            enough = self.texts["yes"] if money >= min(exp_3star, total_if_upgrade) else self.texts["no"]

            # 顯示結果：2星、3星
            result = (
                f"2★ {self.texts['suggest_current']}: {exp_2star}\n"
                f"3★ {self.texts['suggest_current']}: {exp_3star}\n"
                f"{self.texts['suggest_upgrade']}: {exp_next}\n"
                f"{self.texts['upgrade_cost']}: {upgrade_cost}\n"
                f"{self.texts['decision']}: {decision}\n"
                f"{self.texts['money_status']}: {money} {self.texts['gold']} {self.texts['enough']}: {enough}"
            )
            self.result_label.config(text=result)

            # 繪製圖表：兩條線（2星、3星）
            self.ax.clear()
            gold_steps, prob_3star = simulate_probability(level, cost, owned, outside, outside_other, target_copies=9)
            _, prob_2star = simulate_probability(level, cost, owned, outside, outside_other, target_copies=3)

            self.ax.plot(gold_steps, prob_3star, marker="o", color="blue", linewidth=1.5, label="3★")
            self.ax.plot(gold_steps, prob_2star, marker="s", color="green", linewidth=1.5, label="2★")

            self.ax.set_xlabel(self.texts["chart_xlabel"])
            self.ax.set_ylabel(self.texts["chart_ylabel"])
            self.ax.set_title(f"{self.texts['chart_title']} (Cost {cost}, Level {level})")
            self.ax.grid(True, linestyle="--", alpha=0.7)
            self.ax.set_ylim(0, 100)
            self.ax.legend()
            self.canvas.draw()

        except ValueError as e:
            self.result_label.config(text=f"{self.texts['error']}: {e}")
            self.ax.clear()
            self.canvas.draw()


    def on_closing(self):
        """處理視窗關閉事件，釋放資源"""
        # 釋放 Matplotlib 資源
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().pack_forget()  # 移除畫布
            plt.close(self.figure)  # 關閉圖形
            self.canvas = None
            self.figure = None
            self.ax = None

        # 銷毀根視窗
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TFTApp(root)
    root.mainloop()