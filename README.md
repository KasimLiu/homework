# AI 智慧問答機器人

這是一個使用 Gemini AI 模型的智慧問答機器人，提供 Web 介面和 CLI 介面兩種使用方式。

## 功能特點

- 使用 Google Gemini AI 模型進行對話
- 提供 Streamlit Web 介面
- 提供命令行介面 (CLI)
- 支援環境變數配置

## 安裝需求

1. Python 3.8 或更高版本
2. 安裝所需套件：
   ```bash
   pip install -r requirements.txt
   ```

## 環境設定

1. 在專案根目錄建立一個 `.env` 檔案
2. 在 `.env` 檔案中設定您的 Gemini API 金鑰和模型名稱：
   ```
   GEMINI_API_KEY=your_api_key_here
   GEMINI_MODEL=gemini-1.5-flash
   ```

## 使用方式

### Web 介面

執行以下指令啟動 Web 介面：
```bash
streamlit run app.py
```
然後在瀏覽器中開啟 Streamlit 提供的 URL (通常是 http://localhost:8501)

### CLI 介面

執行以下指令啟動命令行介面：
```bash
python app.py --cli
```

## 注意事項

- 請確保您有有效的 Gemini API 金鑰並已在 `.env` 檔案中正確設定。
- CLI 模式提供簡單的命令行互動介面。
- 若要結束 Web 介面，請在執行 `streamlit run app.py` 的終端機中按下 `Ctrl + C`。 