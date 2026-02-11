from datetime import datetime
from extensions import db

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=True) # nullable for migration of old teams, but we reset DB anyway
    submissions = db.relationship('Submission', backref='team', lazy=True)

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

class Challenge(db.Model):
    __tablename__ = 'challenges'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    active = db.Column(db.Boolean, default=False)
    paused = db.Column(db.Boolean, default=False)
    tasks = db.relationship('Task', backref='challenge', lazy=True, cascade="all, delete-orphan")

    def status(self):
        now = datetime.now()
        if not self.start_time or not self.end_time:
            return "not_scheduled"
        if now < self.start_time:
            return "upcoming"
        if self.start_time <= now <= self.end_time:
            return "running"
        return "finished"

    @property
    def remaining_seconds(self):
        if not self.end_time:
            return 0
        now = datetime.now()
        remaining = (self.end_time - now).total_seconds()
        return max(0, int(remaining))

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    max_points = db.Column(db.Integer, default=0)
    submissions = db.relationship('Submission', backref='task', lazy=True, cascade="all, delete-orphan")

class Submission(db.Model):
    __tablename__ = 'submissions'
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    filename = db.Column(db.String(300), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    points = db.Column(db.Integer, nullable=True)
    feedback = db.Column(db.Text, nullable=True)

    __table_args__ = (db.UniqueConstraint('team_id', 'task_id', name='_team_task_uc'),)
