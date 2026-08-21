import os
import random
from app import create_app
from models import db, Program, Exercise, ProgramExercise

def add_programs():
    app = create_app()
    with app.app_context():
        # Clean existing programs except the first one maybe? Actually let's just add new ones if they don't exist.
        programs_to_add = [
            {
                'title': '30 Günlük Yağ Yakımı',
                'slug': '30-gun-yag-yakimi',
                'description': 'Kardiyo ve vücut ağırlığı egzersizleriyle maksimum kalori harcayarak yağ oranınızı düşürün.',
                'duration_days': 30,
                'level': 'Orta',
                'goal': 'Kilo Verme'
            },
            {
                'title': 'Hipertrofi ve Güç',
                'slug': 'hipertrofi-guc',
                'description': 'Tüm kas gruplarını hedef alan, hacim ve güç kazandırmaya yönelik yoğun program.',
                'duration_days': 30,
                'level': 'İleri',
                'goal': 'Kas Geliştirme'
            },
            {
                'title': 'Çelik Karın',
                'slug': 'celik-karin',
                'description': 'Merkez bölgesini (core) güçlendiren, belirgin karın kasları için 21 günlük yoğun seri.',
                'duration_days': 21,
                'level': 'Orta',
                'goal': 'Bölgesel'
            }
        ]

        for p_data in programs_to_add:
            p = Program.query.filter_by(slug=p_data['slug']).first()
            if not p:
                p = Program(**p_data)
                db.session.add(p)
        db.session.commit()

        # Fetch programs
        p_fat = Program.query.filter_by(slug='30-gun-yag-yakimi').first()
        p_muscle = Program.query.filter_by(slug='hipertrofi-guc').first()
        p_core = Program.query.filter_by(slug='celik-karin').first()

        # Fetch exercises
        all_exercises = Exercise.query.all()
        core_exercises = [e for e in all_exercises if 'Karın' in e.muscle_group or 'Core' in e.muscle_group]
        cardio_exercises = [e for e in all_exercises if 'Tüm Vücut' in e.muscle_group or 'Bacak' in e.muscle_group]
        strength_exercises = [e for e in all_exercises if 'Göğüs' in e.muscle_group or 'Sırt' in e.muscle_group or 'Omuz' in e.muscle_group or 'Kol' in e.muscle_group]

        # Seed Fat Burn (30 days) - 4-5 exercises per day
        if ProgramExercise.query.filter_by(program_id=p_fat.id).count() == 0:
            for day in range(1, 31):
                if day % 4 == 0: # Rest day every 4 days
                    continue
                daily_ex = random.sample(cardio_exercises, min(3, len(cardio_exercises))) + random.sample(core_exercises, min(2, len(core_exercises)))
                for ex in daily_ex:
                    pe = ProgramExercise(
                        program_id=p_fat.id,
                        exercise_id=ex.id,
                        day_number=day,
                        sets=4,
                        reps=15,
                        rest_seconds=45
                    )
                    db.session.add(pe)
        
        # Seed Muscle Gain (30 days) - 5-6 exercises per day
        if ProgramExercise.query.filter_by(program_id=p_muscle.id).count() == 0:
            for day in range(1, 31):
                if day % 7 == 0: # Rest day once a week
                    continue
                daily_ex = random.sample(strength_exercises, min(4, len(strength_exercises))) + random.sample(cardio_exercises, min(1, len(cardio_exercises)))
                for ex in daily_ex:
                    pe = ProgramExercise(
                        program_id=p_muscle.id,
                        exercise_id=ex.id,
                        day_number=day,
                        sets=4,
                        reps=10,
                        rest_seconds=90
                    )
                    db.session.add(pe)

        # Seed Core (21 days) - 4 exercises per day
        if ProgramExercise.query.filter_by(program_id=p_core.id).count() == 0:
            for day in range(1, 22):
                if day % 5 == 0: # Rest day
                    continue
                daily_ex = random.sample(core_exercises, min(4, len(core_exercises)))
                for ex in daily_ex:
                    pe = ProgramExercise(
                        program_id=p_core.id,
                        exercise_id=ex.id,
                        day_number=day,
                        sets=3,
                        reps=20,
                        rest_seconds=30
                    )
                    db.session.add(pe)

        db.session.commit()
        print("Programs seeded successfully!")

if __name__ == '__main__':
    add_programs()
