from flask import Flask
from flask_cors import CORS   # ✅ NEW

from backend.routes.calls import calls_bp
from backend.routes.outcome import outcome_bp
from backend.routes.learning import learning_bp
from backend.routes.pipeline import pipeline_bp
from backend.routes.call_data import call_data_bp
from backend.db_handler import init_db

init_db()

app = Flask(__name__)
CORS(app)   # ✅ VERY IMPORTANT (frontend connection)

app.register_blueprint(calls_bp)
app.register_blueprint(outcome_bp)
app.register_blueprint(learning_bp)
app.register_blueprint(pipeline_bp)
app.register_blueprint(call_data_bp)

@app.route("/")
def home():
    return {"message": "Module 4 API running 🚀"}

if __name__ == "__main__":
    app.run(debug=True)