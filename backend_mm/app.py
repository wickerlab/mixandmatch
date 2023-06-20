from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample route
@app.route('/')
def hello():
    return jsonify(message='Hello, Flask!')

# Sample POST route
@app.route('/data', methods=['POST'])
def process_data():
    data = request.get_json()
    # Process the data
    # ...
    return jsonify(status='success', message='Data processed successfully')

if __name__ == '__main__':
    app.run(debug=True)
