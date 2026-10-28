# Flask API Assignment

Exercise to bridge core Python concepts with real world web development and experience in
Building a minimal API
Handling HTTP requests/responses
Writing testable, maintainable code
Deploying a local server for integration testing

---

## Setup Instructions

Follow step by step set up instructions

```bash
# 1. Create Project Directory (Anaconda Prompt)
mkdir flask_api_assignment && cd flask_api_assignment

# 2. Set Up Virtual Environment (Annaconda Prompt)
python -m venv venv
venv\Scripts\activate

# 3. Install Dependencies (Anaconda Prompt)
pip python -m pip install --upgrade pip
pip install Flask pytest
```

_Terminal indicator line should show `(venv)` prefix._

---

## Run the Server

Start the local Flask development server on port 5000:

```bash
python app.py
```

### Expected Server Output:

```text
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

---

## Endpoints Test

With your server actively running on port 5000, verify the operational pathways using a browser or a secondary terminal tab:

### 1. GET `/hello`

- **Command / URL:** Open a web browser and navigate to: `http://127.0.0.1:5000`
- **Expected Outcome:**
  ```json
  {
    "greeting": "Hello, Chris!",
    "status": "success"
  }
  ```

### 2. POST `/sum`

- **Command:** Run this command from a secondary terminal profile:
  ```bash
  curl -X POST http://127.0.0 -H "Content-Type: application/json" -d "{\"numbers\":}"
  ```
- **Expected Outcome:**
  ```json
  {
    "input_count": 3,
    "result": 60,
    "status": "received"
  }
  ```

### 3. POST `/sum` (Error Handling)

- **Command:** Run this command to pass invalid text instead of numbers:
  ```bash
  curl -X POST http://127.0.0 -H "Content-Type: application/json" -d "{\"numbers\": [10, \"broken_string\", 30]}"
  ```
- **Expected Outcome:**
  ```json
  {
    "error": "Invalid value type detected at index 1. All elements must be numbers."
  }
  ```

---

## Edge Cases

To run all edge case tests, stop the active server using **`Ctrl + C`** and type:

```bash
pytest test_app.py
```

### Expected Outcome:

```text
=========================== 10 passed in 0.18s ===========================
```
