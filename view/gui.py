import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
from model.data import DROP_RATES, DAMAGE_DATA, COST_TIERS
from utils.resources import resource_path

matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Microsoft YaHei', 'SimHei', 'sans-serif']
matplotlib.rcParams['axes.unicode_minus'] = False

class TFTView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.texts = {}
        self.figure = None
        self.ax = None
        self.canvas = None
        self.notebook = None
        self.cost_entry = None
        self.owned_entry = None
        self.outside_entry = None
        self.outside_other_entry = None
        self.level_entry = None
        self.money_entry = None
        self.xp_entry = None
        self.result_label = None
        self.lang_btn = None
        self.setup_ui()

    def setup_ui(self):
        """創建基本UI框架"""
        self.root.title(self.texts.get("title", "TFT Calculator"))
        try:
            self.root.iconbitmap(default=resource_path("icon.ico"))
        except:
            pass  # 若無icon.ico，忽略

        # 語言按鈕（文字由update_language更新）
        self.lang_btn = ttk.Button(self.root, text=self.texts.get("btn_switch", "Switch Lang"), command=self.controller.switch_language)
        self.lang_btn.pack(pady=5)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

    def create_input_tab(self):
        """創建輸入與計算標籤頁"""
        tab1 = ttk.Frame(self.notebook)
        self.notebook.add(tab1, text=self.texts.get("tab_input", "Input"))

        # 創建輸入框區域
        input_frame = ttk.LabelFrame(tab1, text=self.texts.get("input_title", "Input"), padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(input_frame, text=self.texts.get("label_cost", "Cost")).grid(row=0, column=0, padx=5, pady=2)
        self.cost_entry = ttk.Entry(input_frame, width=10)
        self.cost_entry.grid(row=0, column=1, padx=5, pady=2)
        self.cost_entry.insert(0, "4")

        ttk.Label(input_frame, text=self.texts.get("label_owned", "Owned")).grid(row=0, column=2, padx=5, pady=2)
        self.owned_entry = ttk.Entry(input_frame, width=10)
        self.owned_entry.grid(row=0, column=3, padx=5, pady=2)
        self.owned_entry.insert(0, "7")

        ttk.Label(input_frame, text=self.texts.get("label_outside", "Outside")).grid(row=1, column=0, padx=5, pady=2)
        self.outside_entry = ttk.Entry(input_frame, width=10)
        self.outside_entry.grid(row=1, column=1, padx=5, pady=2)
        self.outside_entry.insert(0, "0")

        ttk.Label(input_frame, text=self.texts.get("label_outside_othercopies", "Outside Other")).grid(row=1, column=2, padx=5, pady=2)
        self.outside_other_entry = ttk.Entry(input_frame, width=10)
        self.outside_other_entry.grid(row=1, column=3, padx=5, pady=2)
        self.outside_other_entry.insert(0, "42")

        ttk.Label(input_frame, text=self.texts.get("label_level", "Level")).grid(row=2, column=0, padx=5, pady=2)
        self.level_entry = ttk.Entry(input_frame, width=10)
        self.level_entry.grid(row=2, column=1, padx=5, pady=2)
        self.level_entry.insert(0, "8")

        ttk.Label(input_frame, text=self.texts.get("label_money", "Money")).grid(row=2, column=2, padx=5, pady=2)
        self.money_entry = ttk.Entry(input_frame, width=10)
        self.money_entry.grid(row=2, column=3, padx=5, pady=2)
        self.money_entry.insert(0, "100")

        ttk.Label(input_frame, text=self.texts.get("label_xp", "XP")).grid(row=3, column=0, padx=5, pady=2)
        self.xp_entry = ttk.Entry(input_frame, width=10)
        self.xp_entry.grid(row=3, column=1, padx=5, pady=2)
        self.xp_entry.insert(0, "20")

        calc_btn = ttk.Button(input_frame, text=self.texts.get("btn_calculate", "Calculate"), command=self.controller.calculate)
        calc_btn.grid(row=4, column=0, columnspan=4, pady=10)

        # 創建結果區域
        self.result_frame = ttk.LabelFrame(tab1, text=self.texts.get("result_title", "Result"), padding=10)
        self.result_frame.pack(fill="x", padx=10, pady=5)
        self.result_label = ttk.Label(self.result_frame, text="", justify="left", wraplength=400)
        self.result_label.pack(padx=5, pady=5)

        # 創建圖表區域
        self.chart_frame = ttk.LabelFrame(tab1, text=self.texts.get("chart_title", "Chart"), padding=10)
        self.chart_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.figure, self.ax = plt.subplots(figsize=(6, 3))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def create_table_tab(self):
        """創建概率與傷害計算標籤頁"""
        tab2 = ttk.Frame(self.notebook)
        self.notebook.add(tab2, text=self.texts.get("tab_table", "Table"))

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
        columns_damage = ["Round", "Base Damage"]
        tree_damage = ttk.Treeview(tab2, columns=columns_damage, show="headings", height=7)
        for col in columns_damage:
            tree_damage.heading(col, text=col)
            tree_damage.column(col, width=100, anchor="center")
        cumulative = 0
        for round_num in range(1, 8):
            base_damage = DAMAGE_DATA.get(round_num, 17)  # 7+ 使用 17
            cumulative += base_damage
            tree_damage.insert("", "end", values=[f" Round {round_num}", f"+{base_damage} Damage"])
        tree_damage.pack(fill="x", padx=10, pady=10)

    # Getter 方法：供Controller獲取輸入
    def get_cost(self):
        return self.cost_entry.get()

    def get_owned(self):
        return self.owned_entry.get()

    def get_outside(self):
        return self.outside_entry.get()

    def get_outside_other(self):
        return self.outside_other_entry.get()

    def get_level(self):
        return self.level_entry.get()

    def get_money(self):
        return self.money_entry.get()

    def get_xp(self):
        return self.xp_entry.get()

    def update_language(self, texts):
        """更新語言：重建tabs以刷新文字"""
        self.texts = texts
        self.root.title(texts.get("title", "TFT Calculator"))
        self.lang_btn.config(text=texts.get("btn_switch", "Switch Lang"))

        # 清除現有tabs並重建
        for tab_id in self.notebook.tabs():
            self.notebook.forget(tab_id)

        self.create_input_tab()
        self.create_table_tab()

    def update_result(self, result_text):
        """更新結果標籤"""
        self.result_label.config(text=result_text)
        # 更新結果frame文字
        self.result_frame.config(text=self.texts.get("result_title", "Result"))

    def update_chart(self, gold_steps, prob_3star, prob_2star, cost, level):
        """更新圖表"""
        self.ax.clear()
        self.ax.plot(gold_steps, prob_3star, marker="o", color="blue", linewidth=1.5, label="3★")
        self.ax.plot(gold_steps, prob_2star, marker="s", color="green", linewidth=1.5, label="2★")
        self.ax.set_xlabel(self.texts.get("chart_xlabel", "Gold Spent"))
        self.ax.set_ylabel(self.texts.get("chart_ylabel", "Probability (%)"))
        self.ax.set_title(f"{self.texts.get('chart_title', 'Chart')} (Cost {cost}, Level {level})")
        self.ax.grid(True, linestyle="--", alpha=0.7)
        self.ax.set_ylim(0, 100)
        self.ax.legend()
        self.canvas.draw()
        # 更新chart frame文字
        self.chart_frame.config(text=f"{self.texts.get('chart_title', 'Chart')} (Cost {cost}, Level {level})")

    def on_closing(self):
        """處理視窗關閉事件，釋放資源"""
        if self.canvas:
            self.canvas.get_tk_widget().pack_forget()
            plt.close(self.figure)
        self.root.destroy()