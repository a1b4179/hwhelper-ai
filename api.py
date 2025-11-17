from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

app = Flask(__name__)

# CRITICAL: Enable CORS for all routes and all origins
CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': '🎓 Welcome to HWHelper API',
        'status': 'online',
        'endpoints': {
            'health': '/health',
            'test': '/test',
            'solve': '/solve (POST)'
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok', 
        'message': '🚀 HWHelper API is running with CORS enabled!',
        'version': '1.0'
    })

@app.route('/test', methods=['GET'])
def test():
    try:
        from smart_homework_learning_assistant.crew import SmartHomeworkLearningAssistantCrew
        return jsonify({
            'status': 'ok',
            'message': 'Crew imported successfully! ✅',
            'crew_available': True
        })
    except Exception as e:
        import traceback
        return jsonify({
            'status': 'error',
            'message': str(e),
            'traceback': traceback.format_exc(),
            'crew_available': False
        }), 500

@app.route('/solve', methods=['POST', 'OPTIONS'])
def solve_homework():
    # Handle preflight OPTIONS request
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
        
        print(f"\n{'='*70}")
        print(f"📝 NEW REQUEST")
        print(f"Subject: {subject}")
        print(f"Question: {question}")
        print(f"{'='*70}\n")
        
        # Import CrewAI
        from smart_homework_learning_assistant.crew import SmartHomeworkLearningAssistantCrew
        
        # Prepare topic
        topic = f"{subject}: {question}" if subject != 'General' else question
        
        inputs = {'topic': topic}
        
        print("🤖 Initializing CrewAI agents...")
        
        # Run the crew
        crew_instance = SmartHomeworkLearningAssistantCrew()
        result = crew_instance.crew().kickoff(inputs=inputs)
        
        # Convert result to string
        solution = str(result)
        
        print("✅ Solution generated successfully!")
        print(f"Length: {len(solution)} characters\n")
        
        return jsonify({
            'success': True,
            'solution': solution
        })
        
    except Exception as e:
        print(f"\n❌ ERROR OCCURRED:")
        print(f"Error: {str(e)}\n")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'success': False,
            'error': f"Server error: {str(e)}"
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    print("\n" + "="*70)
    print("🎓 HWHelper AI API Server")
    print("="*70)
    print(f"📍 Port: {port}")
    print(f"🌐 CORS: Enabled (all origins)")
    print(f"🤖 CrewAI: Ready")
    print("="*70 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=False)
