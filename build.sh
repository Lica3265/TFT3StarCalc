#!/bin/bash

# build.sh: PyInstaller 打包 TFT Calculator 成單一 EXE
# 使用前：確保在 tft_calculator/ 專案根目錄執行
# 依賴：Python 3.x, pip 已安裝 PyInstaller (腳本會自動檢查/安裝)
# 輸出：dist/ 資料夾下的 tft_calculator.exe (Windows) 或 tft_calculator (Mac/Linux)



echo "=== TFT Calculator 打包腳本 ==="
echo "專案根目錄: $(pwd)"
echo "入口檔案: main.py"

# 步驟1: 檢查並安裝 PyInstaller
if ! command -v PyInstaller &> /dev/null; then
    echo "PyInstaller 未安裝，正在安裝..."
    python -m pip install PyInstaller
else
    echo "PyInstaller 已安裝。"
fi
# 步驟2: 清理舊檔案
rm -rf dist/

# 步驟3: 執行 PyInstaller
echo "開始打包... (這可能需要幾分鐘)"
python -m PyInstaller TFT3StarCalc.spec

# 步驟4: 完成提示
if [ -f "dist/TFT3StarCalc.exe" ] || [ -f "dist/TFT3StarCalc" ]; then
    echo "打包成功！"
    echo "EXE 位置: ./dist/TFT3StarCalc.exe (Windows) 或 ./dist/TFT3StarCalc (其他)"
    echo "測試: 運行 dist/TFT3StarCalc.exe"
else
    echo "打包失敗，請檢查錯誤訊息。"
    read -n 1 -s -p "Press any key to continue..."
    echo
fi

echo "=== 打包完成 ==="
read -n 1 -s -p "Press any key to continue..."
echo
