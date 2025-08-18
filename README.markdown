# TFT3StarCalc

A lightweight and extensible app to help *Teamfight Tactics* (TFT) players calculate the optimal strategy for achieving 3-star champions. Input your current champion copies, outside copies, level, gold, and XP to next level, and the app computes the expected gold needed to hit 3 stars at your current level or after upgrading. It also provides strategic advice on whether to roll at your current level or upgrade first.

---

## 項目簡介

**TFT3StarCalc** 是一個輕量且易於擴充的應用程式，幫助《雲頂之弈》（TFT）玩家計算達成三星棋子的最佳策略。輸入你當前擁有的棋子張數、場外張數、等級、金幣以及距離升級的 XP，應用程式會計算在當前等級或升級後達到三星所需的期望金幣，並提供是留在當前等級抽牌還是升級的策略建議。

**功能特點**：
- 顯示各費用階層（1-5 費）的棋子池總張數及各等級抽卡機率表。
- 根據輸入（擁有張數、場外張數、等級）計算三星的期望金幣。
- 根據金幣效率推薦抽牌或升級策略。
- 低耦合設計，便於維護和未來功能擴充。
- 使用 Python 和 Tkinter 構建，可編譯為 EXE 獨立運行。

**支持**：  
如果覺得這個工具實用，請點擊 ⭐ **Star** 支持本項目！歡迎貢獻代碼或提供反饋。

---

## Installation

### Requirements
- Python 3.6+
- Tkinter (usually included with Python)
- PyInstaller (optional, for compiling to EXE)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/TFT3StarCalc.git
   ```
2. Navigate to the project directory:
   ```bash
   cd TFT3StarCalc
   ```
3. (Optional) Install PyInstaller to compile to EXE:
   ```bash
   pip install pyinstaller
   ```
4. Run the app:
   ```bash
   python tft_3star_calc.py
   ```
5. (Optional) Compile to EXE:
   ```bash
   pyinstaller --onefile tft_3star_calc.py
   ```

The compiled EXE will be in the `dist/` folder.

---

## 使用方法

1. **Launch the App**: Run `tft_3star_calc.py` or the compiled EXE.
2. **Table Tab**: View the champion pool sizes and drop rates for each cost tier (1-5) across all levels.
3. **Calculation Tab**:
   - Input the champion's cost (1-5), owned copies, outside copies, current level, current gold, and XP to next level.
   - Click "Calculate" to get:
     - Expected gold to 3-star at current level.
     - Expected gold to 3-star after upgrading.
     - Recommendation: roll at current level or upgrade first.
     - Whether your current gold is sufficient.
4. Use the results to optimize your TFT economy!

---

## 未來計劃

- Add Monte Carlo simulation for more accurate expected gold calculations.
- Support for new TFT sets by updating game data.
- Add visualization of probability distributions.
- Localization for additional languages.

---

## 貢獻

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

Please report bugs or suggest features via GitHub Issues.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Support**: If you find this tool helpful, please ⭐ **star** the repo to show your support! Your feedback helps improve the project.