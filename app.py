from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import os
from openai import OpenAI
import json

app = Flask(__name__)

# 设置OpenAI API
os.environ['OPENAI_API_KEY'] = 'sk-iBPKKjivWouQB7uL3781E2AbB6B94608B5Ff96Cc1aD64578'
os.environ['OPENAI_API_BASE'] = "https://api.xty.app/v1"

# 预定义角色及其系统提示词
ROLES = {
    "concept_expert": {
        "name": "概念查詢專家",
        "name_en": "Concept Query Expert",
        "system_prompt": """你的任務是仿照原題目的問法，生成{K}個依舊能夠對應原答案的概念尋求查詢的題目。概念尋求查詢的定义：需要多個句子來回答的抽象問題。""",
        "default_count": 3
    },
    "keyword_expert": {
        "name": "關鍵詞查詢專家",
        "name_en": "Keyword Query Expert",
        "system_prompt": "你是一個專業的關鍵詞查詢專家，請根據提供的問答生成{K}個相關的關鍵詞查詢問題。",
        "default_count": 3
    },
    "fact_expert": {
        "name": "實事查詢專家",
        "name_en": "Factual Query Expert",
        "system_prompt": """你的任務是仿照原題目的問法，生成{K}個依舊能夠對應原答案的事實尋求查詢的題目。事實尋求查詢的定义：具有單一、明確答案的查詢。""",
        "default_count": 3
    },
    "spelling_expert": {
        "name": "拼寫錯誤查詢專家",
        "name_en": "Spelling Error Query Expert",
        "system_prompt": """你的任務是仿照原題目的問法，生成{K}個依舊能夠對應原答案的拼寫錯誤查詢的題目。拼寫錯誤查詢的定义：包含拼寫錯誤、換位和常見拼寫錯誤的查詢。""",
        "default_count": 3
    },
    "web_expert": {
        "name": "網頁查詢專家",
        "name_en": "Web Query Expert",
        "system_prompt": """你的任務是仿照原題目的問法，生成{K}個依舊能夠對應原答案的網頁搜索查詢的題目。網頁搜索查詢的定义：類似於通常輸入搜索引擎的簡短查詢轉換。""",
        "default_count": 3
    }
}

# 全局变量存储当前数据
current_data = None

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # 每页显示10条数据
    return render_template('index.html', roles=ROLES, per_page=per_page)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})
        
    if file and file.filename.endswith('.csv'):
        df = pd.read_csv(file)
        global current_data
        current_data = df
        total_pages = (len(df) + 9) // 10  # 计算总页数
        return jsonify({
            'success': True,
            'data': df.to_dict('records'),
            'total_pages': total_pages
        })
    
    return jsonify({'error': 'Invalid file type'})

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        row_index = data['rowIndex']
        role = data['role']
        count = data['count']
        prompt = data['prompt']
        
        # 获取原始问答内容
        row = current_data.iloc[row_index]
        
        # 调用OpenAI API生成新问题
        client = OpenAI(
            base_url="https://api.xty.app/v1",
            api_key=os.environ['OPENAI_API_KEY']
        )
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt.format(K=count)},
                {"role": "user", "content": f"原始问题:{row['題目']}\n原始答案:{row['解答']}"}
            ]
        )
        
        generated_questions = response.choices[0].message.content
        
        return jsonify({
            'success': True,
            'generated': generated_questions
        })
        
    except Exception as e:
        # 记录错误并返回友好的错误信息
        print(f"Error generating questions: {str(e)}")
        return jsonify({
            'success': False,
            'error': '生成问题时出错。可能是由于API访问限制，请检查您的API密钥和网络连接。'
        }), 500

@app.route('/export', methods=['POST'])
def export():
    data = request.json['data']
    df = pd.DataFrame(data)
    df.to_csv('generated_data.csv', index=False)
    return send_file('generated_data.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True) 