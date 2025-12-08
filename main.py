import sys
import os

# 強制設定路徑：動態得到根目錄（TFT3StarCalc/）
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(script_dir) if os.path.basename(script_dir) != 'TFT3StarCalc' else script_dir
sys.path.insert(0, root_dir)


# print(f"Root dir: {root_dir}")
# print(f"sys.path[0]: {sys.path[0]}")

import tkinter as tk
from controller.app_controller import TFTController
# S16 TFT 3-Star Calculator
# 資料數據
# model/data.py
# 資源路徑處理（用於 PyInstaller 打包）
# utils/resources.py
# 載入語言數據
# utils/language.py

# model/calculations.py

if __name__ == "__main__":
    root = tk.Tk()
    app = TFTController(root)
    root.mainloop()