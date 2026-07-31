import os
from flask import Flask, render_template, jsonify, request
from config import Config
from routes.analysis_routes import analysis_bp
from routes.job_routes import job_bp
from routes.builder_routes import builder_bp
from routes.resume_routes import file_bp
from routes.auth_routes import auth_bp
from routes.ai_routes import ai_bp
from routes.interview_routes import interview_bp
from routes.dashboard_routes import dash_bp

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)

    # Initialize configuration (ensure upload/generated folders exist)
    Config.init_app()

    # Register API Blueprints
    app.register_blueprint(analysis_bp)
    app.register_blueprint(job_bp)
    app.register_blueprint(builder_bp)
    app.register_blueprint(file_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(interview_bp)
    app.register_blueprint(dash_bp)

    # Web Page Routes
    @app.route("/")
    def page_home():
        return render_template("index.html", active_page="home")

    @app.route("/builder")
    def page_builder():
        return render_template("builder.html", active_page="builder")

    @app.route("/analyzer")
    def page_analyzer():
        return render_template("analyzer.html", active_page="analyzer")

    @app.route("/matcher")
    def page_matcher():
        return render_template("matcher.html", active_page="matcher")

    @app.route("/dashboard")
    @app.route("/dashboard/<analysis_id>")
    def page_dashboard(analysis_id=None):
        return render_template("dashboard.html", active_page="dashboard", initial_analysis_id=analysis_id or "")

    @app.route("/templates")
    def page_templates():
        return render_template("templates.html", active_page="templates")

    @app.route("/about")
    def page_about():
        return render_template("about.html", active_page="about")

    @app.route("/login")
    def page_login():
        return render_template("login.html", active_page="login")

    @app.route("/register")
    def page_register():
        return render_template("register.html", active_page="register")

    @app.route("/forgot-password")
    def page_forgot_password():
        return render_template("forgot_password.html", active_page="forgot_password")

    @app.route("/profile")
    def page_profile():
        return render_template("profile.html", active_page="profile")

    @app.route("/interview")
    def page_interview():
        return render_template("interview.html", active_page="interview")

    @app.route("/interview/mock")
    def page_interview_mock():
        interview_type = request.args.get("type", "technical")
        category = request.args.get("category", "General")
        difficulty = request.args.get("difficulty", "medium")
        return render_template("interview_mock.html", active_page="interview", interview_type=interview_type, category=category, difficulty=difficulty)

    @app.route("/interview/results/<session_id>")
    def page_interview_results(session_id):
        return render_template("interview_results.html", active_page="interview", session_id=session_id)

    # Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("index.html", active_page="home", error="Page not found"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({"success": False, "error": "Internal server error occurred. Please try again."}), 500

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=(Config.APP_ENV == "development"))
