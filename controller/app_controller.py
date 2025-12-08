import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.calculations import calculate_expected_gold_to_2star, calculate_expected_gold, simulate_probability, calculate_upgrade_cost
from utils.language import load_language_data
from view.gui import TFTView
from model.data import DROP_RATES


class TFTController:
    def __init__(self, root):
        self.root = root
        self.language_data = load_language_data()
        self.language = "zh"  # 預設語言
        self.texts = self.language_data[self.language]
        self.view = TFTView(root, self)
        self.view.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.view.update_language(self.texts)  # 初始更新

    def switch_language(self):
        """切換語言並更新View"""
        self.language = "en" if self.language == "zh" else "zh"
        self.texts = self.language_data[self.language]
        self.view.update_language(self.texts)

    def calculate(self):
        """從View獲取輸入，呼叫Model計算，更新View"""
        try:
            cost = int(self.view.get_cost())
            owned = int(self.view.get_owned())
            outside = int(self.view.get_outside())
            outside_other = int(self.view.get_outside_other())
            level = int(self.view.get_level())
            money = int(self.view.get_money())
            xp_to_next = int(self.view.get_xp())

            if cost not in [1,2,3,4,5] or level not in DROP_RATES:
                raise ValueError("Invalid Input")

            # 計算到 2 星與 3 星的期望金幣
            exp_2star = calculate_expected_gold_to_2star(level, cost, owned, outside, outside_other)
            exp_3star = calculate_expected_gold(level, cost, owned, outside, outside_other)

            upgrade_cost = calculate_upgrade_cost(xp_to_next)
            exp_next = calculate_expected_gold(level + 1, cost, owned, outside, outside_other) if level < 10 else float('inf')

            total_if_upgrade = upgrade_cost + exp_next
            decision = self.texts.get("suggest_current", "Stay") if exp_3star < total_if_upgrade else self.texts.get("suggest_upgrade", "Upgrade")

            enough = self.texts.get("yes", "Yes") if money >= min(exp_3star, total_if_upgrade) else self.texts.get("no", "No")

            # 顯示結果
            result = (
                f"2★ {self.texts.get('suggest_current', 'Stay')}: {exp_2star}\n"
                f"3★ {self.texts.get('suggest_current', 'Stay')}: {exp_3star}\n"
                f"{self.texts.get('suggest_upgrade', 'Upgrade')}: {exp_next}\n"
                f"{self.texts.get('upgrade_cost', 'Upgrade Cost')}: {upgrade_cost}\n"
                f"{self.texts.get('decision', 'Decision')}: {decision}\n"
                f"{self.texts.get('money_status', 'Money Status')}: {money} {self.texts.get('gold', 'Gold')} {self.texts.get('enough', 'Enough')}: {enough}"
            )
            self.view.update_result(result)

            # 模擬並更新圖表
            gold_steps, prob_3star = simulate_probability(level, cost, owned, outside, outside_other, target_copies=9)
            _, prob_2star = simulate_probability(level, cost, owned, outside, outside_other, target_copies=3)
            self.view.update_chart(gold_steps, prob_3star, prob_2star, cost, level)

        except ValueError as e:
            self.view.update_result(f"{self.texts.get('error', 'Error')}: {e}")

    def on_closing(self):
        self.view.on_closing()