# AI聊天機器人

這是一個整合了Web介面和CLI介面的智慧問答機器人，使用Google的Gemini AI模型。

## 功能特點

- 支援Web介面（使用Streamlit）
- 支援CLI介面
- 使用Google Gemini AI模型
- 即時對話功能
- 聊天歷史記錄（Web模式）

## 安裝需求

1. Python 3.7+
2. 安裝依賴包：
```bash
pip install -r requirements.txt
```

## 使用方法

### Web模式（預設）

```bash
python ai_chatbot.py
```
或
```bash
python ai_chatbot.py --mode web
```

### CLI模式

```bash
python ai_chatbot.py --mode cli
```

## 注意事項

- 確保您有穩定的網路連接
- API金鑰已經設定在程式中
- 在CLI模式中，輸入 'quit' 或 'exit' 可以結束對話 