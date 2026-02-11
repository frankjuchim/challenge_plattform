from flask import Blueprint, render_template, request, redirect, url_for, session
from extensions import db
from models import Team, Challenge, Task, Submission
import time # Added for start route

public_bp = Blueprint('public', __name__)

@public_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        team_name = request.form.get("team")
        password = request.form.get("password")
        
        if not team_name or not password:
            return render_template("index.html", error="Bitte Teamname und Passwort angeben.")

        # Check if team exists
        existing_team = Team.query.filter_by(name=team_name).first()
        if existing_team:
             return render_template("index.html", error="Teamname vergeben. Bitte einloggen oder anderen Namen wählen.")

        # Create new team
        new_team = Team(name=team_name)
        new_team.set_password(password)
        db.session.add(new_team)
        db.session.commit()

        # Auto-login
        session["team_id"] = new_team.id
        session["team_name"] = new_team.name
        return redirect(url_for("challenge.view"))

    return render_template("index.html")

@public_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        team_name = request.form.get("team")
        password = request.form.get("password")
        
        team = Team.query.filter_by(name=team_name).first()
        if team and team.check_password(password):
            session["team_id"] = team.id
            session["team_name"] = team.name
            return redirect(url_for("challenge.view"))
        else:
             return render_template("login.html", error="Ungültiger Teamname oder Passwort.")

    return render_template("login.html")

@public_bp.route("/logout")
def logout():
    session.pop("team_id", None)
    session.pop("team_name", None)
    return redirect(url_for("public.index"))

@public_bp.route("/scoreboard")
def scoreboard():
    # Logic fix: Use LATEST challenge to match other views
    challenge = Challenge.query.order_by(Challenge.id.desc()).first()

    if not challenge:
        return render_template("scoreboard.html", challenge=None)

    tasks = Task.query.filter_by(challenge_id=challenge.id).order_by(Task.id).all()
    teams = Team.query.order_by(Team.name).all()
    
    # Submissions for this challenge
    submissions = Submission.query.join(Task).filter(Task.challenge_id == challenge.id).all()

    # Prepare score map
    score_map = {}
    for team in teams:
        score_map[team.id] = {
            "name": team.name,
            "task_points": {t.id: 0 for t in tasks},
            "total": 0
        }

    for s in submissions:
        if s.team_id in score_map:
            score_map[s.team_id]["task_points"][s.task_id] = s.points or 0 # Handle None points
            score_map[s.team_id]["total"] += (s.points or 0)

    # Sort by total
    sorted_teams = sorted(
        score_map.values(),
        key=lambda x: x["total"],
        reverse=True
    )

    return render_template(
        "scoreboard.html",
        challenge=challenge,
        tasks=tasks,
        teams=sorted_teams
    )

@public_bp.route("/start")
def start():
    challenge = Challenge.query.filter_by(active=True).first()
    
    # Check if there is a PLANNED challenge (future start time)
    # If multiple, take the next one. For simplicity, we check if ANY challenge has a start_time in future
    # But current data model might not support "planned" status explicitly other than via time.
    # Let's assume we want to show countdown for the active challenge if it hasn't started yet, 
    # or just a general "next event" page. 
    
    # Reusing existing logic concept from previous file content if applicable
    status = "IDLE"
    start_time_ts = 0
    
    if challenge and challenge.start_time:
        now = time.time()
        if challenge.start_time > now:
            status = "PLANNED"
            start_time_ts = challenge.start_time
    
    return render_template("start.html", challenge=challenge, status=status, start_time=start_time_ts)
