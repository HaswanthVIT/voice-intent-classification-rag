from flask import Flask
from flask_cors import CORS
from module_4.routes.pipeline import pipeline_bp
from module_4.routes.outcome import outcome_bp
from module_4.routes.call_data import call_data_bp
from module_4.routes.learning import learning_bp
from module_4.routes.calls import calls_bp
from module_4.routes.upload import upload_bp          # NEW

app = Flask(__name__)
CORS(app)

app.register_blueprint(pipeline_bp)
app.register_blueprint(outcome_bp)
app.register_blueprint(call_data_bp)
app.register_blueprint(learning_bp)
app.register_blueprint(calls_bp)
app.register_blueprint(upload_bp)                     # NEW

if __name__ == "__main__":
    app.run(debug=True, port=5000)