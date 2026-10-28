from flask import Flask, request, jsonify

app = Flask(__name__)

# --- HELPER PARSING FUNCTIONS ---

def validate_sum_payload(data) -> tuple[bool, str, list]:
    """
    Validates the POST /sum payload constraints and handles structural edge cases.
    Returns (is_valid, error_message, numbers_list).
    """
    # Edge Case: Verify the payload root is a dictionary object
    if not isinstance(data, dict):
        return False, "Payload must be a valid JSON object structure.", []
        
    # Edge Case: Check for the required 'numbers' key
    if "numbers" not in data:
        return False, "Missing required key: 'numbers'.", []
        
    numbers_list = data["numbers"]
    
    # Edge Case: Handle situation where 'numbers' is not a list
    if not isinstance(numbers_list, list):
        return False, "The value of 'numbers' must be a list format.", []
        
    # Edge Case: Allow empty lists cleanly (sum of an empty list is 0)
    if len(numbers_list) == 0:
        return True, "Valid", []
        
    # Edge Case: Verify every item inside the list is an integer or float
    for index, val in enumerate(numbers_list):
        if isinstance(val, bool) or not isinstance(val, (int, float)):
            return False, f"Invalid value type detected at index {index}. All elements must be numbers.", []
            
    return True, "Valid", numbers_list


# GET endpoint
@app.get("/hello")
def hello():
    # Retrieve 'name' query parameter. If missing, default to 'Chris'.
    name_param = request.args.get('name', 'Chris').strip()
    
    # Edge Case: Handle empty parameter strings safely (e.g., /hello?name= )
    if not name_param:
        name_param = 'Chris'
        
    return jsonify({
        "greeting": f"Hello, {name_param}!",
        "status": "success"
    })


# POST endpoint
@app.post("/sum")
def sum_numbers():
    data = request.get_json()
    if not data:
        return jsonify({
            "error": "No JSON data provided"
        }), 400

    # Run nested schema type validation checks
    is_valid, error_msg, numbers = validate_sum_payload(data)
    if not is_valid:
        return jsonify({
            "error": error_msg
        }), 400

    # Calculate sum using Python's native built-in sum function
    total_sum = sum(numbers)
    
    return jsonify({
        "input_count": len(numbers),
        "result": total_sum,
        "status": "received"
    })

# --- ERROR HANDLING ---

@app.errorhandler(400)
def bad_request_fallback(e):
    """Fallback handler for generic malformed HTTP requests."""
    return jsonify({"error": "Bad Request. Malformed data stream input structure."}), 400

@app.errorhandler(404)
def route_not_found(e):
    """Gracefully catch attempts to hit non-existent route paths."""
    return jsonify({"error": "Requested URL route target was not found."}), 404


if __name__ == "__main__":
    # Forces the server to run locally on port 5000 with debug features enabled
    app.run(host="127.0.0.1", port=5000, debug=True)