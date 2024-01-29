from flask import (Flask, Response, jsonify, abort, request)
from receipt_processing import generate_id, generate_points

app = Flask(__name__)

RECEIPTS = {}

@app.route('/')
def index() -> Response:
    return jsonify({'message': 'Hello, World!'})

@app.route('/receipts/process', methods=['POST'])
def process_receipts() -> Response:
    """
    This function will process receipts and return ID.
    """
    data = request.get_json()
    if not data:
        abort(400, description='No data provided.')

    response = generate_id(data)
    return jsonify(response)

@app.route('/receipts/<id>/points', methods=['GET'])
def points_awarded(id) -> Response:
    """
    This function will return the points awarded for a given receipt.
    """
    
    if not id:
        abort(400, description='Please provide an ID.')
    
    points = generate_points(id)
    
    return jsonify(points)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')