import os
from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai
import argparse

app = Flask(__name__)

# 直接設定API金鑰和模型
GEMINI_API_KEY = "AIzaSyCWTS7qIG7X4xnnHzPpYyu5Tu3Q0489VzY"
GEMINI_MODEL = "gemini-1.5-flash"

# 設定API金鑰
try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)
except Exception as e:
    print(f"初始化 Gemini 模型時發生錯誤: {str(e)}")
    raise

# HTML模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI聊天機器人</title>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .chat-container {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .message {
            margin: 10px 0;
            padding: 10px;
            border-radius: 5px;
        }
        .user-message {
            background-color: #e3f2fd;
            margin-left: 20%;
        }
        .ai-message {
            background-color: #f5f5f5;
            margin-right: 20%;
        }
        .input-container {
            margin-top: 20px;
            display: flex;
            gap: 10px;
        }
        input[type="text"] {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        button {
            padding: 10px 20px;
            background-color: #2196f3;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #1976d2;
        }
        #chat-messages {
            max-height: 500px;
            overflow-y: auto;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <h1>AI聊天機器人</h1>
        <div id="chat-messages">
            {% for message in messages %}
            <div class="message {% if message.role == 'user' %}user-message{% else %}ai-message{% endif %}">
                {{ message.content }}
            </div>
            {% endfor %}
        </div>
        <form id="chat-form" class="input-container">
            <input type="text" id="message-input" name="message" placeholder="請輸入您的問題" required>
            <button type="submit">發送</button>
        </form>
    </div>
    <script>
        document.getElementById('chat-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const messageInput = document.getElementById('message-input');
            const message = messageInput.value;
            
            // 添加使用者訊息
            const messagesDiv = document.getElementById('chat-messages');
            messagesDiv.innerHTML += `<div class="message user-message">${message}</div>`;
            messageInput.value = '';
            
            try {
                const response = await fetch('/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `message=${encodeURIComponent(message)}`
                });
                
                const data = await response.json();
                
                // 添加AI回應
                messagesDiv.innerHTML += `<div class="message ai-message">${data.ai_response}</div>`;
                
                // 滾動到最新訊息
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            } catch (error) {
                console.error('Error:', error);
                messagesDiv.innerHTML += `<div class="message ai-message">抱歉，發生錯誤。請稍後再試。</div>`;
            }
        });
    </script>
</body>
</html>
"""

def get_ai_response(prompt):
    """獲取AI回應的通用函數"""
    try:
        response = model.generate_content(prompt)
        if not response:
            return "抱歉，AI模型無法生成回應。請稍後再試。"
        if not hasattr(response, 'text'):
            return "抱歉，AI回應格式不正確。請稍後再試。"
        return response.text
    except Exception as e:
        print(f"AI回應錯誤: {str(e)}")  # 記錄錯誤
        return "抱歉，處理您的請求時發生錯誤。請稍後再試。"

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

@app.route('/', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        message = request.form.get('message', '')
        if message:
            response = get_ai_response(message)
            return jsonify({
                'user_message': message,
                'ai_response': response
            })
    return render_template_string(HTML_TEMPLATE, messages=[])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='AI聊天機器人')
    parser.add_argument('--mode', choices=['cli', 'web'], default='web',
                      help='選擇運行模式: cli (命令列介面) 或 web (網頁介面)')
    
    args = parser.parse_args()
    
    if args.mode == 'cli':
        cli_mode()
    else:
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080))) 