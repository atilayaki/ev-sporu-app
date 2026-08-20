from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from extensions import db, login_manager
from models import Exercise, Program, ProgramExercise, User, UserProgress, Challenge, UserChallenge, DailyLog, ChallengeDay, ChallengeExercise, UserProgram, Badge, UserBadge
from forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime, date
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key-for-ev-sporu'
    
    basedir = os.path.abspath(os.path.dirname(__name__))
    # Supabase (veya baÅŸka bir PostgreSQL) iÃ§in ortam deÄŸiÅŸkeninden DATABASE_URL al
    db_url = os.environ.get('DATABASE_URL')
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or ('sqlite:///' + os.path.join(basedir, 'instance', 'site.db'))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = "Bu sayfayı görüntülemek için giriş yapmalısınız."
    login_manager.login_message_category = "warning"

    # Removed for Vercel read-only filesystem

    from api import api_bp
    app.register_blueprint(api_bp)

    # DB initialization removed for production
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/bilgi/<slug>')
    def bilgi(slug):
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
            'ilerleme-takibi': {
                'baslik': 'Başarı İçin İlerleme Takibi',
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
        }
        return render_template('info.html', icerik=icerikler[slug])

    @app.route('/egzersizler')
    def exercises():
        query = request.args.get('q', '')
        if query:
            all_exercises = Exercise.query.filter(Exercise.name.ilike(f'%{query}%')).all()
        else:
            all_exercises = Exercise.query.all()
        return render_template('exercises.html', exercises=all_exercises, query=query)

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
        if current_user.is_authenticated:
            user_program = UserProgram.query.filter_by(user_id=current_user.id, program_id=program.id).first()
        return render_template('program_detail.html', program=program, user_program=user_program)

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
        
        # Get exercises for current day
        day_exercises = [pe for pe in program.exercises if pe.day_number == user_program.current_day]
        if not day_exercises:
            flash('Bu gün için egzersiz bulunamadı!', 'error')
            return redirect(url_for('program_detail', slug=slug))
            
        return render_template('workout_player.html', program=program, user_program=user_program, exercises=day_exercises)

    @app.route('/programlar/<slug>/tamamla', methods=['POST'])
    @login_required
    def complete_workout(slug):
        program = Program.query.filter_by(slug=slug).first_or_404()
        user_program = UserProgram.query.filter_by(user_id=current_user.id, program_id=program.id).first_or_404()
        
        # Save progress
        data = request.get_json()
        total_duration = data.get('duration_spent', 0)
        total_calories = data.get('calories_burned', 0)
        
        progress = UserProgress(
            user_id=current_user.id,
            program_id=program.id,
            duration_spent=total_duration,
            calories_burned=total_calories
        )
        db.session.add(progress)
        
        # Update daily log
        today = date.today()
        log = DailyLog.query.filter_by(user_id=current_user.id, log_date=today).first()
        if not log:
            log = DailyLog(user_id=current_user.id, log_date=today, calories_consumed=0, water_ml=0)
            db.session.add(log)
        # Assuming you burn calories, maybe we track it in daily log or let UserProgress handle it.
        # Actually DailyLog has calories_consumed, which is food. Let's just rely on UserProgress for burned.
        
        # Advance current day
        if user_program.current_day < program.duration_days:
            user_program.current_day += 1
            
        # Check for first workout badge
        first_badge = Badge.query.filter_by(name='Ä°lk AdÄ±m').first()
        if first_badge and not UserBadge.query.filter_by(user_id=current_user.id, badge_id=first_badge.id).first():
            ub = UserBadge(user_id=current_user.id, badge_id=first_badge.id)
            db.session.add(ub)
            
        db.session.commit()
        return jsonify({'success': True, 'redirect': url_for('program_detail', slug=slug)})

    @app.route('/liderlik')
    def leaderboard():
        # Liderlik tablosu: En Ã§ok egzersiz sÃ¼resi geÃ§irenler
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

    # --- Kimlik DoÄŸrulama RotalarÄ± ---
    
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
            flash('Başarıyla giriş yaptınız!', 'success')
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
                return redirect(next_page) if next_page else redirect(url_for('index'))
            else:
                flash('Giriş başarısız. Lütfen e-posta ve şifrenizi kontrol edin.', 'danger')
        return render_template('login.html', form=form)

    @app.route('/cikis')
    def logout():
        logout_user()
        return redirect(url_for('index'))

    # --- KullanÄ±cÄ± RotalarÄ± ---

    @app.route('/profil')
    @login_required
    def profile():
        # KullanÄ±cÄ±nÄ±n favorileri
        favorites = current_user.favorites
        # KullanÄ±cÄ±nÄ±n ilerlemeleri (son 10)
        progress = UserProgress.query.filter_by(user_id=current_user.id).order_by(UserProgress.completed_at.desc()).limit(10).all()
        today = date.today()
        today_log = DailyLog.query.filter_by(user_id=current_user.id, log_date=today).first()
        
        # Calculate total exercise duration today
        today_start = datetime.combine(today, datetime.min.time())
        today_progress = UserProgress.query.filter(UserProgress.user_id == current_user.id, UserProgress.completed_at >= today_start).all()
        today_duration = sum([p.duration_spent or 0 for p in today_progress])
        
        active_programs = current_user.active_programs
        user_badges = current_user.badges
        
        return render_template('profile.html', favorites=favorites, progress=progress, today_log=today_log, today_duration=today_duration, active_programs=active_programs, user_badges=user_badges)

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
        
        # OyunlaÅŸtÄ±rma: Seri (Streak) gÃ¼ncellemesi
        today = date.today()
        if current_user.last_active_date != today:
            if current_user.last_active_date:
                diff = (today - current_user.last_active_date).days
                if diff == 1:
                    current_user.current_streak += 1
                else:
                    current_user.current_streak = 1
            else:
                current_user.current_streak = 1
            
            if current_user.current_streak > current_user.longest_streak:
                current_user.longest_streak = current_user.current_streak
                
            current_user.last_active_date = today

        db.session.add(progress)

        db.session.commit()
        flash('Antrenman tamamlandı ve ilerlemeniz kaydedildi! Tebrikler!', 'success')
        return redirect(url_for('exercise_detail', slug=exercise.slug))

    @app.route('/breathe')
    def breathe():
        return render_template('breathe.html')

    @app.route("/api/water", methods=['POST'])
    @login_required
    def update_water():
        data = request.get_json()
        action = data.get('action')
        if action == 'add':
            current_user.water_intake_ml += 250
        elif action == 'reset':
            current_user.water_intake_ml = 0
        db.session.commit()
        return jsonify({'water_intake_ml': current_user.water_intake_ml})

    @app.route("/api/fasting", methods=['POST'])
    @login_required
    def update_fasting():
        data = request.get_json()
        action = data.get('action')
        if action == 'start':
            current_user.fasting_start = datetime.utcnow()
        elif action == 'stop':
            current_user.fasting_start = None
        db.session.commit()
        return jsonify({'fasting_start': current_user.fasting_start.isoformat() if current_user.fasting_start else None})


    @app.route('/quiz', methods=['GET', 'POST'])
    @login_required
    def quiz():
        if request.method == 'POST':
            data = request.get_json()
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
            
        # Get exercises grouped by day
        days = ChallengeDay.query.filter_by(challenge_id=challenge.id).order_by(ChallengeDay.day_number).all()
            
        return render_template('challenge_detail.html', challenge=challenge, user_challenge=user_challenge, days=days)

    @app.route('/api/calories', methods=['POST'])
    @login_required
    def add_calories():
        data = request.get_json()
        amount = data.get('amount', 0)
        today = date.today()
        log = DailyLog.query.filter_by(user_id=current_user.id, log_date=today).first()
        if not log:
            log = DailyLog(user_id=current_user.id, log_date=today, calories_consumed=0)
            db.session.add(log)
        log.calories_consumed += amount
        db.session.commit()
        return jsonify({'calories': log.calories_consumed})

    @app.route('/api/water', methods=['POST'])
    @login_required
    def add_water():
        data = request.get_json()
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
        else:
            log.water_ml += amount
            
        # Check for water badge (2000 ml)
        if log.water_ml >= 2000:
            water_badge = Badge.query.filter_by(name='Su CanavarÄ±').first()
            if water_badge and not UserBadge.query.filter_by(user_id=current_user.id, badge_id=water_badge.id).first():
                ub = UserBadge(user_id=current_user.id, badge_id=water_badge.id)
                db.session.add(ub)
            
        db.session.commit()
        return jsonify({'water_ml': log.water_ml})

    @app.route('/api/fasting', methods=['POST'])
    @login_required
    def toggle_fasting():
        data = request.get_json()
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

    return app


