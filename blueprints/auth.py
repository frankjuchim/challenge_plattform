from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form.get("password")
        if password == current_app.config['ADMIN_PASSWORD']:
            session["is_admin"] = True
            return redirect(url_for('admin.dashboard')) # Assuming admin blueprint has a dashboard route
        else:
            return render_template(
                "admin/login.html",
                error="Falsches Passwort"
            )

    return render_template("admin/login.html")

@auth_bp.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    return redirect(url_for('public.index'))
