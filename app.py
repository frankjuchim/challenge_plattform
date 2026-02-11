from flask import Flask, redirect, request
from config import Config
from extensions import db, csrf
from blueprints.auth import auth_bp
from blueprints.public import public_bp
from blueprints.challenge import challenge_bp
from blueprints.admin import admin_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Extensions
    db.init_app(app)
    csrf.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(public_bp)
    app.register_blueprint(challenge_bp)
    app.register_blueprint(admin_bp)

    # Global Middleware
    @app.before_request
    def force_http():
        if request.headers.get("X-Forwarded-Proto") == "https":
            return redirect(request.url.replace("https://", "http://"), code=301)

    return app

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all() # Auto-create tables for dev
        
    app.run(
      host="0.0.0.0",
      port=8000,
      debug=True
    )



if __name__ == "__main__":
    app.run(
      host="0.0.0.0",
      port=8000, #5000 belegt durch AirDrop
      debug=True
    )

