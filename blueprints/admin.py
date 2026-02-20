from flask import Blueprint, render_template, request, redirect, url_for, session, abort, send_from_directory, current_app
from extensions import db
from models import Team, Challenge, Task, Submission
from datetime import datetime
import os

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
def restrict_admin():
    if request.endpoint == 'auth.admin_login':
        return
    if not session.get("is_admin"):
        return redirect(url_for('auth.admin_login'))

@admin_bp.route("/dashboard")
def dashboard():
    challenges = Challenge.query.order_by(Challenge.id.desc()).all()
    return render_template("admin/dashboard.html", challenges=challenges)

@admin_bp.route("/challenges")
def challenges_list():
    challenges = Challenge.query.order_by(Challenge.id.desc()).all()
    return render_template("admin/challenges.html", challenges=challenges)

@admin_bp.route("/challenges/new", methods=["GET", "POST"])
def challenge_new():
    if request.method == "POST":
        title = request.form["title"]
        challenge = Challenge(title=title)
        db.session.add(challenge)
        db.session.commit()
        return redirect(url_for('admin.challenges_list'))
    return render_template("admin/challenge_new.html")

@admin_bp.route("/challenge/<int:cid>/activate")
def challenge_activate(cid):
    # Deactivate all
    Challenge.query.update({Challenge.active: False})
    # Activate one
    challenge = Challenge.query.get_or_404(cid)
    challenge.active = True
    db.session.commit()
    return redirect(url_for('admin.dashboard'))

@admin_bp.route("/challenges/<int:cid>/tasks", methods=["GET", "POST"])
def challenge_tasks(cid):
    challenge = Challenge.query.get_or_404(cid)

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        max_points = int(request.form["max_points"])
        allowed_extension = request.form.get("allowed_extension", ".pde")
        
        task = Task(
            challenge_id=cid, 
            title=title, 
            description=description, 
            max_points=max_points,
            allowed_extension=allowed_extension
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('admin.challenge_tasks', cid=cid))

    tasks = Task.query.filter_by(challenge_id=cid).all()
    return render_template("admin/challenge_tasks.html", challenge=challenge, tasks=tasks)

@admin_bp.route("/challenges/<int:cid>/pause", methods=["POST"])
def challenge_pause(cid):
    challenge = Challenge.query.get_or_404(cid)
    challenge.paused = True
    db.session.commit()
    return redirect(url_for('admin.challenges_list'))

@admin_bp.route("/challenges/<int:cid>/resume", methods=["POST"])
def challenge_resume(cid):
    challenge = Challenge.query.get_or_404(cid)
    challenge.paused = False
    db.session.commit()
    return redirect(url_for('admin.challenges_list'))

@admin_bp.route("/challenges/<int:cid>/delete", methods=["POST"])
def challenge_delete(cid):
    challenge = Challenge.query.get_or_404(cid)
    db.session.delete(challenge)
    db.session.commit()
    return redirect(url_for('admin.challenges_list'))

@admin_bp.route("/tasks/<int:tid>/delete", methods=["POST"])
def task_delete(tid):
    task = Task.query.get_or_404(tid)
    cid = task.challenge_id
    db.session.delete(task)
    db.session.commit()
    # Redirect back to tasks list
    return redirect(url_for('admin.challenge_tasks', cid=cid))

@admin_bp.route("/tasks/<int:tid>/edit", methods=["GET", "POST"])
def task_edit(tid):
    task = Task.query.get_or_404(tid)
    cid = task.challenge_id
    
    if request.method == "POST":
        task.title = request.form["title"]
        task.description = request.form["description"]
        task.max_points = int(request.form["max_points"])
        task.allowed_extension = request.form.get("allowed_extension", ".pde")
        db.session.commit()
        return redirect(url_for('admin.challenge_tasks', cid=cid))

    return render_template("admin/task_edit.html", task=task)

@admin_bp.route("/submissions", methods=["GET", "POST"])
def submissions():
    if request.method == "POST":
        submission_id = request.form.get("submission_id")
        
        if "soft_reset" in request.form:
             submission = Submission.query.get(submission_id)
             if submission:
                 submission.points = None
                 submission.feedback = None
                 db.session.commit()
        else:
             points = request.form.get("points")
             feedback = request.form.get("feedback", "")
             submission = Submission.query.get(submission_id)
             if submission and points: # Check if points is not empty string
                 submission.points = int(points)
                 submission.feedback = feedback
                 db.session.commit()
        return redirect(url_for('admin.submissions'))

    # List submissions
    raw_submissions = Submission.query.join(Team).join(Task).order_by(
        Submission.points.isnot(None), 
        Team.name
    ).all()
    
    submissions_data = []
    for s in raw_submissions:
        content = "Datei konnte nicht gelesen werden."
        try:
            if os.path.exists(s.filename):
                with open(s.filename, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
            else:
                content = "Datei nicht gefunden."
        except Exception as e:
            content = f"Fehler: {e}"

        submissions_data.append({
            "id": s.id,
            "team_name": s.team.name,
            "task_title": s.task.title,
            "task_description": s.task.description,
            "max_points": s.task.max_points,
            "points": s.points,
            "feedback": s.feedback,
            "code": content
        })

    return render_template("admin/review.html", submissions=submissions_data)

@admin_bp.route("/grade/<int:submission_id>", methods=["POST"])
def submission_grade(submission_id):
    points = int(request.form["points"])
    comment = request.form.get("comment", "")
    
    submission = Submission.query.get_or_404(submission_id)
    submission.points = points
    submission.feedback = comment # Model unified 'comment' to 'feedback'
    db.session.commit()
    
    return redirect(url_for('admin.submissions'))

@admin_bp.route("/reset/<int:submission_id>", methods=["POST"])
def submission_reset(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    db.session.delete(submission)
    db.session.commit()
    return redirect(url_for('admin.submissions'))

def safe_name(text):
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
    return "".join(c if c in allowed else "_" for c in text)

@admin_bp.route("/download/<int:submission_id>")
def download_submission(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    
    filepath = submission.filename
    directory = os.path.dirname(filepath)
    original_filename = os.path.basename(filepath)
    
    team_clean = safe_name(submission.team.name)
    ext = os.path.splitext(original_filename)[1]  # z.B. ".sb3" oder ".pde"
    download_name = f"{team_clean}_Aufgabe_{submission.task_id}{ext}"
    
    return send_from_directory(
        directory,
        original_filename,
        as_attachment=True,
        download_name=download_name
    )

@admin_bp.route("/teams")
def teams():
    teams = Team.query.order_by(Team.name).all()
    return render_template("admin/teams.html", teams=teams)

@admin_bp.route("/team/delete/<int:team_id>", methods=["POST"])
def team_delete(team_id):
    team = Team.query.get_or_404(team_id)
    db.session.delete(team)
    db.session.commit()
    return redirect(url_for('admin.teams'))
