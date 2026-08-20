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
    # Supabase (veya başka bir PostgreSQL) için ortam değişkeninden DATABASE_URL al
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

    os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)

    with app.app_context():
        # Models schema changed so we drop & create or just create_all
        # Since it's dev, dropping is fine if we want clean state, but create_all usually doesn't update existing tables
        # I will leave create_all. SQLite will require a manual drop if schema issues arise.
        print('Before create_all'); db.create_all(); print('After create_all')
        if not Exercise.query.first():
            seed_data()
        
        p_beginner = Program.query.filter_by(title="Başlangıç Seviyesi").first()
        p_core = Program.query.filter_by(title="Karın Kası Odaklı").first()
        p_hiit = Program.query.filter_by(title="Yağ Yakıcı HIIT").first()
        p_quiet = Program.query.filter_by(title="Sessiz Ev Antrenmanı").first()
        p_wall = Program.query.filter_by(title="Başlangıç Duvar Pilatesi").first()
        p_calisthenics = Program.query.filter_by(title="Sıfır Ekipman Kalistenik").first()

        # Helper to safely append
        def add_exercises(prog, slug_list):
            if not prog: return
            for slug in slug_list:
                ex = Exercise.query.filter_by(slug=slug).first()
                if ex and ex not in prog.exercises:
                    prog.exercises.append(ex)

        add_exercises(p_beginner, ['squat', 'plank', 'mekik-crunch'])
        add_exercises(p_core, ['mekik-crunch', 'plank', 'rus-burgusu', 'bisiklet-mekik'])
        add_exercises(p_hiit, ['jumping-jack', 'burpee', 'dag-tirmanisi', 'lunge'])
        add_exercises(p_quiet, ['squat', 'lunge', 'plank', 'duvara-oturma', 'kalca-koprusu'])
        add_exercises(p_wall, ['duvara-oturma', 'kalca-koprusu', 'superman', 'sandalye-dipsi'])
        add_exercises(p_calisthenics, ['sinav-push-up', 'genis-tutus-sinav', 'elmas-sinav', 'havlu-ile-kapi-cekisi'])

        db.session.commit()

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
                    '## Kinetik Zincir ve Fonksiyonellik',
                    'Makinelerde yaptığınız izole hareketler (örneğin Leg Extension) sadece tek bir kas grubunu çalıştırır. Ancak Şınav, Barfiks, Squat gibi hareketler kapalı kinetik zincir hareketleridir. Vücudunuz bir bütün olarak senkronize çalışır, merkez (core) bölgeniz sürekli aktiftir.',
                    '## Aşamalı Yüklenme (Progressive Overload)',
                    'Ağırlık plakası ekleyemediğiniz için gelişimin duracağını düşünüyorsanız yanılıyorsunuz. Vücut ağırlığında "Kaldıraç Etkisi" (leverage) kullanılarak hareketler zorlaştırılır.',
                    '- Normal şınavdan sıkıldınız mı? Ayaklarınızı yükseğe koyun (Decline Push-up).',
                    '- O da mı kolay? Tek el şınav (One-arm Push-up) deneyin.',
                    '- Çift bacak squat kolaylaştıysa Pistol Squat (tek bacak) çalışın.',
                    '## Eklemler İçin Güvenli',
                    'Dışarıdan uygulanan suni bir ağırlık olmadığı için vücudunuz doğal hareket aralığında (ROM) çalışır. Eklemlere binen stres çok daha organik bir şekilde dağılır, sakatlanma riskiniz azalır.'
                ]
            },
            'surekli-gelisim': {
                'baslik': 'Sürekli Gelişim ve Disiplin',
                'ikon': '/static/images/progress_chart_icon.jpg',
                'metin': [
                    'Fitness bir 100 metre koşusu değil, ömür boyu sürecek bir maratondur. İstenilen sonuçları almak sadece fiziksel çaba değil, mental bir dayanıklılık gerektirir.',
                    '## Motivasyon vs Disiplin',
                    'Motivasyon, gece saat 3\'te izlediğiniz bir video sonrası hissettiğiniz "Yarın hayatımı değiştiriyorum" duygusudur. Ancak ertesi gün işten veya okuldan yorgun geldiğinizde o duygu kaybolur. İşte tam bu noktada devreye **Disiplin** girer.',
                    'Disiplin, canınız hiç istemediğinde bile o matın üzerine çıkıp antrenmanı tamamlamaktır. Motivasyon sizi başlatır, disiplin hedefe ulaştırır.',
                    '## Veri Takibi (Tracking)',
                    'Gelişiminizi takip etmiyorsanız kör uçuş yapıyorsunuz demektir.',
                    '- **Antrenman Takibi:** Dün kaç şınav çektiniz? Bugün bir tekrar daha fazla yapabildiniz mi?',
                    '- **Su Tüketimi:** Vücudunuzun %70\'i su. Kaslarınızın toparlanması (recovery) için günlük 2-3 litre su içmeyi alışkanlık haline getirin.',
                    '- **Oruç/Beslenme:** Aralıklı oruç (Intermittent Fasting) veya sadece temiz beslenme (Clean eating) ile vücudunuza giren yakıtı kontrol edin.',
                    'Sistemimizdeki izleme araçlarını kullanarak gelişiminizi her gün kaydedin. Birkaç ay sonra geriye dönüp baktığınızda kat ettiğiniz mesafeye inanamayacaksınız.'
                ]
            }
        }
        
        if slug not in icerikler:
            flash('Aradığınız sayfa bulunamadı.', 'danger')
            return redirect(url_for('index'))
            
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
        first_badge = Badge.query.filter_by(name='İlk Adım').first()
        if first_badge and not UserBadge.query.filter_by(user_id=current_user.id, badge_id=first_badge.id).first():
            ub = UserBadge(user_id=current_user.id, badge_id=first_badge.id)
            db.session.add(ub)
            
        db.session.commit()
        return jsonify({'success': True, 'redirect': url_for('program_detail', slug=slug)})

    @app.route('/liderlik')
    def leaderboard():
        # Liderlik tablosu: En çok egzersiz süresi geçirenler
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
            flash('Hesabınız oluşturuldu! Şimdi giriş yapabilirsiniz.', 'success')
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

    # --- Kullanıcı Rotaları ---

    @app.route('/profil')
    @login_required
    def profile():
        # Kullanıcının favorileri
        favorites = current_user.favorites
        # Kullanıcının ilerlemeleri (son 10)
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
        
        # Oyunlaştırma: Seri (Streak) güncellemesi
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
            water_badge = Badge.query.filter_by(name='Su Canavarı').first()
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
        Exercise(name='Şınav (Push-up)', slug='sinav-push-up', description='Temel üst vücut egzersizi.', instructions='Yere yüzüstü uzanın, ellerinizi omuz genişliğinde açarak yeri itin.', muscle_group='Göğüs, Arka Kol', difficulty='Orta', equipment='Ekipmansız', duration_seconds=None, calories_estimate=50),
        Exercise(name='Mekik (Crunch)', slug='mekik-crunch', description='Temel karın egzersizi.', instructions='Sırtüstü uzanın, dizlerinizi bükün ve gövdenizi dizlerinize doğru kaldırın.', muscle_group='Karın', difficulty='Başlangıç', equipment='Ekipmansız', duration_seconds=None, calories_estimate=30),
        Exercise(name='Squat', slug='squat', description='Temel alt vücut egzersizi.', instructions='Ayaklarınızı omuz genişliğinde açın, sandalyeye oturur gibi kalçanızı geriye vererek çömün ve kalkın.', muscle_group='Bacak, Kalça', difficulty='Başlangıç', equipment='Ekipmansız', duration_seconds=None, calories_estimate=60),
        Exercise(name='Plank', slug='plank', description='Tüm karın bölgesini (core) çalıştıran izometrik hareket.', instructions='Dirsekleriniz ve ayak parmak uçlarınız üzerinde yere paralel durun. Vücudunuz düz bir çizgi oluşturmalı.', muscle_group='Core (Merkez)', difficulty='Orta', equipment='Ekipmansız', duration_seconds=60, calories_estimate=20),
        Exercise(name='Jumping Jack', slug='jumping-jack', description='Tüm vücudu çalıştıran kardiyo hareketi.', instructions='Ayakta durun, zıplayarak ayaklarınızı omuz genişliğinden biraz daha fazla açın ve kollarınızı başınızın üzerinde birleştirin.', muscle_group='Tüm Vücut', difficulty='Başlangıç', equipment='Ekipmansız', duration_seconds=60, calories_estimate=80)
    ]
    db.session.add_all(exercises)
    
    p1 = Program(title='7 Günlük Başlangıç', slug='7-gunluk-baslangic', description='Fitness ile yeni tanışanlar için tüm vücudu aktive eden, hafif tempolu başlangıç serisi.', duration_days=7, level='Başlangıç', goal='Genel Kondisyon')
    db.session.add(p1)
    
    db.session.commit()
    
    # Egzersizleri programa ekle
    ex_squat = Exercise.query.filter_by(slug='squat').first()
    ex_crunch = Exercise.query.filter_by(slug='mekik-crunch').first()
    
    db.session.add(ProgramExercise(program_id=p1.id, exercise_id=ex_squat.id, day_number=1, sets=3, reps=10, rest_seconds=60))
    db.session.add(ProgramExercise(program_id=p1.id, exercise_id=ex_crunch.id, day_number=1, sets=3, reps=15, rest_seconds=45))
    
    db.session.commit()


    if Challenge.query.count() == 0:
        c1 = Challenge(title='21 Günlük Karın Kası', slug='21-gun-karin', description='Yaz gelmeden sımsıkı bir karın için her gün artan zorluk seviyesiyle 21 günlük maraton.', duration_days=21)
        db.session.add(c1)
        db.session.commit()
        
        cd1 = ChallengeDay(challenge_id=c1.id, day_number=1, title='Isınma ve Temel Core')
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
