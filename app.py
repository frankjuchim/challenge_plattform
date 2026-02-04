from flask import Flask, render_template, request, redirect, url_for, abort, session, send_from_directory
from datetime import datetime, timedelta
import os
import sqlite3
from werkzeug.utils import secure_filename

from config import DATABASE, UPLOAD_FOLDER, SECRET_KEY, ADMIN_PASSWORD
#print("APP LOADED")


app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"pde"}

@app.before_request
def protect_admin_routes():
    if request.path.startswith("/admin"):
        if request.path == "/admin/login":
            return
        if not session.get("is_admin"):
            abort(403)


@app.before_request
def force_http():
    if request.headers.get("X-Forwarded-Proto") == "https":
        return redirect(request.url.replace("https://", "http://"), code=301)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ---------- Hilfsfunktionen ----------
def challenge_status(challenge):
    if not challenge:
        return "NONE"

    now = datetime.now()
    start = datetime.fromisoformat(challenge["start_time"])
    end = datetime.fromisoformat(challenge["end_time"])

    if now < start:
        return "NOT_STARTED"
    elif start <= now <= end:
        return "RUNNING"
    else:
        return "FINISHED"
      
def challenge_remaining_seconds(challenge):
    if not challenge:
        return 0

    now = datetime.now()
    end = datetime.fromisoformat(challenge["end_time"])
    remaining = (end - now).total_seconds()

    return max(0, int(remaining))

@app.route("/start")
def start_screen():
    challenge = get_active_challenge()

    if not challenge:
        status = "NONE"
    else:
        status = challenge_status(challenge)

    return render_template(
        "start.html",
        challenge=challenge,
        status=status
    )



# ---------- Datenbank ----------
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def query_db(query, args=(), one=False):
    conn = get_db()
    cur = conn.execute(query, args)
    rv = cur.fetchall()
    conn.commit()
    conn.close()
    return (rv[0] if rv else None) if one else rv

def get_active_challenge():
    return query_db(
        "SELECT * FROM challenges WHERE active = 1",
        one=True
    )

# ---------- Initialisierung ----------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        team_name = request.form["team"]

        team = query_db(
            "SELECT * FROM teams WHERE name = ?",
            (team_name,),
            one=True
        )

        if not team:
            query_db(
                "INSERT INTO teams (name) VALUES (?)",
                (team_name,)
            )

            team = query_db(
                "SELECT * FROM teams WHERE name = ?",
                (team_name,),
                one=True
            )

        session["team_id"] = team["id"]
        session["team_name"] = team["name"]

        return redirect(url_for("challenge_view"))

    return render_template("index.html")


@app.route("/scoreboard")
def scoreboard():
    challenge = get_active_challenge()

    if not challenge:
        return render_template("scoreboard.html", challenge=None)

    # Aufgaben der Challenge
    tasks = query_db(
        "SELECT id, title FROM tasks WHERE challenge_id = ? ORDER BY id",
        (challenge["id"],)
    )

    # Teams
    teams = query_db(
        "SELECT id, name FROM teams ORDER BY name"
    )

    # Alle Abgaben dieser Challenge
    submissions = query_db("""
        SELECT team_id, task_id, points
        FROM submissions
        WHERE task_id IN (
            SELECT id FROM tasks WHERE challenge_id = ?
        )
    """, (challenge["id"],))

    # Punkte-Matrix vorbereiten
    score_map = {}
    for team in teams:
        score_map[team["id"]] = {
            "name": team["name"],
            "task_points": {t["id"]: 0 for t in tasks},
            "total": 0
        }

    # Punkte eintragen
    for s in submissions:
        team_entry = score_map[s["team_id"]]
        team_entry["task_points"][s["task_id"]] = s["points"]
        team_entry["total"] += s["points"]

    # Nach Gesamtpunkten sortieren
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




