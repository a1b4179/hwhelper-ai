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

# Possible API endpoints (we'll try them in order)
CREWAI_ENDPOINTS = [
    f'https://api.crewai.com/v1/crews/{CREWAI_PROJECT_ID}/kickoff',
    f'https://api.crewai.com/crews/{CREWAI_PROJECT_ID}/kickoff',
    f'https://app.crewai.com/api/v1/projects/{CREWAI_PROJECT_ID}/kickoff',
    f'https://app.crewai.com/api/crews/{CREWAI_PROJECT_ID}/run',
    f'https://api.crewai.com/v1/projects/{CREWAI_PROJECT_ID}/run',
]

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

@app.route('/test-endpoints', methods=['GET'])
def test_endpoints():
    """Test all possible CrewAI endpoints to find which one works"""
    results = []
    
    headers = {
        'Authorization': f'Bearer {CREWAI_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    test_payload = {
        "inputs": {
            "topic": "test"
        }
    }
    
    for endpoint in CREWAI_ENDPOINTS:
        try:
            response = requests.post(endpoint, json=test_payload, headers=headers, timeout=10)
            results.append({
                'endpoint': endpoint,
                'status': response.status_code,
                'working': response.status_code in [200, 201, 202]
            })
        except Exception as e:
            results.append({
                'endpoint': endpoint,
                'status': 'error',
                'error': str(e)
            })
    
    return jsonify({
        'results': results,
        'instructions': 'Look for status 200, 201, or 202 to find the working endpoint'
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
        
        print("🤖 Trying CrewAI Cloud endpoints...")
        
        # Try each endpoint until one works
        last_error = None
        for endpoint in CREWAI_ENDPOINTS:
            try:
                print(f"Trying: {endpoint}")
                
                response = requests.post(
                    endpoint,
                    json=crewai_payload,
                    headers=headers,
                    timeout=300
                )
                
                print(f"Response: {response.status_code}")
                
                if response.status_code in [200, 201, 202]:
                    result = response.json()
                    
                    # Extract solution
                    if 'result' in result:
                        solution = result['result']
                    elif 'output' in result:
                        solution = result['output']
                    elif 'data' in result:
                        solution = str(result['data'])
                    else:
                        solution = str(result)
                    
                    print(f"✅ Success with endpoint: {endpoint}\n")
                    
                    return jsonify({
                        'success': True,
                        'solution': solution,
                        'endpoint_used': endpoint
                    }), 200
                
                last_error = f"Status {response.status_code}: {response.text}"
                
            except requests.exceptions.Timeout:
                last_error = "Request timeout"
                continue
            except Exception as e:
                last_error = str(e)
                continue
        
        # If we get here, none of the endpoints worked
        print(f"❌ All endpoints failed. Last error: {last_error}\n")
        
        return jsonify({
            'success': False,
            'error': f'Could not connect to CrewAI Cloud. Last error: {last_error}',
            'tried_endpoints': CREWAI_ENDPOINTS
        }), 502
        
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
