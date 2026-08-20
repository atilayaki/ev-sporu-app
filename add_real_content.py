from app import create_app
from extensions import db
from models import Exercise, Program, ProgramExercise, Challenge, ChallengeDay, ChallengeExercise, Badge

app = create_app()

with app.app_context():
    # 1. Egzersizleri Ekle
    exercises_data = [
        {'name': 'Diamond Şınav', 'slug': 'diamond-sinav', 'description': 'Arka kol ve iç göğüs odaklı zorlu şınav.', 'instructions': 'Ellerinizi göğüs hizanızda birleştirip işaret ve baş parmaklarınızla elmas şekli yapın. Vücudunuzu düz tutarak inip kalkın.', 'muscle_group': 'Arka Kol, Göğüs', 'difficulty': 'Orta', 'equipment': 'Ekipmansız', 'duration_seconds': None, 'calories_estimate': 60},
        {'name': 'Mountain Climber', 'slug': 'mountain-climber', 'description': 'Tüm vücudu çalıştıran dinamik karın egzersizi.', 'instructions': 'Şınav pozisyonu alın ve dizlerinizi sırayla göğsünüze doğru hızla çekin.', 'muscle_group': 'Karın, Kardiyo', 'difficulty': 'Başlangıç', 'equipment': 'Ekipmansız', 'duration_seconds': 45, 'calories_estimate': 70},
        {'name': 'Burpee', 'slug': 'burpee', 'description': 'En etkili yağ yakıcı tüm vücut egzersizi.', 'instructions': 'Ayaktayken çömelip şınav pozisyonuna geçin, bir şınav çekin, tekrar çömelme pozisyonuna zıplayıp yukarı doğru sıçrayın.', 'muscle_group': 'Tüm Vücut', 'difficulty': 'İleri', 'equipment': 'Ekipmansız', 'duration_seconds': 60, 'calories_estimate': 120},
        {'name': 'Lunge', 'slug': 'lunge', 'description': 'Bacak ve kalça sıkılaştırıcı.', 'instructions': 'Ayaktayken bir adım öne atın ve dizlerinizi 90 derece bükerek çömelin. Geri dönüp diğer bacakla tekrarlayın.', 'muscle_group': 'Bacak, Kalça', 'difficulty': 'Başlangıç', 'equipment': 'Ekipmansız', 'duration_seconds': None, 'calories_estimate': 50},
        {'name': 'Russian Twist', 'slug': 'russian-twist', 'description': 'Yan karın kasları (oblik) için mükemmel.', 'instructions': 'Yere oturup dizlerinizi bükün, ayaklarınızı havaya kaldırın. Gövdenizi sağa ve sola döndürerek ellerinizi yere değdirin.', 'muscle_group': 'Karın', 'difficulty': 'Orta', 'equipment': 'Ekipmansız', 'duration_seconds': 45, 'calories_estimate': 40},
        {'name': 'Leg Raise', 'slug': 'leg-raise', 'description': 'Alt karın kaslarını hedefler.', 'instructions': 'Sırtüstü uzanın, bacaklarınızı düz tutarak yukarı kaldırın ve yavaşça yere indirin. Yere değdirmeden tekrar kaldırın.', 'muscle_group': 'Alt Karın', 'difficulty': 'Orta', 'equipment': 'Ekipmansız', 'duration_seconds': None, 'calories_estimate': 40},
        {'name': 'Bench Dips', 'slug': 'bench-dips', 'description': 'Evdeki bir sandalye veya koltukla arka kol geliştirin.', 'instructions': 'Bir sandalyeye arkanızı dönün, ellerinizi sandalyenin ucuna koyun. Dirseklerinizi bükerek kalçanızı yere yaklaştırın ve tekrar itin.', 'muscle_group': 'Arka Kol', 'difficulty': 'Başlangıç', 'equipment': 'Sandalye / Koltuk', 'duration_seconds': None, 'calories_estimate': 45}
    ]

    for ex in exercises_data:
        existing = Exercise.query.filter_by(slug=ex['slug']).first()
        if not existing:
            new_ex = Exercise(**ex)
            db.session.add(new_ex)

    db.session.commit()

    # 2. Rozetleri Ekle
    badges_data = [
        {'name': 'İlk Kan', 'description': 'Uygulamadaki ilk egzersizini başarıyla tamamladın!', 'icon': '🎯'},
        {'name': 'Disiplin Abidesi', 'description': '7 gün aralıksız antrenman yaptın.', 'icon': '🔥'},
        {'name': 'Demir İrade', 'description': '30 günlük bir kampı tamamen bitirdin.', 'icon': '🛡️'},
        {'name': 'Gece Kuşu', 'description': 'Saat 22:00 sonrasında antrenman yaptın.', 'icon': '🦉'},
        {'name': 'Su Canavarı', 'description': 'Günlük 2.5 Litre su hedefine ulaştın.', 'icon': '💧'}
    ]

    for b in badges_data:
        existing = Badge.query.filter_by(name=b['name']).first()
        if not existing:
            new_badge = Badge(**b)
            db.session.add(new_badge)
            
    db.session.commit()

    # 3. Yeni Program Ekle
    prog = Program.query.filter_by(slug='30-gun-celik-karin').first()
    if not prog:
        prog = Program(title='30 Günlük Çelik Karın Kampı', slug='30-gun-celik-karin', description='Tüm karın bölgelerini hedefleyen, yağ yakıcı ve kas inşa edici yoğun 30 günlük serüven.', duration_days=30, level='Orta', goal='Kilo Verme & Sıkılaşma')
        db.session.add(prog)
        db.session.commit()
        
        ex_russian = Exercise.query.filter_by(slug='russian-twist').first()
        ex_leg = Exercise.query.filter_by(slug='leg-raise').first()
        ex_plank = Exercise.query.filter_by(slug='plank').first()
        ex_climber = Exercise.query.filter_by(slug='mountain-climber').first()

        if ex_russian and ex_leg and ex_plank and ex_climber:
            db.session.add(ProgramExercise(program_id=prog.id, exercise_id=ex_russian.id, day_number=1, sets=3, reps=20, rest_seconds=30))
            db.session.add(ProgramExercise(program_id=prog.id, exercise_id=ex_leg.id, day_number=1, sets=3, reps=15, rest_seconds=30))
            db.session.add(ProgramExercise(program_id=prog.id, exercise_id=ex_plank.id, day_number=1, sets=3, reps=1, rest_seconds=60))
            db.session.add(ProgramExercise(program_id=prog.id, exercise_id=ex_climber.id, day_number=1, sets=3, reps=20, rest_seconds=45))
        db.session.commit()

    print('Veritabani zenginlestirildi!')