# ---------- Admin ----------
@app.route("/admin")
def admin_root():
    return redirect("/admin/login")

  
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form["password"] == ADMIN_PASSWORD:
            session["is_admin"] = True
            return redirect("/admin/dashboard")
        else:
            return render_template(
                "admin/login.html",
                error="Falsches Passwort"
            )

    return render_template("admin/login.html")
  

@app.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    return redirect("/")


@app.route("/admin/dashboard")
def admin_dashboard():
    challenges = query_db("SELECT * FROM challenges ORDER BY id DESC")
    return render_template("admin/dashboard.html", challenges=challenges)

@app.route("/admin/challenge/new", methods=["GET", "POST"])
def new_challenge():
    if request.method == "POST":
        title = request.form["title"]
        duration = int(request.form["duration"])  # Minuten

        start = datetime.now()
        end = start + timedelta(minutes=duration)

        query_db(
            "INSERT INTO challenges (title, start_time, end_time, active) VALUES (?, ?, ?, 0)",
            (title, start.isoformat(), end.isoformat())
        )
        return redirect(url_for("admin_dashboard"))

    return render_template("admin/new_challenge.html")
  
@app.route("/admin/challenge/<int:cid>/activate")
def activate_challenge(cid):
    # alle deaktivieren
    query_db("UPDATE challenges SET active = 0")

    # diese aktivieren
    query_db("UPDATE challenges SET active = 1 WHERE id = ?", (cid,))

    return redirect(url_for("admin_dashboard"))

@app.route("/admin/challenge/<int:cid>/tasks", methods=["GET", "POST"])
def manage_tasks(cid):
    challenge = query_db(
        "SELECT * FROM challenges WHERE id = ?", (cid,), one=True
    )

    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["description"]
        max_points = int(request.form["max_points"])

        query_db(
            "INSERT INTO tasks (challenge_id, title, description, max_points) VALUES (?, ?, ?, ?)",
            (cid, title, desc, max_points)
        )

    tasks = query_db(
        "SELECT * FROM tasks WHERE challenge_id = ?", (cid,)
    )
    print("TASK ROUTE REGISTERED")
    return render_template(
        "admin/tasks.html",
        challenge=challenge,
        tasks=tasks
    )

@app.route("/admin/submissions", methods=["GET", "POST"])
def admin_submissions():
    if not session.get("is_admin"):
        abort(403)

    # ---------------------------
    # POST: Bewertung / Reset
    # ---------------------------
    if request.method == "POST":
        submission_id = request.form.get("submission_id")

        # Soft-Reset (Bewertung zurücksetzen)
        if "soft_reset" in request.form:
            query_db(
                "UPDATE submissions SET points = NULL, feedback = NULL WHERE id = ?",
                (submission_id,)
            )
            return redirect("/admin/submissions")

        # Bewertung speichern / aktualisieren
        points = request.form.get("points")
        feedback = request.form.get("feedback", "")

        if points is not None:
            query_db(
                """
                UPDATE submissions
                SET points = ?, feedback = ?
                WHERE id = ?
                """,
                (int(points), feedback, submission_id)
            )

        return redirect("/admin/submissions")

    # ---------------------------
    # GET: Abgaben anzeigen
    # ---------------------------
    submissions = query_db("""
        SELECT
          submissions.id,
          submissions.filename,
          submissions.points,
          submissions.feedback,
          tasks.max_points,
          teams.name AS team_name,
          tasks.title AS task_title
        FROM submissions
        JOIN teams ON submissions.team_id = teams.id
        JOIN tasks ON submissions.task_id = tasks.id
        ORDER BY
          submissions.points IS NOT NULL,
          teams.name
    """)

    return render_template(
        "admin/review.html",
        submissions=submissions
    )


@app.route("/admin/grade/<int:submission_id>", methods=["POST"])
def grade_submission(submission_id):
    points = int(request.form["points"])
    comment = request.form.get("comment", "")

    query_db(
        "UPDATE submissions SET points = ?, comment = ? WHERE id = ?",
        (points, comment, submission_id)
    )

    return redirect(url_for("admin_submissions"))

