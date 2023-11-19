from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/process_responses', methods=['POST'])
def process_user_responses():
    user_responses = request.json.get('user_responses', [])

    # Your existing logic to process user responses and generate recommendations
    # Replace the following with your actual logic
    gpt3_recommendation = "Your GPT-3 recommendation"
    perfume_recommendations = [{"Name": "Perfume 1", "Brand": "Brand 1"}, {"Name": "Perfume 2", "Brand": "Brand 2"}]

    response_data = {
        'gpt3_recommendation': gpt3_recommendation,
        'perfume_recommendations': perfume_recommendations
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
