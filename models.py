# -*- coding: utf-8 -*-
from extensions import db, login_manager
from flask_login import UserMixin
from datetime import datetime

# Favori egzersizler için ilişki tablosu
user_favorites = db.Table('user_favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('exercise_id', db.Integer, db.ForeignKey('exercise.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    water_intake_ml = db.Column(db.Integer, default=0)
    fasting_start = db.Column(db.DateTime, nullable=True)
    
    # Yeni eklenen Quiz/Kişiselleştirme alanları
    quiz_completed = db.Column(db.Boolean, default=False)
    goal = db.Column(db.String(50), nullable=True)
    fitness_level = db.Column(db.String(50), nullable=True)
    target_area = db.Column(db.String(50), nullable=True)
    
    # Oyunlaştırma: Seri (Streak)
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    last_active_date = db.Column(db.Date, nullable=True)
    
    # İlişkiler
    favorites = db.relationship('Exercise', secondary=user_favorites, lazy='subquery',
        backref=db.backref('favorited_by', lazy=True))

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    instructions = db.Column(db.Text, nullable=True)
    muscle_group = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    equipment = db.Column(db.String(100), nullable=True)
    video_url = db.Column(db.String(255), nullable=True)
    duration_seconds = db.Column(db.Integer, nullable=True)
    calories_estimate = db.Column(db.Integer, nullable=True)

class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    duration_days = db.Column(db.Integer, nullable=False)
    level = db.Column(db.String(50), nullable=False)
    goal = db.Column(db.String(100), nullable=False)

class ProgramExercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
    day_number = db.Column(db.Integer, nullable=False)
    sets = db.Column(db.Integer, nullable=True)
    reps = db.Column(db.Integer, nullable=True)
    rest_seconds = db.Column(db.Integer, nullable=True)
    
    program = db.relationship('Program', backref=db.backref('exercises', lazy=True))
    exercise = db.relationship('Exercise')

class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'), nullable=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=True)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    duration_spent = db.Column(db.Integer, nullable=True)
    calories_burned = db.Column(db.Integer, nullable=True)
    readiness_score = db.Column(db.Integer, nullable=True) # 0-10 before workout
    perceived_exertion = db.Column(db.Integer, nullable=True) # 0-10 after workout

    user = db.relationship('User', backref=db.backref('progress', lazy=True))
    program = db.relationship('Program')
    exercise = db.relationship('Exercise')

# YENI: Kilitli Meydan Okumalar
class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    duration_days = db.Column(db.Integer, nullable=False)

class ChallengeDay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=False)
    day_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=True)
    
    challenge = db.relationship('Challenge', backref=db.backref('days', lazy=True))

class ChallengeExercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    challenge_day_id = db.Column(db.Integer, db.ForeignKey('challenge_day.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
    sets = db.Column(db.Integer, nullable=True)
    reps = db.Column(db.Integer, nullable=True)
    rest_seconds = db.Column(db.Integer, nullable=True)
    
    challenge_day = db.relationship('ChallengeDay', backref=db.backref('exercises', lazy=True))
    exercise = db.relationship('Exercise')

class UserChallenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=False)
    current_day = db.Column(db.Integer, default=1)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('challenges', lazy=True))
    challenge = db.relationship('Challenge')

class UserProgram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'), nullable=False)
    current_day = db.Column(db.Integer, default=1)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('active_programs', lazy=True))
    program = db.relationship('Program')

# YENI: Beslenme Takibi
class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    icon = db.Column(db.String(50)) # SVG or icon name
    
class UserBadge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.id'), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('badges', lazy=True))
    badge = db.relationship('Badge')

class DailyLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    log_date = db.Column(db.Date, nullable=False)
    calories_consumed = db.Column(db.Integer, default=0)
    water_ml = db.Column(db.Integer, default=0)
    
    user = db.relationship('User', backref=db.backref('daily_logs', lazy=True))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