@app.route("/admin/reset/<int:submission_id>", methods=["POST"])
def reset_submission(submission_id):
    query_db(
        "DELETE FROM submissions WHERE id = ?",
        (submission_id,)
    )

    return redirect(url_for("admin_submissions"))

def safe_name(text):
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
    return "".join(c if c in allowed else "_" for c in text)

@app.route("/admin/download/<int:submission_id>")
def download_submission(submission_id):
    submission = query_db("""
        SELECT submissions.filename,
               teams.name AS team,
               tasks.id AS task_id
        FROM submissions
        JOIN teams ON submissions.team_id = teams.id
        JOIN tasks ON submissions.task_id = tasks.id
        WHERE submissions.id = ?
    """, (submission_id,), one=True)

    if not submission:
        abort(404)

    filepath = submission["filename"]
    directory = os.path.dirname(filepath)
    original_filename = os.path.basename(filepath)

    # 🔹 Teamname "dateisicher" machen
    team_clean = safe_name(submission["team"])

    # 🔹 Neue Download-Bezeichnung
    download_name = f"{team_clean}_Aufgabe_{submission['task_id']}.pde"

    return send_from_directory(
        directory,
        original_filename,
        as_attachment=True,
        download_name=download_name
    )
    
@app.route("/admin/task/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    # Abgaben zur Aufgabe löschen
    query_db("DELETE FROM submissions WHERE task_id = ?", (task_id,))
    # Aufgabe löschen
    query_db("DELETE FROM tasks WHERE id = ?", (task_id,))
    return redirect(request.referrer or "/admin/dashboard")

@app.route("/admin/challenge/delete/<int:challenge_id>", methods=["POST"])
def delete_challenge(challenge_id):
    # Aufgaben der Challenge holen
    tasks = query_db(
        "SELECT id FROM tasks WHERE challenge_id = ?",
        (challenge_id,)
    )

    for t in tasks:
        query_db("DELETE FROM submissions WHERE task_id = ?", (t["id"],))

    query_db("DELETE FROM tasks WHERE challenge_id = ?", (challenge_id,))
    query_db("DELETE FROM challenges WHERE id = ?", (challenge_id,))

    return redirect("/admin/dashboard")

@app.route("/admin/team/delete/<int:team_id>", methods=["POST"])
def delete_team(team_id):
    query_db("DELETE FROM submissions WHERE team_id = ?", (team_id,))
    query_db("DELETE FROM teams WHERE id = ?", (team_id,))
    return redirect("/admin/teams")

@app.route("/admin/teams")
def admin_teams():
    teams = query_db("SELECT id, name FROM teams ORDER BY name")
    return render_template("admin/teams.html", teams=teams)

@app.route("/admin/review", methods=["GET", "POST"])
def admin_review():
    if not session.get("is_admin"):
        abort(403)

    submissions = query_db("""
        SELECT
          submissions.id,
          submissions.filename,
          submissions.max_points,
          teams.name AS team_name,
          tasks.title AS task_title
        FROM submissions
        JOIN teams ON submissions.team_id = teams.id
        JOIN tasks ON submissions.task_id = tasks.id
        WHERE submissions.points IS NULL
    """)

    return render_template(
        "admin/review.html",
        submissions=submissions
    )
    
@app.route("/admin/challenges")
def admin_challenges():
    if not session.get("is_admin"):
        abort(403)

    challenges = query_db("""
        SELECT * FROM challenges ORDER BY id DESC
    """)

    return render_template(
        "admin/challenges.html",
        challenges=challenges
    )

@app.route("/admin/challenges/new", methods=["GET", "POST"])
def admin_challenge_new():
    if not session.get("is_admin"):
        abort(403)

    if request.method == "POST":
        title = request.form["title"]

        query_db(
            "INSERT INTO challenges (title) VALUES (?)",
            (title,)
        )

        return redirect("/admin/challenges")

    return render_template("admin/challenge_new.html")
  
@app.route("/admin/challenges/<int:cid>/tasks", methods=["GET", "POST"])
def admin_challenge_tasks(cid):
    if not session.get("is_admin"):
        abort(403)

    challenge = query_db(
        "SELECT * FROM challenges WHERE id = ?",
        (cid,),
        one=True
    )

    if not challenge:
        abort(404)

    if request.method == "POST":
        title = request.form["title"]
        max_points = int(request.form["max_points"])

        query_db(
            """
            INSERT INTO tasks (challenge_id, title, max_points)
            VALUES (?, ?, ?)
            """,
            (cid, title, max_points)
        )

        return redirect(f"/admin/challenges/{cid}/tasks")

    tasks = query_db(
        "SELECT * FROM tasks WHERE challenge_id = ?",
        (cid,)
    )

    return render_template(
        "admin/challenge_tasks.html",
        challenge=challenge,
        tasks=tasks
    )



# ---------- Teams ----------
@app.route("/challenge")
def challenge_view():
    if "team_id" not in session:
        return redirect(url_for("index"))

    challenge = get_active_challenge()
    submission_map = {}
    tasks = []
    message = None
    status = "NONE"
    remaining = 0
    submitted_task_ids = set()

    if not challenge:
        message = "Aktuell ist keine Challenge aktiv."
    else:
        status = challenge_status(challenge)
        remaining = challenge_remaining_seconds(challenge)

        tasks = query_db(
            "SELECT * FROM tasks WHERE challenge_id = ?",
            (challenge["id"],)
        )

        # 🔹 Eigene Abgaben des Teams holen
        submissions = query_db("""
            SELECT task_id, points, comment
            FROM submissions
            WHERE team_id = ?
        """, (session["team_id"],))

        submission_map = {
            s["task_id"]: s for s in submissions
        }
        submitted_task_ids = {s["task_id"] for s in submissions}

        if status == "FINISHED":
            message = "⏱ Die Challenge ist beendet. Abgaben sind nicht mehr möglich."

    return render_template(
        "challenge.html",
        team=session.get("team_name"),
        challenge=challenge,
        tasks=tasks,
        message=message,
        status=status,
        remaining=remaining,
        submitted_task_ids=submitted_task_ids,
        submission_map=submission_map
    )


@app.route("/submit/<int:task_id>", methods=["POST"])
def submit_task(task_id):
    if "team_id" not in session:
        print("ABORT 403 - 1")
        abort(403)

    challenge = get_active_challenge()
    if not challenge or challenge_status(challenge) != "RUNNING":
        abort(403)

    team_id = session["team_id"]

    # Einmal-Abgabe prüfen
    existing = query_db(
        "SELECT * FROM submissions WHERE team_id = ? AND task_id = ?",
        (team_id, task_id),
        one=True
    )
    if existing:
        abort(403)

    # Datei prüfen
    if "file" not in request.files:
        abort(400)

    file = request.files["file"]

    if file.filename == "":
        abort(400)

    if not allowed_file(file.filename):
        abort(400)

    # Datei speichern
    filename = secure_filename(file.filename)
    team_folder = os.path.join(app.config["UPLOAD_FOLDER"], str(team_id))
    os.makedirs(team_folder, exist_ok=True)

    filepath = os.path.join(team_folder, f"task_{task_id}_{filename}")
    file.save(filepath)

    # DB-Eintrag
    query_db(
        """
        INSERT INTO submissions (team_id, task_id, filename, timestamp, points)
        VALUES (?, ?, ?, ?, 0)
        """,
        (team_id, task_id, filepath, datetime.now().isoformat())
    )
    
    return redirect(url_for("challenge_view"))



if __name__ == "__main__":
    app.run(debug=True)
