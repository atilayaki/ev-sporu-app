from flask import Blueprint, jsonify, request
import os
import json
import google.generativeai as genai
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
            'goal': p.goal, 'image_url': f'/static/images/{p.slug}.jpg'
        })
    return jsonify({'success': True, 'data': data})

@api_bp.route('/programs/<slug>', methods=['GET'])
def get_program_detail(slug):
    p = Program.query.filter_by(slug=slug).first()
    if not p:
        return jsonify({'success': False, 'message': 'Not found'}), 404
        
    days_dict = {day: [] for day in range(1, p.duration_days + 1)}
    
    for pe in p.exercises:
        day = pe.day_number
        if day in days_dict:
            days_dict[day].append({
                'id': pe.exercise.id,
                'name': pe.exercise.name,
                'slug': pe.exercise.slug,
                'description': pe.exercise.description,
                'instructions': pe.exercise.instructions,
                'muscle_group': pe.exercise.muscle_group,
                'difficulty': pe.exercise.difficulty,
                'image_url': f'/static/images/{pe.exercise.slug}.jpg',
                'sets': pe.sets,
                'reps': pe.reps,
                'rest_seconds': pe.rest_seconds
            })
        
    days_list = []
    for day in sorted(days_dict.keys()):
        days_list.append({
            'day_number': day,
            'exercises': days_dict[day]
        })
        
    return jsonify({
        'success': True, 
        'data': {
            'id': p.id,
            'title': p.title,
            'slug': p.slug,
            'description': p.description,
            'duration_days': p.duration_days,
            'level': p.level,
            'goal': p.goal,
            'image_url': f'/static/images/{p.slug}.jpg',
            'days': days_list
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
            'description': e.description,
            'instructions': e.instructions,
            'image_url': f'/static/images/{e.slug}.jpg'
        })
    return jsonify({'success': True, 'data': data})







@api_bp.route('/ai-coach/generate', methods=['POST'])
def ai_coach_generate():
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        return jsonify({'success': False, 'message': 'API anahtari (GEMINI_API_KEY) bulunamadi. Lutfen .env dosyasina ekleyin.'}), 500
        
    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({'success': False, 'message': 'Prompt gerekli.'}), 400
        
    user_prompt = data['prompt']
    readiness = data.get('readiness', 5)
    
    if readiness < 4:
        adaptation = f"Kullanici bugun cok yorgun hissediyor (Enerji: {readiness}/10). Lutfen eklem yormayan, dusuk tekrarlı, esneme veya aktif dinlenme odakli hafif bir antrenman ver."
    elif readiness > 7:
        adaptation = f"Kullanici bugun cok enerjik! (Enerji: {readiness}/10). Onu gercekten zorlayacak, yuksek tekrarlı, patlayici guc gerektiren zor bir antrenman hazirla."
    else:
        adaptation = f"Kullanicinin enerjisi normal seviyede (Enerji: {readiness}/10). Standart, dengeli bir antrenman hazirla."
        
    user_prompt = f"{user_prompt} \n\n{adaptation}"
    
    exercises = Exercise.query.all()
    exercise_context = []
    for e in exercises:
        exercise_context.append(f"- {e.name} (slug: {e.slug}, kas: {e.muscle_group}, zorluk: {e.difficulty})")
    
    context_str = '\n'.join(exercise_context)
    
    system_instruction = f'''
    Sen birinci sinif bir kisisel antrenorsun (Evde Spor AI Kocu).
    Kullanicinin belirttigi hedeflere, sureye veya kisitlamalara uygun bir antrenman programi ureteceksin.
    Elindeki gecerli egzersizler sunlardir:
    {context_str}
    
    SADECE asagidaki JSON formatinda yanit ver (asla markdown veya baska bir yazi kullanma):
    [
      {{
        "slug": "egzersiz_slug_ismi",
        "sets": 3,
        "reps": 12,
        "rest_seconds": 30
      }}
    ]
    Egzersiz slug'lari sadece sana verilen listeden olmalidir. Sadece bir JSON array dondur.
    '''
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-3.6-flash', system_instruction=system_instruction)
        response = model.generate_content(user_prompt)
        
        response_text = response.text.strip()
        if response_text.startswith('```json'):
            response_text = response_text.replace('```json', '')
        if response_text.startswith('```'):
            response_text = response_text.replace('```', '')
        response_text = response_text.strip()
        
        workout_data = json.loads(response_text)
        
        hydrated_exercises = []
        for item in workout_data:
            ex = Exercise.query.filter_by(slug=item.get('slug')).first()
            if ex:
                hydrated_exercises.append({
                    'id': ex.id,
                    'name': ex.name,
                    'slug': ex.slug,
                    'description': ex.description,
                    'instructions': ex.instructions,
                    'muscle_group': ex.muscle_group,
                    'difficulty': ex.difficulty,
                    'image_url': f'/static/images/{ex.slug}.jpg',
                    'sets': item.get('sets', 3),
                    'reps': item.get('reps', 10),
                    'rest_seconds': item.get('rest_seconds', 30)
                })
                
        return jsonify({
            'success': True,
            'data': {
                'title': 'AI Ozel Antrenman',
                'description': 'Istegine ozel olarak yapay zeka tarafindan tasarlandi.',
                'exercises': hydrated_exercises
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@api_bp.route('/nutrition/analyze', methods=['POST'])
def analyze_nutrition():
    data = request.json
    if not data or 'image_base64' not in data:
        return jsonify({'success': False, 'message': 'Image required'}), 400
        
    image_b64 = data['image_base64']
    prompt = """[SYSTEM: STRICT DETERMINISTIC MODE ENABLED] You are an official Nutrition API. Analyze the image to identify the exact food/drink brand and portion size. Step 1: Identify the item (e.g., Fanta Orange 330ml). Step 2: Retrieve the EXACT official nutritional data for that specific portion. For example, a standard 330ml Fanta Orange is ALWAYS exactly 112 kcal, 0g protein, 28g carbs, 0g fat. If you see a branded item, output its OFFICIAL macros, do not estimate or hallucinate. The "food_name" MUST include the portion size. The "food_name" and "analysis_text" MUST BE IN TURKISH. Reply ONLY with a raw JSON object (no markdown). Schema: { "food_name": "Fanta Portakal (330ml)", "calories": 112, "protein_g": 0, "carbs_g": 28, "fat_g": 0, "analysis_text": "Resmi degerlere gore..." }"""
    
    try:
        import google.generativeai as genai
        # API key should already be configured by now
        model = genai.GenerativeModel('gemini-3.6-flash')
        
        # Decode base64 to bytes
        import base64
        image_bytes = base64.b64decode(image_b64)
        
        # Prepare the image dictionary for Gemini API
        image_part = {
            "mime_type": "image/jpeg",
            "data": image_bytes
        }
        
        response = model.generate_content([image_part, prompt], generation_config={"temperature": 0.0, "top_k": 1})
        response_text = response.text.replace("```json", "").replace("```", "").strip()
        
        import json
        result_json = json.loads(response_text)
        return jsonify({'success': True, 'data': result_json})
    except Exception as e:
        print("Vision API Error:", str(e))
        return jsonify({'success': False, 'message': str(e)}), 500


﻿@api_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    from models import User
    users = User.query.all()
    leaderboard_data = []
    for u in users:
        total_duration = sum([p.duration_spent or 0 for p in u.progress])
        leaderboard_data.append({
            'name': u.name,
            'score': total_duration,
            'badges': len(u.badges)
        })
        
    leaderboard_data = sorted(leaderboard_data, key=lambda x: x['score'], reverse=True)[:10]
    return jsonify({'success': True, 'data': leaderboard_data})

﻿@api_bp.route('/sync-progress', methods=['POST'])
def sync_progress():
    data = request.get_json()
    from models import db, User, UserProgress
    # Dummy user sync (without real JWT auth for now, use simple name matching)
    username = data.get('username')
    duration = data.get('duration_spent', 0)
    calories = data.get('calories_burned', 0)
    readiness = data.get('readiness_score')
    exertion = data.get('perceived_exertion')
    
    if not username:
        return jsonify({'success': False, 'message': 'Username required'})
        
    user = User.query.filter_by(name=username).first()
    if not user:
        # Create user if doesn't exist
        user = User(name=username, email=f"{username}@mobile.com", password="dummy")
        db.session.add(user)
        db.session.commit()
        
    prog = UserProgress(
        user_id=user.id,
        duration_spent=duration,
        calories_burned=calories,
        readiness_score=readiness,
        perceived_exertion=exertion
    )
    db.session.add(prog)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Progress synced!'})
