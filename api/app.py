import os
import streamlit as st
import google.generativeai as genai
import argparse

# 從環境變數獲取設定
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# 設定API金鑰
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(GEMINI_MODEL)

def get_ai_response(prompt):
    """獲取AI回應的通用函數"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"發生錯誤: {str(e)}"

def cli_mode():
    """CLI模式"""
    print("歡迎使用AI聊天機器人 (CLI模式)")
    print("輸入 'quit' 或 'exit' 結束對話")
    
    while True:
        user_input = input("\n您: ")
        if user_input.lower() in ['quit', 'exit']:
            print("謝謝使用，再見！")
            break
            
        response = get_ai_response(user_input)
        print(f"\nAI: {response}")

def web_mode():
    """Web模式 (Streamlit)"""
    st.title("AI聊天機器人")
    st.write("歡迎使用AI聊天機器人！")

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

        # 獲取AI回應
        with st.chat_message("assistant"):
            response = get_ai_response(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='AI聊天機器人')
    parser.add_argument('--mode', choices=['cli', 'web'], default='web',
                      help='選擇運行模式: cli (命令列介面) 或 web (網頁介面)')
    
    args = parser.parse_args()
    
    if args.mode == 'cli':
        cli_mode()
    else:
        web_mode() 