from flask import Flask
from get import get_bp
from put import put_bp
from post import post_bp
from delete import delete_bp
from put import put_bp

app = Flask(__name__)

app.register_blueprint(get_bp)
app.register_blueprint(put_bp)
app.register_blueprint(post_bp)
app.register_blueprint(delete_bp)
app.register_blueprint(put_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)