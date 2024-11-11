from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure CORS
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://127.0.0.1:5000", "http://localhost:5000", "null"],
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Define the system message with Cristiana's information
SYSTEM_MESSAGE = """You are an AI assistant for Cristiana Principato's personal website. Here's the key information about Cristiana:

Background:
- Senior Data Scientist with Ph.D. in Experimental Physics
- 5+ years experience in data analytics and science
- Expert in developing predictive algorithms, ML models, and data visualization

Current Role (COMPASS PATHWAYS, Aug 2022 - Present):
- Develops AI solutions for mental health interventions
- Created 85% accurate depression treatment prediction model
- Led development of education-focused AI agent using ChatGPT API
- Implemented advanced speech recognition with 3% error rate

Previous Experience:
- MakerSights (Sep 2021 - Nov 2022): Led $1M+ price optimization project
- Smiths Digital Forge (Sep 2020 - Sep 2021): Developed 90% precise monitoring system
- Earlier role at MakerSights (Sep 2019 - May 2020)

Education:
- Ph.D. in High Energy Physics (University of Virginia, 2019)
- MS in Nuclear and Sub Nuclear Physics (University of Roma "Tor Vergata", 2014)
- Insight Data Science Fellowship (2019)

Skills:
- Machine Learning: NLP, LLMs, RAG, Anomaly Detection, Time Series, Bayesian Modeling
- Technologies: Python, SQL, PyTorch, MongoDB, PostgreSQL, AWS, Azure
- Data Science: Predictive Analytics, Advanced Statistics, A/B Testing, ETL

Answer questions about Cristiana professionally and concisely, focusing on her expertise in AI, data science, and machine learning."""

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        # Create the chat completion
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,  # Limit response length
            temperature=0.7  # Balance between creativity and consistency
        )

        # Extract the response text
        bot_response = response.choices[0].message.content

        return jsonify({'response': bot_response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)
