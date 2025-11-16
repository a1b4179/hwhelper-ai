from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add src to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, 'src'))

app = Flask(__name__)
CORS(app)

@app.route('/solve', methods=['POST'])
def solve_homework():
    try:
        data = request.json
        subject = data.get('subject', '')
        question = data.get('question', '')
        
        print(f"\n{'='*60}")
        print(f"📝 New Homework Request!")
        print(f"Subject: {subject}")
        print(f"Question: {question}")
        print(f"{'='*60}\n")
        
        # Import your crew
        from smart_homework_learning_assistant.crew import SmartHomeworkLearningAssistantCrew
        
        # Create the topic string combining subject and question
        topic = f"{subject}: {question}" if subject else question
        
        # Prepare inputs
        inputs = {
            'topic': topic
        }
        
        print("🤖 Initializing AI agents...")
        print("⚙️ Starting research, video curation, and solution generation...")
        
        # Run the crew
        crew_instance = SmartHomeworkLearningAssistantCrew()
        result = crew_instance.crew().kickoff(inputs=inputs)
        
        # Convert result to string
        solution = str(result)
        
        print("\n✅ Solution generated successfully!")
        print(f"Solution length: {len(solution)} characters\n")
        
        return jsonify({
            'success': True,
            'solution': solution
        })
        
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}\n")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'success': False,
            'error': f"Error: {str(e)}. Make sure you have set up your OpenAI API key!"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok', 
        'message': '🚀 HWHelper API is running!',
        'version': '1.0'
    })

@app.route('/test', methods=['GET'])
def test():
    """Test endpoint to verify crew import"""
    try:
        from smart_homework_learning_assistant.crew import SmartHomeworkLearningAssistantCrew
        return jsonify({
            'status': 'ok',
            'message': 'Crew imported successfully! ✅',
            'crew_available': True
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'crew_available': False
        }), 500

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🎓 HWHelper - Smart Homework Learning Assistant API")
    print("="*70)
    print("📍 API URL: http://localhost:5000")
    print("🏥 Health Check: http://localhost:5000/health")
    print("🧪 Test Crew: http://localhost:5000/test")
    print("💡 Solve Endpoint: http://localhost:5000/solve (POST)")
    print("="*70)
    print("\n⚠️  IMPORTANT: Make sure your OpenAI API key is set!")
    print("💡 Set it with: export OPENAI_API_KEY='your-key-here' (Mac/Linux)")
    print("💡 Or: set OPENAI_API_KEY=your-key-here (Windows)")
    print("\n⏳ Starting server...\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)