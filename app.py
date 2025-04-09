import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import argparse

# 載入環境變數
load_dotenv()

# 設定 Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")

# 檢查 API Key 是否存在
if not GEMINI_API_KEY:
    st.error("錯誤：找不到 GEMINI_API_KEY 環境變數。請在 .env 檔案中設定。")
    exit()
if not GEMINI_MODEL:
    st.warning("警告：找不到 GEMINI_MODEL 環境變數。將使用預設模型 'gemini-1.5-flash'。")
    GEMINI_MODEL = "gemini-1.5-flash" # 提供預設值

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(GEMINI_MODEL)

def get_ai_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"錯誤：{str(e)}"

# Streamlit 介面 (現在是主要函數)
def main_streamlit():
    st.title("AI 智慧問答機器人")
    st.write("歡迎使用 AI 智慧問答系統！")

    # 初始化聊天歷史
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 顯示聊天歷史
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 使用者輸入
    if prompt := st.chat_input("請輸入您的問題"):
        # 添加使用者訊息到歷史
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 獲取 AI 回應
        with st.chat_message("assistant"):
            response = get_ai_response(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# CLI 介面
def cli_interface():
    print("歡迎使用 AI 智慧問答系統 (CLI 模式)")
    print("輸入 'quit' 或 'exit' 結束對話")
    
    while True:
        user_input = input("\n請輸入您的問題: ")
        if user_input.lower() in ['quit', 'exit']:
            print("感謝使用，再見！")
            break
        
        response = get_ai_response(user_input)
        print("\nAI 回應:", response)

if __name__ == "__main__":
    # 使用 argparse 處理命令行參數
    parser = argparse.ArgumentParser(description="AI 智慧問答機器人")
    parser.add_argument("--cli", action="store_true", help="以 CLI 模式運行")
    args = parser.parse_args()

    if args.cli:
        # CLI 模式
        cli_interface()
    else:
        # Streamlit 模式 (不再從腳本內啟動，由 streamlit run 啟動)
        main_streamlit() 