def seed_data():
    exercises = [
        Exercise(name='ÅÄ±nav (Push-up)', slug='sinav-push-up', description='Temel Ã¼st vÃ¼cut egzersizi.', instructions='Yere yÃ¼zÃ¼stÃ¼ uzanÄ±n, ellerinizi omuz geniÅŸliÄŸinde aÃ§arak yeri itin.', muscle_group='GÃ¶ÄŸÃ¼s, Arka Kol', difficulty='Orta', equipment='EkipmansÄ±z', duration_seconds=None, calories_estimate=50),
        Exercise(name='Mekik (Crunch)', slug='mekik-crunch', description='Temel karÄ±n egzersizi.', instructions='SÄ±rtÃ¼stÃ¼ uzanÄ±n, dizlerinizi bÃ¼kÃ¼n ve gÃ¶vdenizi dizlerinize doÄŸru kaldÄ±rÄ±n.', muscle_group='KarÄ±n', difficulty='BaÅŸlangÄ±Ã§', equipment='EkipmansÄ±z', duration_seconds=None, calories_estimate=30),
        Exercise(name='Squat', slug='squat', description='Temel alt vÃ¼cut egzersizi.', instructions='AyaklarÄ±nÄ±zÄ± omuz geniÅŸliÄŸinde aÃ§Ä±n, sandalyeye oturur gibi kalÃ§anÄ±zÄ± geriye vererek Ã§Ã¶mÃ¼n ve kalkÄ±n.', muscle_group='Bacak, KalÃ§a', difficulty='BaÅŸlangÄ±Ã§', equipment='EkipmansÄ±z', duration_seconds=None, calories_estimate=60),
        Exercise(name='Plank', slug='plank', description='TÃ¼m karÄ±n bÃ¶lgesini (core) Ã§alÄ±ÅŸtÄ±ran izometrik hareket.', instructions='Dirsekleriniz ve ayak parmak uÃ§larÄ±nÄ±z Ã¼zerinde yere paralel durun. VÃ¼cudunuz dÃ¼z bir Ã§izgi oluÅŸturmalÄ±.', muscle_group='Core (Merkez)', difficulty='Orta', equipment='EkipmansÄ±z', duration_seconds=60, calories_estimate=20),
        Exercise(name='Jumping Jack', slug='jumping-jack', description='TÃ¼m vÃ¼cudu Ã§alÄ±ÅŸtÄ±ran kardiyo hareketi.', instructions='Ayakta durun, zÄ±playarak ayaklarÄ±nÄ±zÄ± omuz geniÅŸliÄŸinden biraz daha fazla aÃ§Ä±n ve kollarÄ±nÄ±zÄ± baÅŸÄ±nÄ±zÄ±n Ã¼zerinde birleÅŸtirin.', muscle_group='TÃ¼m VÃ¼cut', difficulty='BaÅŸlangÄ±Ã§', equipment='EkipmansÄ±z', duration_seconds=60, calories_estimate=80)
    ]
    db.session.add_all(exercises)
    
    p1 = Program(title='7 GÃ¼nlÃ¼k BaÅŸlangÄ±Ã§', slug='7-gunluk-baslangic', description='Fitness ile yeni tanÄ±ÅŸanlar iÃ§in tÃ¼m vÃ¼cudu aktive eden, hafif tempolu baÅŸlangÄ±Ã§ serisi.', duration_days=7, level='BaÅŸlangÄ±Ã§', goal='Genel Kondisyon')
    db.session.add(p1)
    
    db.session.commit()
    
    # Egzersizleri programa ekle
    ex_squat = Exercise.query.filter_by(slug='squat').first()
    ex_crunch = Exercise.query.filter_by(slug='mekik-crunch').first()
    
    db.session.add(ProgramExercise(program_id=p1.id, exercise_id=ex_squat.id, day_number=1, sets=3, reps=10, rest_seconds=60))
    db.session.add(ProgramExercise(program_id=p1.id, exercise_id=ex_crunch.id, day_number=1, sets=3, reps=15, rest_seconds=45))
    
    db.session.commit()


    if Challenge.query.count() == 0:
        c1 = Challenge(title='21 GÃ¼nlÃ¼k KarÄ±n KasÄ±', slug='21-gun-karin', description='Yaz gelmeden sÄ±msÄ±kÄ± bir karÄ±n iÃ§in her gÃ¼n artan zorluk seviyesiyle 21 gÃ¼nlÃ¼k maraton.', duration_days=21)
        db.session.add(c1)
        db.session.commit()
        
        cd1 = ChallengeDay(challenge_id=c1.id, day_number=1, title='IsÄ±nma ve Temel Core')
        db.session.add(cd1)
        db.session.commit()
        
        ex_crunch = Exercise.query.filter_by(slug='mekik-crunch').first()
        ex_plank = Exercise.query.filter_by(slug='plank').first()
        
        if ex_crunch:
            db.session.add(ChallengeExercise(challenge_day_id=cd1.id, exercise_id=ex_crunch.id, sets=3, reps=15, rest_seconds=30))
        if ex_plank:
            db.session.add(ChallengeExercise(challenge_day_id=cd1.id, exercise_id=ex_plank.id, sets=3, reps=1, rest_seconds=60))
            
        db.session.commit()

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)




