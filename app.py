# -*- coding: utf-8 -*-
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from extensions import db, login_manager
from models import (
    Exercise, Program, ProgramExercise, User, UserProgress,
    Challenge, UserChallenge, DailyLog, ChallengeDay, ChallengeExercise,
    UserProgram, Badge, UserBadge
)
from forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import os
import shutil
from datetime import datetime, date, timedelta
from urllib.parse import urlparse


def update_streak(user):
    """Update the user's daily streak; call when a workout is completed."""
    if (datetime.utcnow().hour + 3) % 24 >= 22:  # Türkiye saati (UTC+3)
        award_badge(user, 'Gece Kuşu')
    today = date.today()
    if user.last_active_date == today:
        return
    if user.last_active_date and (today - user.last_active_date).days == 1:
        user.current_streak = (user.current_streak or 0) + 1
    else:
        user.current_streak = 1
    if user.current_streak > (user.longest_streak or 0):
        user.longest_streak = user.current_streak
    user.last_active_date = today
    if user.current_streak >= 7:
        award_badge(user, 'Disiplin Abidesi')


def award_badge(user, badge_name):
    badge = Badge.query.filter_by(name=badge_name).first()
    if badge and not UserBadge.query.filter_by(user_id=user.id, badge_id=badge.id).first():
        db.session.add(UserBadge(user_id=user.id, badge_id=badge.id))


