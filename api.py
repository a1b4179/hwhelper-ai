from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)

# Enable CORS
CORS(app, origins="*", allow_headers=["Content-Type"], methods=["GET", "POST", "OPTIONS"])

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

# CrewAI Cloud Configuration
CREWAI_TOKEN = os.environ.get('CREWAI_TOKEN', '796c01f5d0bb')
CREWAI_PROJECT_ID = '85c60404-7f80-4834-8683-f57e72137d2f'
CREWAI_API_URL = f'https://api.crewai.com/v1/projects/{CREWAI_PROJECT_ID}/kickoff'

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': '🎓 HWHelper API - Connected to CrewAI Cloud',
        'status': 'online',
        'crew': 'Smart Homework Assistant Pro V1'
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok', 
        'message': '🚀 API is running!',
        'crewai_cloud': 'connected'
    })

@app.route('/test', methods=['GET'])
def test():
    return jsonify({
        'status': 'ok',
        'message': 'API ready to call CrewAI Cloud!',
        'project_id': CREWAI_PROJECT_ID
    })

@app.route('/solve', methods=['POST', 'OPTIONS'])
def solve_homework():
    # Handle preflight
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        data = request.json
        subject = data.get('subject', 'General')
        question = data.get('question', '')
        
        if not question:
            return jsonify({
                'success': False,
                'error': 'No question provided'
            }), 400
        
        print(f"\n{'='*60}")
        print(f"📝 Request: {subject} - {question}")
        print(f"{'='*60}\n")
        
        # Prepare payload for CrewAI Cloud
        topic = f"{subject}: {question}" if subject != 'General' else question
        
        crewai_payload = {
            "inputs": {
                "topic": topic
            }
        }
        
        headers = {
            'Authorization': f'Bearer {CREWAI_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        print("🤖 Calling CrewAI Cloud...")
        print(f"URL: {CREWAI_API_URL}")
        
        # Call CrewAI Cloud API
        response = requests.post(
            CREWAI_API_URL,
            json=crewai_payload,
            headers=headers,
            timeout=300  # 5 minutes timeout
        )
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            # Extract the solution from CrewAI response
            # The exact structure depends on CrewAI's response format
            if 'result' in result:
                solution = result['result']
            elif 'output' in result:
                solution = result['output']
            elif 'data' in result:
                solution = str(result['data'])
            else:
                solution = str(result)
            
            print("✅ Solution received from CrewAI Cloud!\n")
            
            return jsonify({
                'success': True,
                'solution': solution
            }), 200
        else:
            error_msg = f"CrewAI Cloud error: {response.status_code}"
            try:
                error_detail = response.json()
                error_msg += f" - {error_detail}"
            except:
                error_msg += f" - {response.text}"
            
            print(f"❌ Error: {error_msg}\n")
            
            return jsonify({
                'success': False,
                'error': error_msg
            }), response.status_code
        
    except requests.exceptions.Timeout:
        print("❌ Request timeout\n")
        return jsonify({
            'success': False,
            'error': 'CrewAI Cloud request timed out. The AI agents might be taking too long.'
        }), 504
        
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"\n{'='*70}")
    print(f"🎓 HWHelper API - CrewAI Cloud Integration")
    print(f"{'='*70}")
    print(f"📍 Port: {port}")
    print(f"🌐 CrewAI Project: {CREWAI_PROJECT_ID}")
    print(f"🔑 Token: {CREWAI_TOKEN[:8]}...")
    print(f"{'='*70}\n")
    
    app.run(host='0.0.0.0', port=port, debug=False)
