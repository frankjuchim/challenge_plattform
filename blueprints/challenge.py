from flask import Blueprint, render_template, request, redirect, url_for, session, abort, current_app
from extensions import db
from models import Team, Challenge, Task, Submission
from werkzeug.utils import secure_filename
import os
from datetime import datetime

challenge_bp = Blueprint('challenge', __name__)

def allowed_file(filename, allowed_ext):
    return "." in filename and filename.lower().endswith(allowed_ext.lower())

def get_active_challenge():
    # In old app: SELECT * FROM challenges WHERE active = 1
    return Challenge.query.filter_by(active=True).first()

@challenge_bp.route("/challenge")
def view():
    if "team_id" not in session:
        return redirect(url_for("public.index"))

    team_id = session["team_id"]
    team = Team.query.get(team_id) # Ensure team exists

    # Logic from app.py: "EINZIGE aktive Challenge: die zuletzt angelegte" (Wait, app.py said that but code did ORDER BY id DESC LIMIT 1)
    # Actually app.py said:
    # challenge = query_db("SELECT * FROM challenges ORDER BY id DESC LIMIT 1", one=True)
    # But get_active_challenge used WHERE active=1.
    # The view used the *latest* one, not necessarily active?
    # Let's check app.py trace again.
    # 644: challenge = query_db("SELECT * FROM challenges ORDER BY id DESC LIMIT 1", one=True)
    # This implies the team sees the LATEST challenge, regardless of active status?
    # But later:
    # 693: challenge = get_active_challenge() (in submit_task)
    #
    # I should probably stick to "show the latest one".
    
    challenge = Challenge.query.order_by(Challenge.id.desc()).first()

    if not challenge:
        return render_template(
            "challenge.html",
            challenge=None,
            tasks=[],
            submission_map={},
            team=team.name if team else session.get("team_name")
        )

    tasks = Task.query.filter_by(challenge_id=challenge.id).all()
    
    submissions = Submission.query.filter_by(team_id=team_id).join(Task).filter(Task.challenge_id == challenge.id).all()
    submission_map = {s.task_id: s for s in submissions}

    return render_template(
        "challenge.html",
        challenge=challenge,
        tasks=tasks,
        submission_map=submission_map,
        team=team.name if team else session.get("team_name")
    )

@challenge_bp.route("/submit/<int:task_id>", methods=["POST"])
def submit_task(task_id):
    if "team_id" not in session:
        abort(403)

    # Submission allowed only for ACTIVE challenge?
    # app.py: 
    # challenge = get_active_challenge() (WHERE active=1)
    # if not challenge: abort(403)
    
    # Logic fix: View shows LATEST challenge, but submit checked ACTIVE challenge.
    # We should stick to the latest challenge to allow submission if it's visible.
    
    challenge = Challenge.query.order_by(Challenge.id.desc()).first()
    if not challenge:
        abort(403)
        
    # Check if task belongs to active challenge?
    task = Task.query.get_or_404(task_id)
    if task.challenge_id != challenge.id:
        abort(403) # Task not part of active challenge

    team_id = session["team_id"]

    # Check existing
    existing = Submission.query.filter_by(team_id=team_id, task_id=task_id).first()
    if existing:
        abort(403)

    # Paused check
    # app.py checked if ANY challenge was paused? 
    # 708: challenge = query_db("SELECT * FROM challenges ORDER BY id DESC LIMIT 1", one=True)
    # if challenge["paused"]: abort(403)
    # It seems to check the LATEST challenge for paused status.
    latest_challenge = Challenge.query.order_by(Challenge.id.desc()).first()
    if latest_challenge and latest_challenge.paused:
        abort(403)

    # File check
    if "file" not in request.files:
        abort(400)
    
    file = request.files["file"]
    if file.filename == "" or not allowed_file(file.filename, task.allowed_extension):
        abort(400)

    filename = secure_filename(file.filename)
    team_folder = os.path.join(current_app.config["UPLOAD_FOLDER"], str(team_id))
    os.makedirs(team_folder, exist_ok=True)
    
    filepath = os.path.join(team_folder, f"task_{task_id}_{filename}")
    file.save(filepath)

    submission = Submission(
        team_id=team_id,
        task_id=task_id,
        filename=filepath,
        timestamp=datetime.now()
    )
    db.session.add(submission)
    db.session.commit()

    return redirect(url_for("challenge.view"))
