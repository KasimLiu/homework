from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from dotenv import load_dotenv
import google.generativeai as genai
import json

app = Flask(__name__, static_folder='static')
load_dotenv()

# 設置 Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# 檢查 API Key 是否存在
if not GEMINI_API_KEY:
    print("警告：找不到 GEMINI_API_KEY 環境變數。")

try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)
except Exception as e:
    print(f"警告：初始化 Gemini API 時發生錯誤：{str(e)}")

def get_ai_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"錯誤：生成回應時發生錯誤：{str(e)}")
        return f"抱歉，處理您的請求時發生錯誤。請稍後再試。"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')
    
    if not user_input:
        return jsonify({
            'error': '請輸入問題'
        }), 400
    
    try:
        response = get_ai_response(user_input)
        return jsonify({
            'response': response
        })
    except Exception as e:
        print(f"錯誤：處理聊天請求時發生錯誤：{str(e)}")
        return jsonify({
            'error': '處理您的請求時發生錯誤。請稍後再試。'
        }), 500

# 添加靜態文件路由
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# 添加健康檢查路由
@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"})

# 添加 404 處理
@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 