# TFT3StarCalc

## 中文版

### 項目簡介
**TFT3StarCalc** 是一個輕量且易於擴充的應用程式，幫助《雲頂之弈》（TFT）玩家計算達成三星棋子的最佳策略。輸入你當前擁有的棋子張數、場外張數、等級、金幣以及距離升級的 XP，應用程式會計算在當前等級或升級後達到三星所需的期望金幣，並提供是留在當前等級抽牌還是升級的策略建議。

#### 功能特點
- 顯示各費用階層（1-5 費）的棋子池總張數及各等級抽卡機率表。
- 根據輸入（擁有張數、場外張數、等級）計算三星的期望金幣。
- 根據金幣效率推薦抽牌或升級策略。
- 低耦合設計，便於維護和未來功能擴充。
- 使用 Python 和 Tkinter 構建，可編譯為 EXE 獨立運行。

#### 下載
[TFT 3星計算機](https://github.com/Lica3265/TFT3StarCalc/releases/download/Initial_release/TFT3StarCalc.exe)

*注意*：此可執行文件適用於 Windows。請確保你的系統有權限運行 `.exe` 文件。

#### 使用方法
1. **啟動應用程式**：運行已編譯的 EXE 文件。
2. **表格標籤頁**：查看各費用階層（1-5 費）棋子池大小及各等級抽卡機率。
3. **計算標籤頁**：
   - 輸入棋子費用（1-5）、擁有張數、場外張數、當前等級、當前金幣及距離升級的 XP。
   - 點擊「計算並繪圖」獲取：
     - 在當前等級達到三星的期望金幣。
     - 升級後達到三星的期望金幣。
     - 建議：是否在當前等級抽牌或先升級。
     - 判斷當前金幣是否足夠。
4. 根據結果優化你的D牌策略！

#### 未來計劃
- 增加蒙特卡羅模擬以提升期望金幣計算的準確性。
- 支援新 TFT 賽季，更新遊戲數據。
- 添加機率分佈的可視化。
- 支援更多語言的本地化。

#### 貢獻
歡迎貢獻！貢獻步驟：
1. Fork 該倉庫。
2. 創建新分支（`git checkout -b feature/your-feature`）。
3. 提交更改（`git commit -m '添加你的功能'`）。
4. 推送分支（`git push origin feature/your-feature`）。
5. 提交 Pull Request。

請通過 GitHub Issues 報告錯誤或建議新功能。

#### 授權
本項目採用 MIT 授權 - 詳見 [LICENSE](LICENSE) 文件。

#### 支援
如果覺得這個工具實用，請點擊 ⭐ **Star** 支持本項目！你的反饋有助於改進項目。

---

## English Version

### Project Overview
**TFT3StarCalc** is a lightweight and extensible app designed to help *Teamfight Tactics* (TFT) players calculate the optimal strategy for achieving 3-star champions. Input your current champion copies, outside copies, level, gold, and XP to next level, and the app computes the expected gold needed to hit 3 stars at your current level or after upgrading. It also provides strategic advice on whether to roll at your current level or upgrade first.

#### Features
- Displays total champion pool sizes and drop rates for each cost tier (1-5) across all levels.
- Calculates expected gold to 3-star based on owned copies, outside copies, and level.
- Recommends rolling or upgrading based on gold efficiency.
- Low-coupling design for easy maintenance and future expansion.
- Built with Python and Tkinter, compilable to a standalone EXE.

#### Downloads
The latest version of the executable (`.exe`) is available for download:
[TFT 3-Star Calculator (Windows)](https://github.com/Lica3265/TFT3StarCalc/releases/download/Initial_release/TFT3StarCalc.exe)

*Note*: This executable is built for Windows. Ensure you have the necessary permissions to run `.exe` files on your system.

#### Installation

##### Requirements
- Python 3.6+
- Tkinter (usually included with Python)
- PyInstaller (optional, for compiling to EXE)

##### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Lica3265/TFT3StarCalc.git
   ```
2. Navigate to the project directory:
   ```
   cd TFT3StarCalc
   ```


3. (Optional) Install PyInstaller to compile to EXE:
   ```
   pip install pyinstaller
   ```

3. Run the app:
   ```
   python tft_3star_calc.py
   ```
   4.(Optional) Compile to EXE:
   ```
   python -m PyInstaller --onefile --noconsole --add-data "languages.json;." --add-data "icon.ico;." --hidden-import=tkinter --hidden-import=matplotlib --hidden-import=matplotlib.pyplot --distpath="../TFT3StarCalcBuild" main.py
   ```

The compiled EXE will be in the TFT3StarCalcBuild/ folder.
### Usage

1. Launch the App: Run tft_3star_calc.py or the compiled EXE.
2. Table Tab: View the champion pool sizes and drop rates for each cost tier (1-5) across all levels.
3. Calculation Tab:

- Input the champion's cost (1-5), owned copies, outside copies, current level, current gold, and XP to next level.
- Click "Calculate" to get:

- Expected gold to 3-star at current level.
- Expected gold to 3-star after upgrading.
- Recommendation: roll at current level or upgrade first.
- Whether your current gold is sufficient.




4. Use the results to optimize your TFT economy!

#### Future Plans

1. Add Monte Carlo simulation for more accurate expected gold calculations.
2. Support for new TFT sets by updating game data.
3. Add visualization of probability distributions.
4. Localization for additional languages.

#### Contributing
Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (git checkout -b feature/your-feature).
3. Commit your changes (git commit -m 'Add your feature').
4. Push to the branch (git push origin feature/your-feature).
5. Open a Pull Request.

Please report bugs or suggest features via GitHub Issues.
#### License
This project is licensed under the MIT License - see the LICENSE file for details.
#### Support
If you find this tool helpful, please ⭐ star the repo to show your support! Your feedback helps improve the project.

![中文](assets/zh.png)
![英文](assets/en.png)