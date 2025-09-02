## Peano Axioms Playground (Flask)

Minimal Flask app to explore Peano arithmetic (naturals and fractions) with a step-by-step trace.

### Run with Docker
```bash
docker build -t peano-app .
docker run --rm -p 8080:8080 peano-app
```
Open `http://localhost:8080`.

### Run locally
```bash
source venv/bin/activate
pip install -r requirements.txt
flask --app peano_app.app run --host 0.0.0.0 --port 8080
```