import os
import urllib.parse
password = urllib.parse.quote_plus('2478152Qwd.')
os.environ['DATABASE_URL'] = f'postgresql+psycopg2://postgres.zfwgxqomsikktyovfktn:{password}@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres?sslmode=require'

import sys
try:
    from app import create_app
    from extensions import db
    from models import Exercise, Program, ProgramExercise, Challenge, ChallengeDay, ChallengeExercise, Badge

    app = create_app()

    with app.app_context():
        print('Baglanti kuruluyor ve tablolar olusturuluyor...')
        db.create_all()
        print('Tablolar olusturuldu!')

        # 1. Egzersizleri Ekle
        exercises_data = [
            {'name': 'Diamond Şınav', 'slug': 'diamond-sinav', 'description': 'Arka kol ve iç göğüs odaklı zorlu şınav.', 'instructions': 'Ellerinizi göğüs hizanızda birleştirip işaret ve baş parmaklarınızla elmas şekli yapın. Vücudunuzu düz tutarak inip kalkın.', 'muscle_group': 'Arka Kol, Göğüs', 'difficulty': 'Orta', 'equipment': 'Ekipmansız', 'duration_seconds': None, 'calories_estimate': 60},
            {'name': 'Mountain Climber', 'slug': 'mountain-climber', 'description': 'Tüm vücudu çalıştıran dinamik karın egzersizi.', 'instructions': 'Şınav pozisyonu alın ve dizlerinizi sırayla göğsünüze doğru hızla çekin.', 'muscle_group': 'Karın, Kardiyo', 'difficulty': 'Başlangıç', 'equipment': 'Ekipmansız', 'duration_seconds': 45, 'calories_estimate': 70}
        ]

        for ex in exercises_data:
            existing = Exercise.query.filter_by(slug=ex['slug']).first()
            if not existing:
                new_ex = Exercise(**ex)
                db.session.add(new_ex)

        db.session.commit()
        print('Supabase veritabani basariyla zenginlestirildi!')
except Exception as e:
    print('HATA:', e)
    sys.exit(1)
