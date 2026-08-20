from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Program, Exercise, UserProgress
import jwt
import datetime

api_bp = Blueprint('api', __name__, url_prefix='/api')
SECRET_KEY = 'dev-secret-key-for-ev-sporu' # Should match app.py

@api_bp.route('/programs', methods=['GET'])
def get_programs():
    programs = Program.query.all()
    data = []
    for p in programs:
        data.append({
            'id': p.id,
            'title': p.title,
            'slug': p.slug,
            'description': p.description,
            'level': p.level,
            'duration_days': p.duration_days,
            'goal': p.goal
        })
    return jsonify({'success': True, 'data': data})

@api_bp.route('/programs/<slug>', methods=['GET'])
def get_program_detail(slug):
    p = Program.query.filter_by(slug=slug).first()
    if not p:
        return jsonify({'success': False, 'message': 'Not found'}), 404
        
    exercises = []
    for pe in p.exercises:
        exercises.append({
            'id': pe.id,
            'name': pe.name,
            'slug': pe.slug,
            'description': pe.description,
            'muscle_group': pe.muscle_group,
            'difficulty': pe.difficulty,
            'image_url': f'/static/images/{pe.slug}.jpg'
        })
        
    return jsonify({
        'success': True, 
        'data': {
            'id': p.id,
            'title': p.title,
            'description': p.description,
            'exercises': exercises
        }
    })

@api_bp.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    data = []
    for e in exercises:
        data.append({
            'id': e.id,
            'name': e.name,
            'slug': e.slug,
            'muscle_group': e.muscle_group,
            'difficulty': e.difficulty,
            'image_url': f'/static/images/{e.slug}.jpg'
        })
    return jsonify({'success': True, 'data': data})
