from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

app = Flask(__name__)

# ENABLE CORS - CRITICAL!
CORS(app, origins="*", allow_headers=["Content-Type"], methods=["GET", "POST", "OPTIONS"])

# Add CORS headers to every response
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': '🎓 HWHelper API',
        'status': 'online',
        'cors': 'enabled'
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok', 
        'message': '🚀 API is running!',
        'cors': 'enabled'
    })

@app.route('/solve', methods=['POST', 'OPTIONS'])
def solve_homework():
    # Handle preflight
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        return response, 200
    
    try:
        data = request.json
        subject = data.get('subject', 'General')
        question = data.get('question', '')
        
        print(f"\n{'='*60}")
        print(f"📝 {subject}: {question}")
        print(f"{'='*60}\n")
        
        from smart_homework_learning_assistant.crew import SmartHomeworkLearningAssistantCrew
        
        topic = f"{subject}: {question}" if subject != 'General' else question
        inputs = {'topic': topic}
        
        print("🤖 Starting AI agents...")
        
        crew_instance = SmartHomeworkLearningAssistantCrew()
        result = crew_instance.crew().kickoff(inputs=inputs)
        
        solution = str(result)
        
        print("✅ Done!\n")
        
        return jsonify({
            'success': True,
            'solution': solution
        }), 200
        
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"\n🚀 HWHelper API on port {port}\n")
    app.run(host='0.0.0.0', port=port, debug=False)
