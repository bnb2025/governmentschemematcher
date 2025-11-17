import os
from flask import Flask, request, jsonify
from agent import BigQueryAgent

app = Flask(__name__)

# Initialize the BigQueryAgent
try:
    bq_agent = BigQueryAgent()
except (ValueError, FileNotFoundError) as e:
    # If the agent fails to initialize, log the error and exit
    app.logger.error(f"Failed to initialize BigQueryAgent: {e}")
    # In a production environment, you might want to handle this more gracefully
    # For now, we'll let the application fail to start if the agent can't be created
    raise

@app.route('/query', methods=['POST'])
def query():
    """
    Handles POST requests to the /query endpoint.
    Expects a JSON payload with a "query" key.
    """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    query_text = data.get('query')

    if not query_text:
        return jsonify({"error": "Missing 'query' in request body"}), 400

    try:
        result = bq_agent.run(query_text)
        return jsonify({"result": result})
    except Exception as e:
        app.logger.error(f"Error processing query: {e}")
        return jsonify({"error": "An error occurred while processing your query."}), 500

if __name__ == '__main__':
    # This is for local development.
    # For production, use a WSGI server like Gunicorn.
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
