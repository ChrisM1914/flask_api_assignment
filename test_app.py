import pytest
from app import app

@pytest.fixture
def client():
    """Configures the official Flask test client framework execution wrapper."""
    app.config['TESTING'] = True
    with app.test_client() as test_client:
        yield test_client


# --- GET /hello TEST CASES ---

def test_hello_default_param(client):
    """Verifies route falls back to 'World' when query param is entirely missing."""
    response = client.get('/hello')
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data["status"] == "success"
    assert json_data["greeting"] == "Hello, World!"

def test_hello_custom_param(client):
    """Verifies query parameters map correctly into string greetings."""
    response = client.get('/hello?name=Chris')
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data["greeting"] == "Hello, Chris!"

def test_hello_empty_param_edge_case(client):
    """Verifies fallback handles blank string values gracefully."""
    response = client.get('/hello?name=')
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data["greeting"] == "Hello, Chris!"


# --- POST /sum TEST CASES ---

def test_sum_successful_integers(client):
    """Verifies that arrays of integer values sum correctly."""
    response = client.post('/sum', json={"numbers": [1, 2, 3]})
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data["status"] == "received"
    assert json_data["result"] == 6

def test_sum_successful_floats_and_negatives(client):
    """Verifies math execution handling negative signs and decimals."""
    response = client.post('/sum', json={"numbers": [1.5, -2, 3.5]})
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data["result"] == 3.0

def test_sum_empty_list_edge_case(client):
    """Verifies that an empty array cleanly computes to 0."""
    response = client.post('/sum', json={"numbers": []})
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data["result"] == 0


# --- FAILURE MODE / ERROR HANDLING TEST CASES ---

def test_sum_malformed_json_syntax(client):
    """Verifies raw string input tracking crashes cleanly into a 400 error."""
    response = client.post('/sum', 
                           data='{"numbers": [1, 2, ', 
                           content_type='application/json')
    json_data = response.get_json()
    assert response.status_code == 400
    assert "error" in json_data

def test_sum_missing_required_key(client):
    """Verifies 400 structure catches typo payloads."""
    response = client.post('/sum', json={"wrong_key": [1, 2, 3]})
    json_data = response.get_json()
    assert response.status_code == 400
    assert "Missing required key" in json_data["error"]

def test_sum_invalid_type_in_list(client):
    """Verifies internal value screening blocks strings mixed with integers."""
    response = client.post('/sum', json={"numbers": [1, "two", 3]})
    json_data = response.get_json()
    assert response.status_code == 400
    assert "Invalid value type detected" in json_data["error"]

def test_sum_boolean_leakage_edge_case(client):
    """Verifies Python booleans (True/False evaluate to numbers natively) are rejected."""
    response = client.post('/sum', json={"numbers": [1, True, 3]})
    json_data = response.get_json()
    assert response.status_code == 400