import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Harvester Materials B2B API Server is Running!"

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json or {}
        user_name = data.get('name', 'Valued Customer')
        user_email = data.get('email', 'customer@example.com')
        license_type = data.get('license', 'Professional')
        
        # PDF 및 엑셀 파일 생성 실행
        os.system("python make_full_pdf.py")
        os.system("python make_excel_dataset.py")
        
        return jsonify({
            "status": "success",
            "message": f"Generated files for {user_name} ({user_email})"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