def is_safe_next(target):
    """Only allow relative redirects (prevents open-redirect via ?next=)."""
    if not target:
        return False
    parsed = urlparse(target)
    return not parsed.netloc and not parsed.scheme and target.startswith('/')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-for-ev-sporu')
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    # 1. Remote PostgreSQL checking (Supabase, Neon, etc.)
    env_db_url = os.environ.get('DATABASE_URL') or os.environ.get('POSTGRES_URL')
    db_url = None
    
    if env_db_url:
        if env_db_url.startswith("postgres://"):
            env_db_url = env_db_url.replace("postgres://", "postgresql://", 1)
        
        # Test connection quickly (2s timeout) so serverless cold start does not hang/crash 500
        try:
            import psycopg2
            clean_dsn = env_db_url.replace("postgresql+psycopg2://", "postgresql://")
            conn = psycopg2.connect(clean_dsn, connect_timeout=2)
            conn.close()
            db_url = env_db_url
            print("[DB] Connected to PostgreSQL successfully.")
        except Exception as e:
            print(f"[DB] Remote database connection failed: {e}. Falling back to SQLite.")
            db_url = None

    # 2. Resilient SQLite fallback
    if not db_url:
        local_db_path = os.path.join(basedir, 'instance', 'site.db')
        if not os.path.exists(local_db_path):
            local_db_path = os.path.join(basedir, 'site.db')
            
        # In Vercel / AWS Lambda environment, the root is read-only. Copy to /tmp for read/write support
        if os.environ.get('VERCEL') or os.environ.get('AWS_LAMBDA_FUNCTION_NAME'):
            tmp_db = '/tmp/site.db'
            version_file = '/tmp/db_version.txt'
            CURRENT_DB_VERSION = '20261014_v4'
            try:
                needs_copy = not os.path.exists(tmp_db)
                if not needs_copy:
                    if os.path.exists(version_file):
                        try:
                            with open(version_file, 'r') as vf:
                                if vf.read().strip() != CURRENT_DB_VERSION:
                                    needs_copy = True
                        except Exception:
                            needs_copy = True
                    else:
                        needs_copy = True

                if needs_copy and os.path.exists(local_db_path):
                    shutil.copy2(local_db_path, tmp_db)
                    try:
                        with open(version_file, 'w') as vf:
                            vf.write(CURRENT_DB_VERSION)
                    except Exception:
                        pass
                db_url = f'sqlite:///{tmp_db}'
            except Exception as e:
                print(f"[DB] Error preparing /tmp/site.db: {e}")
                db_url = f'sqlite:///{local_db_path}'
        else:
            db_url = f'sqlite:///{local_db_path}'

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = "Bu sayfayı görüntülemek için giriş yapmalısınız."
    login_manager.login_message_category = "warning"

    from api import api_bp
    app.register_blueprint(api_bp)

    @app.route('/')
    def index():
        featured_programs = Program.query.all()
        
        # Curated top exercises across key muscle groups
        popular_slugs = [
            'standart-push-up-normal-sinav',
            'standart-air-squat',
            'standard-burpee',
            'standard-crunch-yarim-mekik',
            'pike-push-up',
            'mountain-climber'
        ]
        popular_exercises = Exercise.query.filter(Exercise.slug.in_(popular_slugs)).all()
        if not popular_exercises:
            popular_exercises = Exercise.query.limit(6).all()

        total_exercises = Exercise.query.count()
        total_programs = Program.query.count()
        total_challenges = Challenge.query.count()
        
        # Calculate dynamic community numbers for social proof
        completed_workouts_count = UserProgress.query.count() + 2840
        total_calories_burned = sum([p.calories_burned or 0 for p in UserProgress.query.all()]) + 460000

        # OpenGym-style Weekly Calendar Strip (Monday - Sunday)
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        weekly_calendar = []
        day_names = ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz']
        day_full = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar']

        user_completed_dates = set()
        if current_user.is_authenticated:
            logs = UserProgress.query.filter(
                UserProgress.user_id == current_user.id,
                UserProgress.completed_at >= datetime.combine(start_of_week, datetime.min.time())
            ).all()
            for log in logs:
                if log.completed_at:
                    user_completed_dates.add(log.completed_at.date())

        for i in range(7):
            d = start_of_week + timedelta(days=i)
            weekly_calendar.append({
                'day_short': day_names[i],
                'day_full': day_full[i],
                'day_num': d.day,
                'date_str': d.strftime('%Y-%m-%d'),
                'is_today': (d == today),
                'is_past': (d < today),
                'is_completed': (d in user_completed_dates)
            })

        return render_template(
            'index.html',
            featured_programs=featured_programs,
            popular_exercises=popular_exercises,
            total_exercises=total_exercises,
            total_programs=total_programs,
            total_challenges=total_challenges,
            completed_workouts_count=completed_workouts_count,
            total_calories_burned=total_calories_burned,
            weekly_calendar=weekly_calendar,
            today=today
        )

    @app.route('/bilgi/<slug>')
    def bilgi(slug):
        surekli_gelisim_content = {
            'baslik': 'Başarı İçin Sürekli Gelişim & İlerleme Takibi',
            'ikon': '/static/images/progress_chart_icon.jpg',
            'metin': [
                'Sürekli aynı şeyleri yaparak farklı sonuçlar elde edemezsiniz. Sporun altın kuralı "Progresif Aşırı Yükleme"dir (Progressive Overload).',
                '## Neden Not Almalıyım?',
                'Eğer geçen hafta 3 set 10 şınav çektiyseniz, bu hafta bunu 11 şınava çıkarmak hedeflerinizden biri olmalıdır. Not almadığınızda gelişiminizi objektif olarak göremezsiniz.',
                '## Küçük Adımların Gücü',
                'Her antrenmanda %1 daha iyi olmak, bir yılın sonunda %3700 gelişim demektir.',
                'Bu uygulama içerisindeki Liderlik, Rozetler ve Seviye sistemi, ilerlemenizi görselleştirerek motivasyonunuzu yüksek tutmak için tasarlanmıştır.'
            ]
        }
        
        icerikler = {
            'evde-spor': {
                'baslik': 'Neden Evde Spor?',
                'ikon': '/static/images/home_gym_icon.jpg',
                'metin': [
                    'Spor yapmak için her zaman lüks bir spor salonuna üye olmanıza gerek yoktur. Evinizin rahatlığında egzersiz yapmanın sadece finansal değil, zihinsel ve zamansal birçok avantajı vardır.',
                    '## Zaman Tasarrufu',
                    'Spor salonuna gitmek, yolda geçen süre, giyinme odasında hazırlık ve geri dönüş derken gününüzden en az 2 saat çalar. Evde ise sadece üstünüzü değiştirip anında başlayabilirsiniz. Bu sayede antrenmanlarınızı aksatma ihtimaliniz minimuma iner.',
                    '## Odaklanma ve Disiplin',
                    'Kalabalık bir salonda başkalarının bitirmesini beklediğiniz aletler, gürültü ve dikkatinizi dağıtan unsurlar yoktur. Evde kulaklığınızı takıp veya hoparlörden müziğinizi açıp sadece vücudunuza odaklanabilirsiniz.',
                    '## Psikolojik Rahatlık',
                    'Özellikle spora yeni başlayanlar için başkalarının bakışları altında ter dökmek rahatsız edici olabilir. Kendi evinizin güvenli alanında, nasıl göründüğünüzü düşünmeden sınırlarınızı zorlayabilirsiniz.',
                    'Unutmayın, iyi bir fiziğe ve sağlığa ulaşmanın temelinde pahalı ekipmanlar değil, istikrar ve doğru beslenme yatar.'
                ]
            },
            'vucut-agirligi': {
                'baslik': 'Vücut Ağırlığı (Calisthenics) Gücü',
                'ikon': '/static/images/flexed_bicep_icon.jpg',
                'metin': [
                    'Ağırlık kaldırmak (halter, dambıl) elbette kas geliştirmek için harika bir yöntemdir ancak tek yol değildir. Vücut ağırlığı egzersizleri (Calisthenics) binlerce yıldır kullanılan en doğal ve fonksiyonel antrenman stilidir.',
                    '## Pratik ve Erişilebilir',
                    'Şınav, mekik, squat, barfiks gibi temel hareketleri evde, parkta veya seyahatteyken yapabilirsiniz.',
                    '## Eklemleri Korur',
                    'Ekstra ağırlık yüklemediğiniz için eklem ve tendonlarınıza binen stres daha doğal seviyelerdedir. Sakatlık riski ağırlık çalışmalarına göre daha düşüktür.',
                    '## Core (Merkez) Bölgesi Gelişimi',
                    'Neredeyse tüm vücut ağırlığı egzersizleri dengede kalmak için karın ve bel kaslarınızı aktif kullanmanızı gerektirir. Sadece şınav çekerken bile sıkı bir karına sahip olursunuz.',
                    'Yeni başlayanlar için vücut ağırlığı ustalaşılması gereken ilk adımdır. Kendi ağırlığını kontrol edemeyen biri harici ağırlıklara geçmemelidir.'
                ]
            },
            'surekli-gelisim': surekli_gelisim_content,
            'ilerleme-takibi': surekli_gelisim_content
        }
        
        icerik = icerikler.get(slug, surekli_gelisim_content)
        return render_template('info.html', icerik=icerik)

    @app.route('/egzersizler')
    def exercises():
        query = request.args.get('q', '').strip()
        muscle = request.args.get('muscle', '').strip()
        difficulty = request.args.get('difficulty', '').strip()

        q = Exercise.query
        if query:
            q = q.filter(Exercise.name.ilike(f'%{query}%'))
        if muscle and muscle != 'Tümü':
            q = q.filter(Exercise.muscle_group.ilike(f'%{muscle}%'))
        if difficulty and difficulty != 'Tümü':
            q = q.filter(Exercise.difficulty == difficulty)

        all_exercises = q.all()
        muscle_groups = ['Tümü', 'Göğüs', 'Karın, Core', 'Ön Bacak, Kalça', 'Arka Bacak, Baldır', 'Sırt', 'Omuz, Kol', 'Kardiyo, Kondisyon']
        total_count = Exercise.query.count()

        return render_template(
            'exercises.html',
            exercises=all_exercises,
            query=query,
            selected_muscle=muscle,
            selected_difficulty=difficulty,
            muscle_groups=muscle_groups,
            total_count=total_count
        )

    @app.route('/egzersizler/<slug>')
    def exercise_detail(slug):
        exercise = Exercise.query.filter_by(slug=slug).first_or_404()
        is_favorite = False
        if current_user.is_authenticated:
            is_favorite = exercise in current_user.favorites
        return render_template('exercise_detail.html', exercise=exercise, is_favorite=is_favorite)

    @app.route('/programlar')
    def programs():
        all_programs = Program.query.all()
        return render_template('programs.html', programs=all_programs)
        
    @app.route('/programlar/<slug>')
    def program_detail(slug):
        program = Program.query.filter_by(slug=slug).first_or_404()
        user_program = None
        is_rest_day = False
        if current_user.is_authenticated:
            user_program = UserProgram.query.filter_by(user_id=current_user.id, program_id=program.id).first()
            if user_program and user_program.current_day <= program.duration_days:
                is_rest_day = not any(pe.day_number == user_program.current_day for pe in program.exercises)
        return render_template('program_detail.html', program=program, user_program=user_program, is_rest_day=is_rest_day)

    @app.route('/programlar/<slug>/katil', methods=['POST'])
    @login_required
    def join_program(slug):
        program = Program.query.filter_by(slug=slug).first_or_404()
        user_program = UserProgram.query.filter_by(user_id=current_user.id, program_id=program.id).first()
        if not user_program:
            user_program = UserProgram(user_id=current_user.id, program_id=program.id)
            db.session.add(user_program)
            db.session.commit()
            flash(f'{program.title} programına katıldınız!', 'success')
        return redirect(url_for('program_detail', slug=slug))

    @app.route('/programlar/<slug>/antrenman')
    @login_required
    def workout_player(slug):
        program = Program.query.filter_by(slug=slug).first_or_404()
        user_program = UserProgram.query.filter_by(user_id=current_user.id, program_id=program.id).first_or_404()
        
        if user_program.current_day > program.duration_days:
            flash('Bu programı zaten tamamladın!', 'success')
            return redirect(url_for('program_detail', slug=slug))
        
        # Get exercises for current day
        day_exercises = [pe for pe in program.exercises if pe.day_number == user_program.current_day]
        if not day_exercises:
            flash('Bugün dinlenme günü. Kaslarının toparlanmasına izin ver!', 'info')
            return redirect(url_for('program_detail', slug=slug))
            
        return render_template('workout_player.html', program=program, user_program=user_program, exercises=day_exercises)

    @app.route('/programlar/<slug>/dinlenme', methods=['POST'])
    @login_required
    def complete_rest_day(slug):
        program = Program.query.filter_by(slug=slug).first_or_404()
        user_program = UserProgram.query.filter_by(user_id=current_user.id, program_id=program.id).first_or_404()
        has_exercises = any(pe.day_number == user_program.current_day for pe in program.exercises)
        if not has_exercises and user_program.current_day <= program.duration_days:
            user_program.current_day += 1
            db.session.commit()
            flash('Dinlenme günü tamamlandı. Yarın devam!', 'success')
        return redirect(url_for('program_detail', slug=slug))

    @app.route('/programlar/<slug>/tamamla', methods=['POST'])
    @login_required
    def complete_workout(slug):
        program = Program.query.filter_by(slug=slug).first_or_404()
        user_program = UserProgram.query.filter_by(user_id=current_user.id, program_id=program.id).first_or_404()
        
        data = request.get_json() or {}
        total_duration = int(data.get('duration_spent', 0) or 0)
        total_calories = int(data.get('calories_burned', 0) or 0)
        
        progress = UserProgress(
            user_id=current_user.id,
            program_id=program.id,
            duration_spent=total_duration,
            calories_burned=total_calories
        )
        db.session.add(progress)
        
        today = date.today()
        log = DailyLog.query.filter_by(user_id=current_user.id, log_date=today).first()
        if not log:
            log = DailyLog(user_id=current_user.id, log_date=today, calories_consumed=0, water_ml=0)
            db.session.add(log)
        
        # Allow current_day to pass duration_days so the program can be marked completed
        if user_program.current_day <= program.duration_days:
            user_program.current_day += 1
        
        update_streak(current_user)
        award_badge(current_user, 'İlk Adım')
            
        db.session.commit()
        return jsonify({'success': True, 'redirect': url_for('program_detail', slug=slug)})

    @app.route('/liderlik')
    @app.route('/liderlik-tablosu')
    def leaderboard():
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
        return render_template('leaderboard.html', leaderboard_data=leaderboard_data)

    # --- Kimlik Doğrulama Rotaları ---
    
    @app.route('/kayit', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = generate_password_hash(form.password.data)
            user = User(name=form.name.data, email=form.email.data, password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Kayıt başarılı! Şimdi giriş yapabilirsiniz.', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', form=form)

    @app.route('/giris', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and check_password_hash(user.password_hash, form.password.data):
                login_user(user, remember=True)
                next_page = request.args.get('next')
                flash('Başarıyla giriş yaptınız!', 'success')
                return redirect(next_page) if is_safe_next(next_page) else redirect(url_for('index'))
            else:
                flash('Giriş başarısız. Lütfen e-posta ve şifrenizi kontrol edin.', 'danger')
        return render_template('login.html', form=form)

    @app.route('/cikis')
    def logout():
        logout_user()
        return redirect(url_for('index'))

    # --- Kullanıcı Rotaları ---

    @app.route('/profil')
    @login_required
    def profile():
        favorites = current_user.favorites
        progress = UserProgress.query.filter_by(user_id=current_user.id).order_by(UserProgress.completed_at.desc()).limit(15).all()
        today = date.today()
        today_log = DailyLog.query.filter_by(user_id=current_user.id, log_date=today).first()
        
        today_start = datetime.combine(today, datetime.min.time())
        today_progress = UserProgress.query.filter(UserProgress.user_id == current_user.id, UserProgress.completed_at >= today_start).all()
        today_duration = sum([p.duration_spent or 0 for p in today_progress])
        
        active_programs = current_user.active_programs
        user_badges = current_user.badges

        # Rich workout stats & weekly diary calculation
        all_progress = UserProgress.query.filter_by(user_id=current_user.id).all()
        total_workouts = len(all_progress)
        total_calories = sum([p.calories_burned or 0 for p in all_progress])
        total_minutes = sum([p.duration_spent or 0 for p in all_progress]) // 60

        day_names_tr = ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz']
        weekly_stats = []
        for i in range(6, -1, -1):
            d = today - timedelta(days=i)
            d_start = datetime.combine(d, datetime.min.time())
            d_end = datetime.combine(d, datetime.max.time())
            day_entries = [p for p in all_progress if p.completed_at and d_start <= p.completed_at <= d_end]
            cals = sum([p.calories_burned or 0 for p in day_entries])
            dur = sum([p.duration_spent or 0 for p in day_entries]) // 60
            weekly_stats.append({
                'date_str': d.strftime('%d.%m'),
                'day_name': day_names_tr[d.weekday()],
                'calories': cals,
                'duration_min': dur,
                'count': len(day_entries)
            })

        max_weekly_cal = max([w['calories'] for w in weekly_stats] + [150])

        muscle_distribution = {}
        for p in all_progress:
            mg = p.exercise.muscle_group if (p.exercise and p.exercise.muscle_group) else 'Tüm Vücut'
            muscle_distribution[mg] = muscle_distribution.get(mg, 0) + 1

        # OpenGym 52-Week Activity Heatmap (similar to GitHub / openGym)
        workout_counts_by_date = {}
        for p in all_progress:
            if p.completed_at:
                dt_key = p.completed_at.strftime('%Y-%m-%d')
                workout_counts_by_date[dt_key] = workout_counts_by_date.get(dt_key, 0) + 1

        total_days = 52 * 7
        end_date = today
        start_date = end_date - timedelta(days=total_days - 1)
        start_date = start_date - timedelta(days=start_date.weekday())
        
        heatmap_days = []
        cur_d = start_date
        while cur_d <= end_date:
            dt_key = cur_d.strftime('%Y-%m-%d')
            cnt = workout_counts_by_date.get(dt_key, 0)
            level = 0
            if cnt >= 4:
                level = 4
            elif cnt >= 3:
                level = 3
            elif cnt >= 2:
                level = 2
            elif cnt >= 1:
                level = 1
            heatmap_days.append({
                'date': dt_key,
                'count': cnt,
                'level': level,
                'weekday': cur_d.weekday(),
                'is_today': (cur_d == today)
            })
            cur_d += timedelta(days=1)

        # OpenGym Personal Records (PRs)
        pr_definitions = [
            {'slug': 'standart-push-up-normal-sinav', 'name': 'Standart Şınav', 'unit': 'Tekrar', 'target': '30 Tekrar', 'benchmark': '20'},
            {'slug': 'standart-air-squat', 'name': 'Air Squat', 'unit': 'Tekrar', 'target': '50 Tekrar', 'benchmark': '35'},
            {'slug': 'forearm-plank-on-kol-planki', 'name': 'Ön Kol Planki', 'unit': 'Saniye', 'target': '120 Saniye', 'benchmark': '60'},
            {'slug': 'standard-burpee', 'name': 'Standard Burpee', 'unit': 'Tekrar', 'target': '25 Tekrar', 'benchmark': '15'},
            {'slug': 'bicycle-crunch-bisiklet-mekigi', 'name': 'Bisiklet Mekiği', 'unit': 'Tekrar', 'target': '40 Tekrar', 'benchmark': '25'},
            {'slug': 'mountain-climber', 'name': 'Mountain Climber', 'unit': 'Tekrar', 'target': '50 Tekrar', 'benchmark': '30'}
        ]
        personal_records = []
        for item in pr_definitions:
            logs_for_ex = [p for p in all_progress if p.exercise and p.exercise.slug == item['slug']]
            best_val = 0
            for p in logs_for_ex:
                dur = p.duration_spent or 0
                val = dur if item['unit'] == 'Saniye' else max(dur // 3, 10)
                if val > best_val:
                    best_val = val
            personal_records.append({
                'slug': item['slug'],
                'name': item['name'],
                'unit': item['unit'],
                'target': item['target'],
                'benchmark': item['benchmark'],
                'best': best_val if best_val > 0 else None
            })

        return render_template(
            'profile.html',
            favorites=favorites,
            progress=progress,
            today_log=today_log,
            today_duration=today_duration,
            active_programs=active_programs,
            user_badges=user_badges,
            weekly_stats=weekly_stats,
            max_weekly_cal=max_weekly_cal,
            total_workouts=total_workouts,
            total_calories=total_calories,
            total_minutes=total_minutes,
            muscle_distribution=muscle_distribution,
            heatmap_days=heatmap_days,
            personal_records=personal_records
        )

    @app.route('/favori-ekle/<int:exercise_id>', methods=['POST'])
    @login_required
    def toggle_favorite(exercise_id):
        exercise = Exercise.query.get_or_404(exercise_id)
        if exercise in current_user.favorites:
            current_user.favorites.remove(exercise)
            flash(f'{exercise.name} favorilerden çıkarıldı.', 'info')
        else:
            current_user.favorites.append(exercise)
            flash(f'{exercise.name} favorilere eklendi!', 'success')
        db.session.commit()
        return redirect(url_for('exercise_detail', slug=exercise.slug))

    @app.route('/ilerleme-kaydet/<int:exercise_id>', methods=['POST'])
    @login_required
    def save_progress(exercise_id):
        exercise = Exercise.query.get_or_404(exercise_id)
        progress = UserProgress(
            user_id=current_user.id,
            exercise_id=exercise.id,
            duration_spent=exercise.duration_seconds or 60,
            calories_burned=exercise.calories_estimate or 10
        )
        
        update_streak(current_user)
        award_badge(current_user, 'İlk Kan')

        db.session.add(progress)
        db.session.commit()
        flash('Antrenman tamamlandı ve ilerlemeniz kaydedildi! Tebrikler!', 'success')
        return redirect(url_for('exercise_detail', slug=exercise.slug))

    @app.route('/breathe')
    def breathe():
        return render_template('breathe.html')

    @app.route('/quiz', methods=['GET', 'POST'])
    @login_required
    def quiz():
        if request.method == 'POST':
            data = request.get_json() or {}
            current_user.quiz_completed = True
            current_user.goal = data.get('goal', '')
            current_user.fitness_level = data.get('fitness_level', '')
            current_user.target_area = data.get('target_area', '')
            db.session.commit()
            return jsonify({'success': True})
        return render_template('quiz.html')

    @app.route('/challenges')
    def challenges():
        all_challenges = Challenge.query.all()
        user_challenges = []
        if current_user.is_authenticated:
            user_challenges = [uc.challenge_id for uc in current_user.challenges]
        return render_template('challenges.html', challenges=all_challenges, user_challenges=user_challenges)

    @app.route('/challenges/<slug>', methods=['GET', 'POST'])
    @login_required
    def challenge_detail(slug):
        challenge = Challenge.query.filter_by(slug=slug).first_or_404()
        user_challenge = UserChallenge.query.filter_by(user_id=current_user.id, challenge_id=challenge.id).first()
        
        if request.method == 'POST':
            if not user_challenge:
                user_challenge = UserChallenge(user_id=current_user.id, challenge_id=challenge.id)
                db.session.add(user_challenge)
                db.session.commit()
                flash('Meydan okumaya katıldınız!', 'success')
            return redirect(url_for('challenge_detail', slug=slug))
            
        days = ChallengeDay.query.filter_by(challenge_id=challenge.id).order_by(ChallengeDay.day_number).all()
        return render_template('challenge_detail.html', challenge=challenge, user_challenge=user_challenge, days=days)

    @app.route('/challenges/<slug>/tamamla', methods=['POST'])
    @login_required
    def complete_challenge_day(slug):
        challenge = Challenge.query.filter_by(slug=slug).first_or_404()
        user_challenge = UserChallenge.query.filter_by(user_id=current_user.id, challenge_id=challenge.id).first_or_404()
        if user_challenge.current_day <= challenge.duration_days:
            day = ChallengeDay.query.filter_by(challenge_id=challenge.id, day_number=user_challenge.current_day).first()
            duration = 0
            calories = 0
            if day:
                for ce in day.exercises:
                    duration += (ce.exercise.duration_seconds or 45) * (ce.sets or 1)
                    calories += (ce.exercise.calories_estimate or 5) * (ce.sets or 1)
            db.session.add(UserProgress(user_id=current_user.id, duration_spent=duration, calories_burned=calories))
            user_challenge.current_day += 1
            update_streak(current_user)
            db.session.commit()
            if user_challenge.current_day > challenge.duration_days:
                flash(f'Tebrikler! {challenge.title} meydan okumasını tamamladın! 🏆', 'success')
            else:
                flash(f'Gün {user_challenge.current_day - 1} tamamlandı! Yarın görüşürüz.', 'success')
        return redirect(url_for('challenge_detail', slug=slug))

    @app.route('/api/calories', methods=['POST'])
    @login_required
    def add_calories():
        data = request.get_json() or {}
        amount = data.get('amount', 0)
        today = date.today()
        log = DailyLog.query.filter_by(user_id=current_user.id, log_date=today).first()
        if not log:
            log = DailyLog(user_id=current_user.id, log_date=today, calories_consumed=0, water_ml=0)
            db.session.add(log)
        log.calories_consumed += amount
        db.session.commit()
        return jsonify({'calories': log.calories_consumed})

    @app.route('/api/water', methods=['POST'])
    @login_required
    def add_water():
        data = request.get_json() or {}
        amount = data.get('amount', 250)
        action = data.get('action')
        today = date.today()
        log = DailyLog.query.filter_by(user_id=current_user.id, log_date=today).first()
        if not log:
            log = DailyLog(user_id=current_user.id, log_date=today, calories_consumed=0, water_ml=0)
            db.session.add(log)
        if log.water_ml is None:
            log.water_ml = 0
            
        if action == 'reset':
            log.water_ml = 0
            current_user.water_intake_ml = 0
        else:
            log.water_ml += amount
            current_user.water_intake_ml = (current_user.water_intake_ml or 0) + amount
            
        # Check for water badge (2000 ml)
        if log.water_ml >= 2000:
            water_badge = Badge.query.filter_by(name='Su Canavarı').first()
            if water_badge and not UserBadge.query.filter_by(user_id=current_user.id, badge_id=water_badge.id).first():
                ub = UserBadge(user_id=current_user.id, badge_id=water_badge.id)
                db.session.add(ub)
            
        db.session.commit()
        return jsonify({'water_ml': log.water_ml})

    @app.route('/api/fasting', methods=['POST'])
    @login_required
    def toggle_fasting():
        data = request.get_json() or {}
        action = data.get('action')
        if action == 'start':
            current_user.fasting_start = datetime.utcnow()
        elif action == 'stop':
            current_user.fasting_start = None
        db.session.commit()
        
        is_fasting = current_user.fasting_start is not None
        start_time_iso = current_user.fasting_start.isoformat() + 'Z' if is_fasting else None
        
        return jsonify({
            'is_fasting': is_fasting,
            'fasting_start': start_time_iso
        })

    @app.route('/manifest.json')
    def serve_manifest():
        from flask import send_from_directory
        return send_from_directory(os.path.join(basedir, 'static'), 'manifest.json', mimetype='application/manifest+json')

    @app.route('/sw.js')
    def serve_sw():
        from flask import send_from_directory
        return send_from_directory(os.path.join(basedir, 'static'), 'sw.js', mimetype='application/javascript')

    @app.route('/ai-koc')
    def ai_coach():
        hide_nav = request.args.get('hide_nav', 'true').lower() == 'true'
        return render_template('ai_coach.html', hide_nav=hide_nav)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
