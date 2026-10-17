# -*- coding: utf-8 -*-
"""
Evde Spor 2.0 — Egzersiz Biyomekanik, Kademe Zinciri (Kolaylaştır / Zorlaştır / Alternatif)
ve Kalistenik Yetenek Ağacı (Skill Tree) Veritabanı.

İlham Kaynakları:
- gellyfish-ai/gymbells-exercises (easier / harder / swaps / secondary_muscles / mechanic)
- richi-sixt/calisthenics-progression (Skill Tree & Tier Progressions)
- arnobt78/Gym-Fitness-Instructor (Tempo, Split & Goal-based Workout Generator)
- wger-project/wger & Cawlumm/lyftr (Anatomy Muscle Mapping)
"""

EXERCISE_META = {
    # ==========================================
    # 1. GÖĞÜS (CHEST / HORIZONTAL PUSH)
    # ==========================================
    'incline-push-up-eller-yuksekte-sinav': {
        'tier': 1,
        'tier_label': 'Seviye 1 • Başlangıç Temeli',
        'mechanic': 'Bileşik (Compound)',
        'pattern': 'Yatay İtiş (Push)',
        'tempo': '2-1-2',
        'tempo_desc': '2 sn kontrollü iniş • 1 sn alt noktada duraklama • 2 sn güçlü itiş',
        'secondary_muscles': ['Ön Omuz (Anterior Deltoid)', 'Arka Kol (Triceps)', 'Merkez (Core)'],
        'easier': None,
        'harder': 'knee-push-up-diz-ustu-sinav',
        'swaps': ['knee-push-up-diz-ustu-sinav', 'standart-push-up-normal-sinav'],
        'mastery_goal': '3 Set × 15 Nizami Tekrar'
    },
    'knee-push-up-diz-ustu-sinav': {
        'tier': 2,
        'tier_label': 'Seviye 2 • Temel Geçiş',
        'mechanic': 'Bileşik (Compound)',
        'pattern': 'Yatay İtiş (Push)',
        'tempo': '2-1-2',
        'tempo_desc': '2 sn kontrollü iniş • 1 sn göğüs yere yakın bekle • 2 sn itiş',
        'secondary_muscles': ['Arka Kol (Triceps)', 'Ön Omuz', 'Karın (Core)'],
        'easier': 'incline-push-up-eller-yuksekte-sinav',
        'harder': 'standart-push-up-normal-sinav',
        'swaps': ['incline-push-up-eller-yuksekte-sinav', 'standart-push-up-normal-sinav'],
        'mastery_goal': '3 Set × 15 Nizami Tekrar'
    },
    'standart-push-up-normal-sinav': {
        'tier': 3,
        'tier_label': 'Seviye 3 • Klasik Ustalık',
        'mechanic': 'Bileşik (Compound)',
        'pattern': 'Yatay İtiş (Push)',
        'tempo': '2-1-1',
        'tempo_desc': '2 sn kontrollü iniş • 1 sn dipte sıkıştırma • 1 sn patlayıcı itiş',
        'secondary_muscles': ['Arka Kol (Triceps)', 'Ön Omuz', 'Serratus Anterior', 'Core'],
        'easier': 'knee-push-up-diz-ustu-sinav',
        'harder': 'decline-push-up-ayaklar-yuksekte-sinav',
        'swaps': ['wide-grip-push-up-genis-tutus-sinav', 'staggered-push-up-kademeli-sinav', 'diamond-push-up-elmas-sinav'],
        'mastery_goal': '3 Set × 20 Nizami Tekrar'
    },
    'wide-grip-push-up-genis-tutus-sinav': {
        'tier': 3,
        'tier_label': 'Seviye 3 • Göğüs Odaklı',
        'mechanic': 'Bileşik (Compound)',
        'pattern': 'Yatay İtiş (Push)',
        'tempo': '3-1-1',
        'tempo_desc': '3 sn yavaş gerilimle iniş • 1 sn göğüs esnetme • 1 sn güçlü itiş',
        'secondary_muscles': ['Ön Omuz', 'Biceps Kısa Baş (Stabilizör)', 'Core'],
        'easier': 'standart-push-up-normal-sinav',
        'harder': 'staggered-push-up-kademeli-sinav',
        'swaps': ['standart-push-up-normal-sinav', 'decline-push-up-ayaklar-yuksekte-sinav'],
        'mastery_goal': '3 Set × 15 Tekrar'
    },
    'staggered-push-up-kademeli-sinav': {
        'tier': 4,
        'tier_label': 'Seviye 4 • Asimetrik Güç',
        'mechanic': 'Bileşik (Compound)',
        'pattern': 'Asimetrik İtiş (Push)',
        'tempo': '2-1-1',
        'tempo_desc': '2 sn iniş • 1 sn denge koruma • 1 sn patlayıcı itiş',
        'secondary_muscles': ['Triceps', 'Ön Omuz', 'Oblikler (Yan Karın)'],
        'easier': 'standart-push-up-normal-sinav',
        'harder': 'diamond-push-up-elmas-sinav',
        'swaps': ['decline-push-up-ayaklar-yuksekte-sinav', 'diamond-push-up-elmas-sinav'],
        'mastery_goal': 'Her el önde 3 Set × 10 Tekrar'
    },
    'decline-push-up-ayaklar-yuksekte-sinav': {
        'tier': 4,
        'tier_label': 'Seviye 4 • Üst Göğüs & Güç',
        'mechanic': 'Bileşik (Compound)',
        'pattern': 'Eğimli İtiş (Incline Clavicular Push)',
        'tempo': '2-1-1',
        'tempo_desc': '2 sn kontrollü iniş • 1 sn üst göğüs kasılması • 1 sn güçlü itiş',
        'secondary_muscles': ['Üst Göğüs (Clavicular)', 'Ön Omuz', 'Triceps', 'Core'],
        'easier': 'standart-push-up-normal-sinav',
        'harder': 'diamond-push-up-elmas-sinav',
        'swaps': ['pike-push-up', 'staggered-push-up-kademeli-sinav'],
        'mastery_goal': '3 Set × 15 Tekrar'
    },
    'diamond-push-up-elmas-sinav': {
        'tier': 4,
        'tier_label': 'Seviye 4 • İç Göğüs & Triceps',
        'mechanic': 'Bileşik (Compound)',
        'pattern': 'Dar Tutuş İtiş (Push)',
        'tempo': '2-1-2',
        'tempo_desc': '2 sn dirsekler vücuda yakın iniş • 1 sn bekle • 2 sn kilitli itiş',
        'secondary_muscles': ['Arka Kol (Triceps Brachii)', 'İç Göğüs', 'Ön Omuz'],
        'easier': 'standart-push-up-normal-sinav',
        'harder': 'archer-push-up-okcu-sinavi',
        'swaps': ['triceps-floor-push-up-plank-to-push-up', 'decline-push-up-ayaklar-yuksekte-sinav'],
        'mastery_goal': '3 Set × 12 Tekrar'
    },
    'archer-push-up-okcu-sinavi': {
        'tier': 5,
        'tier_label': 'Seviye 5 • Elit Kalistenik',
        'mechanic': 'Bileşik / Tek Kol Geçişi (Unilateral)',
        'pattern': 'Tek Taraflı Yatay İtiş',
        'tempo': '3-1-1',
        'tempo_desc': '3 sn çalışan kola yüklenerek iniş • 1 sn dipte kontrol • 1 sn güçlü itiş',
        'secondary_muscles': ['Triceps', 'Ön Omuz', 'Göğüs Dış Hat', 'Anti-Rotasyon Core'],
        'easier': 'diamond-push-up-elmas-sinav',
        'harder': None,
        'swaps': ['diamond-push-up-elmas-sinav', 'staggered-push-up-kademeli-sinav'],
        'mastery_goal': 'Her yön 3 Set × 8 Tekrar'
    },

    # ==========================================
    # 2. SIRT (BACK / POSTERIOR CHAIN & PULL)
    # ==========================================
    'bird-dog': {
        'tier': 1,
        'tier_label': 'Seviye 1 • Omurga Stabilizasyonu',
        'mechanic': 'İzolasyon / Stabilizasyon',
        'pattern': 'Çapraz Ekstansiyon',
        'tempo': '2-2-2',
        'tempo_desc': '2 sn uzanma • 2 sn tepe noktada düz çizgi bekleme • 2 sn dönüş',
        'secondary_muscles': ['Kalça (Gluteus Maximus)', 'Arka Omuz', 'Derin Core (Multifidus)'],
        'easier': None,
        'harder': 'superman-hold',
        'swaps': ['superman-hold', 'deadbug'],
        'mastery_goal': '3 Set × 12 Çapraz Tekrar'
    },
    'superman-hold': {
        'tier': 2,
        'tier_label': 'Seviye 2 • Arka Zincir İzometrik',
        'mechanic': 'İzometrik / İzolasyon',
        'pattern': 'Omurga Ekstansiyonu',
        'tempo': 'İzometrik Tutuş',
        'tempo_desc': 'Tepe noktada kalça ve sırt kaslarını sıkarak kesintisiz izometrik bekleme',
        'secondary_muscles': ['Alt Sırt (Erector Spinae)', 'Kalça (Glutes)', 'Arka Omuz'],
        'easier': 'bird-dog',
        'harder': 'swimmer-yuzucu-pozisyonu',
        'swaps': ['swimmer-yuzucu-pozisyonu', 'reverse-snow-angels'],
        'mastery_goal': '3 Set × 45 Saniye Tutuş'
    },
    'swimmer-yuzucu-pozisyonu': {
        'tier': 2,
        'tier_label': 'Seviye 2 • Dinamik Sırt Kondisyonu',
        'mechanic': 'Bileşik (Compound)',
        'pattern': 'Dinamik Arka Zincir',
        'tempo': '1-0-1',
        'tempo_desc': 'Ritimli ve kontrollü çapraz kol-bacak çırpışı',
        'secondary_muscles': ['Alt Sırt', 'Arka Omuz', 'Kalça', 'Hamstring'],
        'easier': 'superman-hold',
        'harder': 'reverse-snow-angels',
        'swaps': ['superman-hold', 'bird-dog'],
        'mastery_goal': '3 Set × 40 Saniye'
    },
    'reverse-snow-angels': {
        'tier': 3,
        'tier_label': 'Seviye 3 • Skapular Kontrol',
        'mechanic': 'İzolasyon',
        'pattern': 'Skapular Retraksiyon',
        'tempo': '3-1-3',
        'tempo_desc': '3 sn geniş daire çizerek geriye • 1 sn kürek kemiklerini sıkıştır • 3 sn öne',
        'secondary_muscles': ['Trapez (Orta/Alt)', 'Rhomboidler', 'Arka Omuz', 'Rotator Cuff'],
        'easier': 'swimmer-yuzucu-pozisyonu',
        'harder': 'prone-y-t-w-raises',
        'swaps': ['prone-y-t-w-raises', 'towel-lat-pulldown'],
        'mastery_goal': '3 Set × 12 Yavaş Tekrar'
    },
    'prone-y-t-w-raises': {
        'tier': 3,
        'tier_label': 'Seviye 3 • Postür & Üst Sırt',
        'mechanic': 'İzolasyon',
        'pattern': 'Çok Açılı Skapular Kaldırış',
        'tempo': '2-2-2',
        'tempo_desc': 'Her harfte (Y-T-W) tepe noktada 2 sn kürek kemiklerini sıkıştırarak bekle',
        'secondary_muscles': ['Alt Trapez', 'Rhomboid', 'Arka Omuz (Rear Delt)'],
        'easier': 'reverse-snow-angels',
        'harder': 'towel-lat-pulldown',
        'swaps': ['reverse-snow-angels', 'towel-lat-pulldown'],
        'mastery_goal': '3 Set × 10 Tam Y-T-W Turu'
    },
    'towel-lat-pulldown': {
        'tier': 4,
        'tier_label': 'Seviye 4 • Kanat (Lat) Aktivasyonu',
        'mechanic': 'Bileşik (Compound)',
        'pattern': 'Dikey Çekiş (Vertical Pull)',
        'tempo': '2-2-2',
        'tempo_desc': 'Havluyu iki yana dışa doğru güçlüce gerdirirken 2 sn çek • 2 sn kanatları sık • 2 sn uzat',
        'secondary_muscles': ['Latissimus Dorsi (Kanat)', 'Biceps', 'Orta Sırt'],
        'easier': 'prone-y-t-w-raises',
        'harder': 'doorframe-table-inverted-row',
        'swaps': ['doorframe-table-inverted-row', 'reverse-snow-angels'],
        'mastery_goal': '3 Set × 15 Tam Gerilimli Tekrar'
    },
    'doorframe-table-inverted-row': {
        'tier': 5,
        'tier_label': 'Seviye 5 • Tam Vücut Ağırlığı Çekiş',
        'mechanic': 'Bileşik (Compound)',
        'pattern': 'Yatay Çekiş (Horizontal Pull)',
        'tempo': '2-1-2',
        'tempo_desc': '2 sn göğsü masaya/kapıya çek • 1 sn kürek kemiklerini kilitle • 2 sn kontrollü in',
        'secondary_muscles': ['Biceps Brachii', 'Arka Omuz', 'Kanat (Lats)', 'Core'],
        'easier': 'towel-lat-pulldown',
        'harder': None,
        'swaps': ['towel-lat-pulldown', 'doorframe-biceps-curl'],
        'mastery_goal': '4 Set × 12 Nizami Tekrar'
    },

    # ==========================================
    # 3. OMUZ & KOL (SHOULDERS & ARMS)
    # ==========================================
    'doorframe-biceps-curl': {
        'tier': 1,
        'tier_label': 'Seviye 1 • Ön Kol & Biceps İzolasyon',
        'mechanic': 'İzolasyon',
        'pattern': 'Dirsek Fleksiyonu (Pull)',
        'tempo': '2-1-2',
        'tempo_desc': '2 sn sadece biceps gücüyle kendini çek • 1 sn tepe kasılma • 2 sn yavaş negatif',
        'secondary_muscles': ['Ön Kol (Forearms)', 'Brachialis', 'Arka Omuz'],
        'easier': None,
        'harder': 'chair-dips-sandalye-arkasi-dips',
        'swaps': ['doorframe-table-inverted-row', 'chair-dips-sandalye-arkasi-dips'],
        'mastery_goal': '3 Set × 15 Tekrar'
    },
    'chair-dips-sandalye-arkasi-dips': {
        'tier': 2,
        'tier_label': 'Seviye 2 • Arka Kol (Triceps) Temeli',
        'mechanic': 'Bileşik (Compound)',
        'pattern': 'Dikey İtiş (Dip)',
        'tempo': '2-1-1',
        'tempo_desc': '2 sn dirsekler 90 derece olana dek in • 1 sn bekle • 1 sn triceps ile it',
        'secondary_muscles': ['Ön Omuz', 'Alt Göğüs', 'Merkez (Core)'],
        'easier': 'doorframe-biceps-curl',
        'harder': 'triceps-floor-push-up-plank-to-push-up',
        'swaps': ['triceps-floor-push-up-plank-to-push-up', 'bodyweight-triceps-extension'],
        'mastery_goal': '3 Set × 15 Tekrar'
    },
    'triceps-floor-push-up-plank-to-push-up': {
        'tier': 3,
        'tier_label': 'Seviye 3 • Dinamik Kol & Core',
        'mechanic': 'Bileşik (Compound)',
        'pattern': 'Dinamik İtiş & Stabilizasyon',
        'tempo': '1-1-1',
        'tempo_desc': 'Kalçayı sallamadan kontrollü şekilde ön koldan tam planke geçiş',
        'secondary_muscles': ['Triceps', 'Ön Omuz', 'Derin Core (Oblikler)'],
        'easier': 'chair-dips-sandalye-arkasi-dips',
        'harder': 'bodyweight-triceps-extension',
        'swaps': ['chair-dips-sandalye-arkasi-dips', 'diamond-push-up-elmas-sinav'],
        'mastery_goal': '3 Set × 12 Tekrar'
    },
    'bodyweight-triceps-extension': {
        'tier': 3,
        'tier_label': 'Seviye 3 • Saf Triceps Hipertrofisi',
        'mechanic': 'İzolasyon',
        'pattern': 'Dirsek Ekstansiyonu',
        'tempo': '3-1-1',
        'tempo_desc': '3 sn dirsekleri bükerek yavaşça alçal • 1 sn gerilim • 1 sn sadece ön kolla it',
        'secondary_muscles': ['Triceps Uzun Baş', 'Core', 'Serratus Anterior'],
        'easier': 'triceps-floor-push-up-plank-to-push-up',
        'harder': 'dolphin-push-up',
        'swaps': ['diamond-push-up-elmas-sinav', 'chair-dips-sandalye-arkasi-dips'],
        'mastery_goal': '3 Set × 12 Tekrar'
    },
    'dolphin-push-up': {
        'tier': 3,
        'tier_label': 'Seviye 3 • Omuz & Serratus Gücü',
        'mechanic': 'Bileşik (Compound)',
        'pattern': 'Ön Kol Dikey İtiş',
        'tempo': '2-1-2',
        'tempo_desc': '2 sn omuzları ellerin ilerisine kaydır • 1 sn tut • 2 sn kalçayı yukarı it',
        'secondary_muscles': ['Ön/Yan Omuz', 'Triceps', 'Üst Sırt', 'Core'],
        'easier': 'bodyweight-triceps-extension',
        'harder': 'pike-push-up',
        'swaps': ['pike-push-up', 'forearm-plank-on-kol-planki'],
        'mastery_goal': '3 Set × 12 Tekrar'
    },
    'pike-push-up': {
        'tier': 4,
        'tier_label': 'Seviye 4 • Dikey Omuz Pres',
        'mechanic': 'Bileşik (Compound)',
        'pattern': 'Dikey İtiş (Overhead Press)',
        'tempo': '2-1-1',
        'tempo_desc': '2 sn başın tepesini ellerin ilerisine indir • 1 sn bekle • 1 sn dikey it',
        'secondary_muscles': ['Ön & Yan Omuz (Deltoids)', 'Triceps', 'Üst Göğüs', 'Trapez'],
        'easier': 'dolphin-push-up',
        'harder': 'feet-elevated-pike-push-up',
        'swaps': ['decline-push-up-ayaklar-yuksekte-sinav', 'dolphin-push-up'],
        'mastery_goal': '3 Set × 12 Nizami Tekrar'
    },
    'feet-elevated-pike-push-up': {
        'tier': 5,
        'tier_label': 'Seviye 5 • Handstand Push-Up Öncesi',
        'mechanic': 'Bileşik (Compound)',
        'pattern': 'Tam Dikey İtiş (Vertical Push)',
        'tempo': '3-1-1',
        'tempo_desc': '3 sn kontrollü negatif iniş • 1 sn dipte güç topla • 1 sn omuzlarla yukarı it',
        'secondary_muscles': ['Tüm Omuz Başları', 'Triceps', 'Üst Trapez', 'Core'],
        'easier': 'pike-push-up',
        'harder': 'wall-handstand-hold',
        'swaps': ['pike-push-up', 'wall-handstand-hold'],
        'mastery_goal': '3 Set × 10 Tekrar'
    },
    'wall-handstand-hold': {
        'tier': 5,
        'tier_label': 'Seviye 5 • Elit Amut (Handstand)',
        'mechanic': 'İzometrik / Tam Vücut',
        'pattern': 'Ters Duruş Stabilizasyon',
        'tempo': 'İzometrik Tutuş',
        'tempo_desc': 'Kulakları omuzlarla kapatarak yeri tam güçle it ve karın/kalçayı kilitle',
        'secondary_muscles': ['Omuz Kuşağı', 'Trapez', 'Triceps', 'Bilek & Core Stabilizatörleri'],
        'easier': 'feet-elevated-pike-push-up',
        'harder': None,
        'swaps': ['feet-elevated-pike-push-up', 'pike-push-up'],
        'mastery_goal': '3 Set × 45 Saniye Duvar Amutu'
    },

    # ==========================================
    # 4. ÖN BACAK & KALÇA (QUADS & GLUTES)
    # ==========================================
    'wall-sit-duvar-oturusu': {
        'tier': 1,
        'tier_label': 'Seviye 1 • İzometrik Bacak Dayanıklılığı',
        'mechanic': 'İzometrik',
        'pattern': 'Statik Squat (Diz 90°)',
        'tempo': 'İzometrik Tutuş',
        'tempo_desc': 'Sırt duvara tam yapışık, üst bacak yere paralel sabit bekleme',
        'secondary_muscles': ['Ön Bacak (Quadriceps)', 'Kalça', 'Baldır'],
        'easier': None,
        'harder': 'standart-air-squat',
        'swaps': ['standart-air-squat', 'glute-bridge-iki-bacak-kalca-koprusu'],
        'mastery_goal': '3 Set × 60 Saniye'
    },
    'standart-air-squat': {
        'tier': 2,
        'tier_label': 'Seviye 2 • Temel Squat Formu',
        'mechanic': 'Bileşik (Compound)',
        'pattern': 'Çift Bacak Squat',
        'tempo': '2-1-1',
        'tempo_desc': '2 sn kalçayı geriye alarak çök • 1 sn paralel altında bekle • 1 sn topuklardan güçle kalk',
        'secondary_muscles': ['Kalça (Glutes)', 'Arka Bacak (Hamstrings)', 'Core'],
        'easier': 'wall-sit-duvar-oturusu',
        'harder': 'sumo-squat',
        'swaps': ['sumo-squat', 'narrow-stance-squat', 'reverse-lunge-geri-lunge'],
        'mastery_goal': '3 Set × 25 Nizami Tekrar'
    },
    'sumo-squat': {
        'tier': 2,
        'tier_label': 'Seviye 2 • İç Bacak & Kalça Odaklı',
        'mechanic': 'Bileşik (Compound)',
        'pattern': 'Geniş Açılı Squat',
        'tempo': '2-1-2',
        'tempo_desc': '2 sn dizleri ayak parmak yönüne açarak in • 1 sn dipte sıkıştır • 2 sn kalk',
        'secondary_muscles': ['İç Bacak (Adductors)', 'Kalça (Glutes)', 'Quadriceps'],
        'easier': 'standart-air-squat',
        'harder': 'narrow-stance-squat',
        'swaps': ['standart-air-squat', 'curtsy-lunge'],
        'mastery_goal': '3 Set × 20 Tekrar'
    },
    'narrow-stance-squat': {
        'tier': 3,
        'tier_label': 'Seviye 3 • Saf Quadriceps Vurgusu',
        'mechanic': 'Bileşik (Compound)',
        'pattern': 'Dar Açılı Squat',
        'tempo': '3-1-1',
        'tempo_desc': '3 sn yavaşça dizleri öne sürerek derin in • 1 sn bekle • 1 sn güçlü kalk',
        'secondary_muscles': ['Dış Ön Bacak (Vastus Lateralis)', 'Kalça', 'Core'],
        'easier': 'standart-air-squat',
        'harder': 'reverse-lunge-geri-lunge',
        'swaps': ['standart-air-squat', 'forward-lunge-ileri-lunge'],
        'mastery_goal': '3 Set × 18 Tekrar'
    },
    'reverse-lunge-geri-lunge': {
        'tier': 3,
        'tier_label': 'Seviye 3 • Diz Dostu Tek Bacak Geçişi',
        'mechanic': 'Bileşik / Unilateral',
        'pattern': 'Lunge (Tek Bacak)',
        'tempo': '2-1-1',
        'tempo_desc': '2 sn geriye adım alıp arka dizi yere yaklaştır • 1 sn denge • 1 sn ön topukla kalk',
        'secondary_muscles': ['Kalça (Gluteus Maximus)', 'Hamstring', 'Denge Kasları'],
        'easier': 'standart-air-squat',
        'harder': 'forward-lunge-ileri-lunge',
        'swaps': ['forward-lunge-ileri-lunge', 'curtsy-lunge'],
        'mastery_goal': 'Her bacak 3 Set × 12 Tekrar'
    },
    'forward-lunge-ileri-lunge': {
        'tier': 3,
        'tier_label': 'Seviye 3 • Dinamik Ön Bacak Gücü',
        'mechanic': 'Bileşik / Unilateral',
        'pattern': 'Lunge (İleri Adım)',
        'tempo': '2-1-1',
        'tempo_desc': '2 sn ileri adım ve frenleme • 1 sn 90° açı • 1 sn başlangıca güçlü itiş',
        'secondary_muscles': ['Quadriceps', 'Kalça', 'Core Stabilizatörleri'],
        'easier': 'reverse-lunge-geri-lunge',
        'harder': 'walking-lunge',
        'swaps': ['reverse-lunge-geri-lunge', 'walking-lunge'],
        'mastery_goal': 'Her bacak 3 Set × 12 Tekrar'
    },
    'curtsy-lunge': {
        'tier': 3,
        'tier_label': 'Seviye 3 • Yan Kalça (Gluteus Medius)',
        'mechanic': 'Bileşik / Unilateral',
        'pattern': 'Çapraz Lunge',
        'tempo': '2-1-2',
        'tempo_desc': '2 sn çapraz geriye adım • 1 sn yan kalçada gerilim • 2 sn kontrollü kalkış',
        'secondary_muscles': ['Yan Kalça (Gluteus Medius)', 'Quadriceps', 'İç Bacak'],
        'easier': 'reverse-lunge-geri-lunge',
        'harder': 'walking-lunge',
        'swaps': ['reverse-lunge-geri-lunge', 'sumo-squat'],
        'mastery_goal': 'Her bacak 3 Set × 12 Tekrar'
    },
    'walking-lunge': {
        'tier': 4,
        'tier_label': 'Seviye 4 • Sürekli Gerilim Lunge',
        'mechanic': 'Bileşik / Unilateral',
        'pattern': 'Yürüyerek Lunge',
        'tempo': '2-0-1',
        'tempo_desc': 'Duraksamadan akıcı adımlarla 2 sn çöküş ve 1 sn ileri transfer',
        'secondary_muscles': ['Kalça', 'Quadriceps', 'Hamstring', 'Kardiyovasküler Sistem'],
        'easier': 'forward-lunge-ileri-lunge',
        'harder': 'bulgarian-split-squat',
        'swaps': ['forward-lunge-ileri-lunge', 'bulgarian-split-squat'],
        'mastery_goal': '3 Set × 20 Adım'
    },
    'bulgarian-split-squat': {
        'tier': 4,
        'tier_label': 'Seviye 4 • İleri Tek Bacak Hipertrofisi',
        'mechanic': 'Bileşik / Unilateral',
        'pattern': 'Yükseltilmiş Tek Bacak Squat',
        'tempo': '3-1-1',
        'tempo_desc': '3 sn derin kontrollü iniş • 1 sn dipte esneme • 1 sn ön bacakla patlayıcı kalkış',
        'secondary_muscles': ['Kalça (Glutes)', 'Quadriceps', 'Hamstring', 'Ayak Bileği Stabilitesi'],
        'easier': 'walking-lunge',
        'harder': 'pistol-squat-tek-bacak-squat',
        'swaps': ['reverse-lunge-geri-lunge', 'single-leg-glute-bridge'],
        'mastery_goal': 'Her bacak 3 Set × 12 Tekrar'
    },
    'pistol-squat-tek-bacak-squat': {
        'tier': 5,
        'tier_label': 'Seviye 5 • Elit Kalistenik Bacak Ustası',
        'mechanic': 'Bileşik / Unilateral',
        'pattern': 'Tam Tek Bacak Squat',
        'tempo': '3-1-1',
        'tempo_desc': '3 sn diğer bacak havada tam çöküş • 1 sn dipte denge • 1 sn tek bacakla kalkış',
        'secondary_muscles': ['Quadriceps', 'Kalça', 'Hip Flexors (Kalça Bükücüler)', 'Core'],
        'easier': 'bulgarian-split-squat',
        'harder': None,
        'swaps': ['bulgarian-split-squat', 'squat-jump'],
        'mastery_goal': 'Her bacak 3 Set × 6 Nizami Tekrar'
    },

    # ==========================================
    # 5. ARKA BACAK & BALDIR (HAMSTRINGS & CALVES)
    # ==========================================
    'standing-calf-raise-cift-ayak-baldir-kaldirma': {
        'tier': 1,
        'tier_label': 'Seviye 1 • Baldır & Bilek Temeli',
        'mechanic': 'İzolasyon',
        'pattern': 'Ayak Bileği Plantar Fleksiyon',
        'tempo': '2-2-2',
        'tempo_desc': '2 sn parmak ucuna yüksel • 2 sn zirvede baldırı sık • 2 sn yavaşça in',
        'secondary_muscles': ['Gastrocnemius', 'Soleus', 'Ayak Bileği Stabilizatörleri'],
        'easier': None,
        'harder': 'single-leg-calf-raise',
        'swaps': ['single-leg-calf-raise', 'good-morning-vucut-agirligi'],
        'mastery_goal': '3 Set × 25 Tekrar'
    },
    'good-morning-vucut-agirligi': {
        'tier': 1,
        'tier_label': 'Seviye 1 • Kalça Menteşesi (Hip Hinge)',
        'mechanic': 'Bileşik (Compound)',
        'pattern': 'Hip Hinge (Kalça Büküşü)',
        'tempo': '3-1-1',
        'tempo_desc': '3 sn sırt düz, kalçayı geriye iterek eğil • 1 sn arka bacakta gerilim • 1 sn kalçayı sıkarak doğrul',
        'secondary_muscles': ['Alt Sırt (Erector Spinae)', 'Kalça (Glutes)', 'Hamstrings'],
        'easier': 'standing-calf-raise-cift-ayak-baldir-kaldirma',
        'harder': 'glute-bridge-iki-bacak-kalca-koprusu',
        'swaps': ['glute-bridge-iki-bacak-kalca-koprusu', 'superman-hold'],
        'mastery_goal': '3 Set × 20 Tekrar'
    },
    'glute-bridge-iki-bacak-kalca-koprusu': {
        'tier': 2,
        'tier_label': 'Seviye 2 • Kalça & Hamstring Aktivasyonu',
        'mechanic': 'Bileşik (Compound)',
        'pattern': 'Kalça Ekstansiyonu (Hip Thrust)',
        'tempo': '2-2-2',
        'tempo_desc': '2 sn kalçayı kaldır • 2 sn tepe noktada kalçayı maksimum sık • 2 sn kontrollü in',
        'secondary_muscles': ['Kalça (Gluteus Maximus)', 'Arka Bacak (Hamstrings)', 'Core'],
        'easier': 'good-morning-vucut-agirligi',
        'harder': 'elevated-glute-bridge',
        'swaps': ['elevated-glute-bridge', 'single-leg-glute-bridge'],
        'mastery_goal': '3 Set × 20 Tekrar'
    },
    'single-leg-calf-raise': {
        'tier': 3,
        'tier_label': 'Seviye 3 • Tek Bacak Baldır Gücü',
        'mechanic': 'İzolasyon / Unilateral',
        'pattern': 'Tek Ayak Plantar Fleksiyon',
        'tempo': '2-2-2',
        'tempo_desc': '2 sn yüksel • 2 sn tepe noktada bekle • 2 sn topuğu yavaşça indir',
        'secondary_muscles': ['Gastrocnemius', 'Soleus', 'Peroneal Kaslar'],
        'easier': 'standing-calf-raise-cift-ayak-baldir-kaldirma',
        'harder': 'elevated-glute-bridge',
        'swaps': ['standing-calf-raise-cift-ayak-baldir-kaldirma'],
        'mastery_goal': 'Her bacak 3 Set × 15 Tekrar'
    },
    'elevated-glute-bridge': {
        'tier': 3,
        'tier_label': 'Seviye 3 • Geniş Açılı Kalça Köprüsü',
        'mechanic': 'Bileşik (Compound)',
        'pattern': 'Yükseltilmiş Hip Thrust',
        'tempo': '2-2-2',
        'tempo_desc': 'Ayaklar yüksekte 2 sn çıkış • 2 sn zirvede sıkıştırma • 2 sn tam esneme',
        'secondary_muscles': ['Arka Bacak (Hamstrings)', 'Gluteus Maximus', 'Alt Sırt'],
        'easier': 'glute-bridge-iki-bacak-kalca-koprusu',
        'harder': 'single-leg-glute-bridge',
        'swaps': ['glute-bridge-iki-bacak-kalca-koprusu', 'single-leg-glute-bridge'],
        'mastery_goal': '3 Set × 15 Tekrar'
    },
    'single-leg-glute-bridge': {
        'tier': 4,
        'tier_label': 'Seviye 4 • Tek Bacak Arka Zincir',
        'mechanic': 'Bileşik / Unilateral',
        'pattern': 'Tek Bacak Kalça Ekstansiyonu',
        'tempo': '2-2-2',
        'tempo_desc': 'Kalça rotasyonunu önleyerek 2 sn çıkış • 2 sn tepe tutuş • 2 sn iniş',
        'secondary_muscles': ['Hamstrings', 'Gluteus Maximus & Medius', 'Core'],
        'easier': 'elevated-glute-bridge',
        'harder': 'nordic-curl-ayaklar-sabitli-hamstring-bukusu',
        'swaps': ['elevated-glute-bridge', 'bulgarian-split-squat'],
        'mastery_goal': 'Her bacak 3 Set × 12 Tekrar'
    },
    'nordic-curl-ayaklar-sabitli-hamstring-bukusu': {
        'tier': 5,
        'tier_label': 'Seviye 5 • Elit Hamstring Zırhı',
        'mechanic': 'İzolasyon / Eksantrik Güç',
        'pattern': 'Diz Fleksiyonu (Nordic)',
        'tempo': '4-1-1',
        'tempo_desc': '4 sn boyunca arka bacakla direnerek çok yavaş öne alçal • yerde ellerle desteklenip geri çık',
        'secondary_muscles': ['Hamstrings (Biceps Femoris)', 'Kalça', 'Baldır (Gastrocnemius)'],
        'easier': 'single-leg-glute-bridge',
        'harder': None,
        'swaps': ['single-leg-glute-bridge', 'elevated-glute-bridge'],
        'mastery_goal': '3 Set × 6 Kontrollü Tekrar'
    },

    # ==========================================
    # 6. KARIN & CORE (ABS & CORE)
    # ==========================================
    'standard-crunch-yarim-mekik': {
        'tier': 1,
        'tier_label': 'Seviye 1 • Üst Karın Temeli',
        'mechanic': 'İzolasyon',
        'pattern': 'Spinal Fleksiyon',
        'tempo': '2-1-2',
        'tempo_desc': '2 sn nefes vererek kürek kemiklerini yerden kaldır • 1 sn karını sık • 2 sn in',
        'secondary_muscles': ['Rectus Abdominis (Üst Karın)', 'Oblikler'],
        'easier': None,
        'harder': 'heel-touches-topuk-dokunusu',
        'swaps': ['heel-touches-topuk-dokunusu', 'deadbug'],
        'mastery_goal': '3 Set × 20 Tekrar'
    },
    'heel-touches-topuk-dokunusu': {
        'tier': 1,
        'tier_label': 'Seviye 1 • Yan Karın (Oblik) Aktivasyonu',
        'mechanic': 'İzolasyon',
        'pattern': 'Lateral Fleksiyon',
        'tempo': '1-1-1',
        'tempo_desc': '1 sn sağ topuğa uzan ve yan karını sık • 1 sn sol topuğa uzan',
        'secondary_muscles': ['Oblikler (Yan Karın)', 'Üst Karın'],
        'easier': 'standard-crunch-yarim-mekik',
        'harder': 'deadbug',
        'swaps': ['standard-crunch-yarim-mekik', 'russian-twist'],
        'mastery_goal': '3 Set × 30 Dokunuş'
    },
    'deadbug': {
        'tier': 2,
        'tier_label': 'Seviye 2 • Anti-Ekstansiyon Core Kontrolü',
        'mechanic': 'İzolasyon / Stabilizasyon',
        'pattern': 'Anti-Ekstansiyon Core',
        'tempo': '3-1-2',
        'tempo_desc': 'Bel boşluğunu yere tam bastırarak 3 sn çapraz kol-bacak uzat • 1 sn tut • 2 sn dön',
        'secondary_muscles': ['Transversus Abdominis (Derin Core)', 'Rectus Abdominis', 'Kalça Bükücüler'],
        'easier': 'heel-touches-topuk-dokunusu',
        'harder': 'high-plank-duz-kol-planki',
        'swaps': ['bird-dog', 'reverse-crunch-ters-mekik'],
        'mastery_goal': '3 Set × 16 Kontrollü Tekrar'
    },
    'high-plank-duz-kol-planki': {
        'tier': 2,
        'tier_label': 'Seviye 2 • Tam Vücut İzometrik Blok',
        'mechanic': 'İzometrik',
        'pattern': 'Anti-Ekstansiyon Plank',
        'tempo': 'İzometrik Tutuş',
        'tempo_desc': 'Omuzlar bileklerin tam üzerinde, kalça ve karın taş gibi sıkı sabit duruş',
        'secondary_muscles': ['Omuz Kuşağı', 'Serratus Anterior', 'Kalça', 'Quadriceps'],
        'easier': 'deadbug',
        'harder': 'forearm-plank-on-kol-planki',
        'swaps': ['forearm-plank-on-kol-planki', 'deadbug'],
        'mastery_goal': '3 Set × 60 Saniye'
    },
    'forearm-plank-on-kol-planki': {
        'tier': 2,
        'tier_label': 'Seviye 2 • Derin Core Dayanıklılığı',
        'mechanic': 'İzometrik',
        'pattern': 'Anti-Ekstansiyon Plank',
        'tempo': 'İzometrik Tutuş',
        'tempo_desc': 'Dirsekleri ayak parmaklarına doğru hayali olarak çekerek maksimum karın gerilimi',
        'secondary_muscles': ['Transversus Abdominis', 'Rectus Abdominis', 'Omuz', 'Kalça'],
        'easier': 'high-plank-duz-kol-planki',
        'harder': 'reverse-crunch-ters-mekik',
        'swaps': ['high-plank-duz-kol-planki', 'side-plank-yan-plank'],
        'mastery_goal': '3 Set × 60 Saniye'
    },
    'reverse-crunch-ters-mekik': {
        'tier': 3,
        'tier_label': 'Seviye 3 • Alt Karın Odaklı',
        'mechanic': 'İzolasyon',
        'pattern': 'Posterior Pelvik Tilt',
        'tempo': '2-1-3',
        'tempo_desc': '2 sn kalçayı yerden yuvarlayarak kaldır • 1 sn sık • 3 sn yavaşça indir',
        'secondary_muscles': ['Alt Karın (Lower Abs)', 'Oblikler'],
        'easier': 'forearm-plank-on-kol-planki',
        'harder': 'bicycle-crunch-bisiklet-mekigi',
        'swaps': ['lying-leg-raise', 'standard-crunch-yarim-mekik'],
        'mastery_goal': '3 Set × 15 Tekrar'
    },
    'bicycle-crunch-bisiklet-mekigi': {
        'tier': 3,
        'tier_label': 'Seviye 3 • Rotasyonel Karın & Oblik',
        'mechanic': 'Bileşik (Compound)',
        'pattern': 'Fleksiyon + Rotasyon',
        'tempo': '2-1-2',
        'tempo_desc': 'Acele etmeden omuzu karşı dize çevirerek 1 sn tam kasılma ile uygula',
        'secondary_muscles': ['Oblikler (İç ve Dış)', 'Rectus Abdominis', 'Kalça Bükücüler'],
        'easier': 'reverse-crunch-ters-mekik',
        'harder': 'russian-twist',
        'swaps': ['russian-twist', 'heel-touches-topuk-dokunusu'],
        'mastery_goal': '3 Set × 24 Tekrar'
    },
    'russian-twist': {
        'tier': 3,
        'tier_label': 'Seviye 3 • Gövde Rotasyon Gücü',
        'mechanic': 'Bileşik (Compound)',
        'pattern': 'Rotasyonel Core',
        'tempo': '2-1-2',
        'tempo_desc': 'Sadece kolları değil tüm omuz kuşağını sağa ve sola çevirerek kontrol et',
        'secondary_muscles': ['Oblikler', 'Transversus Abdominis', 'Alt Sırt Stabilizatörleri'],
        'easier': 'bicycle-crunch-bisiklet-mekigi',
        'harder': 'side-plank-yan-plank',
        'swaps': ['bicycle-crunch-bisiklet-mekigi', 'side-plank-yan-plank'],
        'mastery_goal': '3 Set × 30 Dönüş'
    },
    'side-plank-yan-plank': {
        'tier': 3,
        'tier_label': 'Seviye 3 • Lateral Core Zırhı',
        'mechanic': 'İzometrik',
        'pattern': 'Anti-Lateral Fleksiyon',
        'tempo': 'İzometrik Tutuş',
        'tempo_desc': 'Kalçayı yere düşürmeden baş, gövde ve ayakları tek bir düz çizgide tut',
        'secondary_muscles': ['Oblikler', 'Quadratus Lumborum (Bel Yanı)', 'Yan Kalça (Gluteus Medius)'],
        'easier': 'forearm-plank-on-kol-planki',
        'harder': 'side-plank-hip-dip',
        'swaps': ['side-plank-hip-dip', 'russian-twist'],
        'mastery_goal': 'Her yön 3 Set × 45 Saniye'
    },
    'side-plank-hip-dip': {
        'tier': 4,
        'tier_label': 'Seviye 4 • Dinamik Yan Karın',
        'mechanic': 'İzolasyon',
        'pattern': 'Dinamik Lateral Fleksiyon',
        'tempo': '2-1-1',
        'tempo_desc': '2 sn kalçayı yere yaklaştır • 1 sn yan karınla yukarı tepeye it',
        'secondary_muscles': ['Oblikler', 'Gluteus Medius', 'Omuz Stabilizatörleri'],
        'easier': 'side-plank-yan-plank',
        'harder': 'lying-leg-raise',
        'swaps': ['side-plank-yan-plank', 'russian-twist'],
        'mastery_goal': 'Her yön 3 Set × 12 Tekrar'
    },
    'lying-leg-raise': {
        'tier': 4,
        'tier_label': 'Seviye 4 • Alt Karın & Kalça Kontrolü',
        'mechanic': 'Bileşik (Compound)',
        'pattern': 'Uzun Kaldıraç Fleksiyon',
        'tempo': '2-1-3',
        'tempo_desc': '2 sn düz bacakları kaldır • 1 sn tut • 3 sn beli yerden kaldırmadan yavaşça indir',
        'secondary_muscles': ['Alt Karın', 'Kalça Bükücüler (Iliopsoas)', 'Quadriceps'],
        'easier': 'reverse-crunch-ters-mekik',
        'harder': 'hollow-body-hold',
        'swaps': ['reverse-crunch-ters-mekik', 'hollow-body-hold'],
        'mastery_goal': '3 Set × 15 Tekrar'
    },
    'hollow-body-hold': {
        'tier': 5,
        'tier_label': 'Seviye 5 • Cimnastik Core Temeli',
        'mechanic': 'İzometrik',
        'pattern': 'Tam Cimnastik Kompresyonu',
        'tempo': 'İzometrik Tutuş',
        'tempo_desc': 'Bel boşluğu yere sıfır yapışık, kollar ve bacaklar uzatılmış muz formunda sabit tutuş',
        'secondary_muscles': ['Tüm Karın Duvarı', 'Derin Core', 'Quadriceps'],
        'easier': 'lying-leg-raise',
        'harder': 'v-up-caki-pozisyonu',
        'swaps': ['v-up-caki-pozisyonu', 'lying-leg-raise'],
        'mastery_goal': '3 Set × 45 Saniye'
    },
    'v-up-caki-pozisyonu': {
        'tier': 5,
        'tier_label': 'Seviye 5 • Elit Patlayıcı Karın (Çakı)',
        'mechanic': 'Bileşik (Compound)',
        'pattern': 'Tam Kompresyon Fleksiyon',
        'tempo': '1-1-2',
        'tempo_desc': '1 sn patlayıcı şekilde el ve ayakları ortada birleştir • 1 sn denge • 2 sn kontrollü açıl',
        'secondary_muscles': ['Üst ve Alt Karın', 'Kalça Bükücüler', 'Serratus'],
        'easier': 'hollow-body-hold',
        'harder': None,
        'swaps': ['hollow-body-hold', 'lying-leg-raise'],
        'mastery_goal': '3 Set × 12 Nizami Tekrar'
    },

    # ==========================================
    # 7. KARDİYO & KONDİSYON (CARDIO & HIIT)
    # ==========================================
    'jumping-jacks': {
        'tier': 1,
        'tier_label': 'Seviye 1 • Ritim & Isınma Kardiyosu',
        'mechanic': 'Bileşik (Compound)',
        'pattern': 'Pliometrik Ritmik Sıçrama',
        'tempo': '1-0-1',
        'tempo_desc': 'Yumuşak parmak ucu inişleriyle tempolu ve nefesle uyumlu ritim',
        'secondary_muscles': ['Baldır (Calves)', 'Omuz', 'Kalça Abduktörleri'],
        'easier': None,
        'harder': 'mountain-climber',
        'swaps': ['high-knees', 'mountain-climber'],
        'mastery_goal': '3 Set × 60 Saniye'
    },
    'mountain-climber': {
        'tier': 2,
        'tier_label': 'Seviye 2 • Dinamik Core & Nabız',
        'mechanic': 'Bileşik (Compound)',
        'pattern': 'Dinamik Plank Koşusu',
        'tempo': '1-0-1',
        'tempo_desc': 'Kalçayı havaya kaldırmadan dizleri göğse doğru seri ve ritmik çek',
        'secondary_muscles': ['Karın (Core)', 'Omuz Stabilizatörleri', 'Kalça Bükücüler'],
        'easier': 'jumping-jacks',
        'harder': 'cross-body-mountain-climber',
        'swaps': ['cross-body-mountain-climber', 'high-knees'],
        'mastery_goal': '3 Set × 45 Saniye'
    },
    'cross-body-mountain-climber': {
        'tier': 3,
        'tier_label': 'Seviye 3 • Oblik Odaklı Dağ Tırmanışı',
        'mechanic': 'Bileşik (Compound)',
        'pattern': 'Rotasyonel Plank Koşusu',
        'tempo': '1-0-1',
        'tempo_desc': 'Dizleri çapraz dirseğe doğru çekerek yan karın kaslarını ateşle',
        'secondary_muscles': ['Oblikler (Yan Karın)', 'Alt Karın', 'Omuz'],
        'easier': 'mountain-climber',
        'harder': 'high-knees',
        'swaps': ['mountain-climber', 'bicycle-crunch-bisiklet-mekigi'],
        'mastery_goal': '3 Set × 45 Saniye'
    },
    'high-knees': {
        'tier': 3,
        'tier_label': 'Seviye 3 • Sprint Kondisyonu',
        'mechanic': 'Bileşik (Compound)',
        'pattern': 'Olduğu Yerde Patlayıcı Koşu',
        'tempo': 'Maksimum Ritim',
        'tempo_desc': 'Kolları aktif kullanarak dizleri bel hizasının üzerine seri şekilde çek',
        'secondary_muscles': ['Alt Karın', 'Baldır', 'Kalça Bükücüler', 'Kardiyo'],
        'easier': 'jumping-jacks',
        'harder': 'skater-hops-paten-sicrayisi',
        'swaps': ['jumping-jacks', 'mountain-climber'],
        'mastery_goal': '3 Set × 45 Saniye'
    },
    'skater-hops-paten-sicrayisi': {
        'tier': 4,
        'tier_label': 'Seviye 4 • Yanal Çeviklik & Patlayıcılık',
        'mechanic': 'Bileşik / Pliometrik',
        'pattern': 'Lateral Pliometrik Sıçrama',
        'tempo': '1-1-1',
        'tempo_desc': 'Yana güçlü sıçra • tek ayak üzerinde yumuşakça diz bükerek kon ve hemen diğer yana patla',
        'secondary_muscles': ['Yan Kalça (Gluteus Medius)', 'Quadriceps', 'Ayak Bileği Stabilitesi'],
        'easier': 'high-knees',
        'harder': 'squat-jump',
        'swaps': ['squat-jump', 'curtsy-lunge'],
        'mastery_goal': '3 Set × 40 Saniye'
    },
    'squat-jump': {
        'tier': 4,
        'tier_label': 'Seviye 4 • Patlayıcı Alt Vücut Gücü',
        'mechanic': 'Bileşik / Pliometrik',
        'pattern': 'Dikey Pliometrik Squat',
        'tempo': '2-0-X',
        'tempo_desc': '2 sn squat çöküşü • dipten beklemeden maksimum patlayıcılıkla sıçra ve yay gibi yumuşak in',
        'secondary_muscles': ['Quadriceps', 'Kalça (Glutes)', 'Baldır (Calves)', 'Core'],
        'easier': 'standart-air-squat',
        'harder': 'standard-burpee',
        'swaps': ['skater-hops-paten-sicrayisi', 'standart-air-squat'],
        'mastery_goal': '3 Set × 15 Patlayıcı Tekrar'
    },
    'standard-burpee': {
        'tier': 5,
        'tier_label': 'Seviye 5 • Tam Vücut Metabolik Zirve',
        'mechanic': 'Bileşik / Tam Vücut',
        'pattern': 'Şınav + Squat + Sıçrama Kombinasyonu',
        'tempo': 'Akıcı Tam Ritim',
        'tempo_desc': 'Çök • ayakları geriye fırlat • göğsü yere değdir • sıçrayarak topla ve havaya zıpla',
        'secondary_muscles': ['Göğüs', 'Omuz', 'Bacaklar', 'Core', 'Kardiyovasküler Kapasite'],
        'easier': 'squat-jump',
        'harder': None,
        'swaps': ['squat-jump', 'mountain-climber'],
        'mastery_goal': '3 Set × 15 Kesintisiz Tekrar'
    }
}


# Kalistenik Yetenek Ağacı (Skill Tree Tracks)
CALISTHENICS_TREES = [
    {
        'id': 'push-tree',
        'title': 'Yatay İtiş & Göğüs Ustası',
        'subtitle': 'Eğimli Şınavdan Tek Kol (Okçu) Şınava Uzanan Güç Zinciri',
        'icon': '🔥',
        'muscle_group': 'Göğüs',
        'color': 'orange',
        'nodes': [
            'incline-push-up-eller-yuksekte-sinav',
            'knee-push-up-diz-ustu-sinav',
            'standart-push-up-normal-sinav',
            'wide-grip-push-up-genis-tutus-sinav',
            'staggered-push-up-kademeli-sinav',
            'decline-push-up-ayaklar-yuksekte-sinav',
            'diamond-push-up-elmas-sinav',
            'archer-push-up-okcu-sinavi'
        ]
    },
    {
        'id': 'handstand-tree',
        'title': 'Omuz, Kol & Amut (Handstand) Yolu',
        'subtitle': 'Temel Kol Gücünden Duvar Amutuna (Wall Handstand) İlerleme',
        'icon': '🤸',
        'muscle_group': 'Omuz, Kol',
        'color': 'amber',
        'nodes': [
            'doorframe-biceps-curl',
            'chair-dips-sandalye-arkasi-dips',
            'triceps-floor-push-up-plank-to-push-up',
            'bodyweight-triceps-extension',
            'dolphin-push-up',
            'pike-push-up',
            'feet-elevated-pike-push-up',
            'wall-handstand-hold'
        ]
    },
    {
        'id': 'pull-tree',
        'title': 'Çekiş & Çelik Sırt Zinciri',
        'subtitle': 'Omurga Aktivasyonundan Tam Vücut Ağırlığı Yatay Çekişe',
        'icon': '🦅',
        'muscle_group': 'Sırt',
        'color': 'emerald',
        'nodes': [
            'bird-dog',
            'superman-hold',
            'swimmer-yuzucu-pozisyonu',
            'reverse-snow-angels',
            'prone-y-t-w-raises',
            'towel-lat-pulldown',
            'doorframe-table-inverted-row'
        ]
    },
    {
        'id': 'squat-tree',
        'title': 'Tek Bacak Squat (Pistol Squat) Yolu',
        'subtitle': 'Duvar Oturuşundan Elit Tek Bacak Pistol Squat\'a Kademeli Geçiş',
        'icon': '⚡',
        'muscle_group': 'Ön Bacak, Kalça',
        'color': 'blue',
        'nodes': [
            'wall-sit-duvar-oturusu',
            'standart-air-squat',
            'sumo-squat',
            'narrow-stance-squat',
            'reverse-lunge-geri-lunge',
            'forward-lunge-ileri-lunge',
            'walking-lunge',
            'bulgarian-split-squat',
            'pistol-squat-tek-bacak-squat'
        ]
    },
    {
        'id': 'posterior-tree',
        'title': 'Arka Zincir & Nordic Curl Ustası',
        'subtitle': 'Kalça Köprüsünden Elit Eksantrik Nordic Hamstring Curl\'e',
        'icon': '🛡️',
        'muscle_group': 'Arka Bacak, Baldır',
        'color': 'purple',
        'nodes': [
            'standing-calf-raise-cift-ayak-baldir-kaldirma',
            'good-morning-vucut-agirligi',
            'glute-bridge-iki-bacak-kalca-koprusu',
            'single-leg-calf-raise',
            'elevated-glute-bridge',
            'single-leg-glute-bridge',
            'nordic-curl-ayaklar-sabitli-hamstring-bukusu'
        ]
    },
    {
        'id': 'core-tree',
        'title': 'Cimnastik Core & V-Up Zırhı',
        'subtitle': 'Temel Mekikten Cimnastik Hollow Body ve V-Up Kompresyonuna',
        'icon': '💎',
        'muscle_group': 'Karın, Core',
        'color': 'rose',
        'nodes': [
            'standard-crunch-yarim-mekik',
            'heel-touches-topuk-dokunusu',
            'deadbug',
            'high-plank-duz-kol-planki',
            'forearm-plank-on-kol-planki',
            'reverse-crunch-ters-mekik',
            'bicycle-crunch-bisiklet-mekigi',
            'side-plank-yan-plank',
            'lying-leg-raise',
            'hollow-body-hold',
            'v-up-caki-pozisyonu'
        ]
    },
    {
        'id': 'cardio-tree',
        'title': 'Metabolik Kondisyon & Patlayıcı HIIT',
        'subtitle': 'Ritimli Sıçramalardan Tam Vücut Patlayıcı Burpee Kondisyonuna',
        'icon': '🚀',
        'muscle_group': 'Kardiyo, Kondisyon',
        'color': 'red',
        'nodes': [
            'jumping-jacks',
            'mountain-climber',
            'cross-body-mountain-climber',
            'high-knees',
            'skater-hops-paten-sicrayisi',
            'squat-jump',
            'standard-burpee'
        ]
    }
]


# GymMane 'Places' Mantığı: Ev Ortamı & Ekipman Sınıflandırması
CHAIR_OR_WALL_EXERCISES = {
    'incline-push-up-eller-yuksekte-sinav': 'Koltuk / Sandalye / Yatak Kenarı',
    'decline-push-up-ayaklar-yuksekte-sinav': 'Koltuk / Sandalye',
    'chair-dips-sandalye-arkasi-dips': 'Sağlam Sandalye / Koltuk Kenarı',
    'bulgarian-split-squat': 'Sandalye / Koltuk',
    'elevated-glute-bridge': 'Koltuk / Sandalye',
    'feet-elevated-pike-push-up': 'Koltuk / Sandalye',
    'wall-sit-duvar-oturusu': 'Düz Duvar',
    'wall-handstand-hold': 'Boş Duvar'
}

TOWEL_OR_DOOR_EXERCISES = {
    'towel-lat-pulldown': 'Banyo Havlusu',
    'doorframe-table-inverted-row': 'Sağlam Masa Altı / Kapı Kenarı',
    'doorframe-biceps-curl': 'Kapı Pervazı / Direk',
    'sliding-leg-curl-havlu-ile-arka-bacak': 'Kaygan Zemin + Havlu',
    'nordic-curl-ayaklar-sabitli-hamstring-bukusu': 'Koltuk Altı / Ayak Sabitleyici'
}


def get_exercise_meta(slug):
    """Return metadata dict for an exercise slug with safe defaults + GymMane Places & Superset metadata."""
    default_meta = {
        'tier': 2,
        'tier_label': 'Seviye 2 • Temel Hareket',
        'mechanic': 'Bileşik (Compound)',
        'pattern': 'Fonksiyonel Vücut Ağırlığı',
        'tempo': '2-1-2',
        'tempo_desc': '2 sn kontrollü iniş • 1 sn tepe kasılma • 2 sn dönüş',
        'secondary_muscles': ['Merkez (Core)', 'Stabilizatör Kaslar'],
        'easier': None,
        'harder': None,
        'swaps': [],
        'mastery_goal': '3 Set × 15 Nizami Tekrar'
    }
    meta = EXERCISE_META.get(slug)
    merged = default_meta.copy()
    if meta:
        merged.update(meta)

    if slug in CHAIR_OR_WALL_EXERCISES:
        merged['place_kit'] = 'sandalye'
        merged['place_label'] = '🪑 Sandalye / Duvar'
        merged['equipment_needed'] = CHAIR_OR_WALL_EXERCISES[slug]
    elif slug in TOWEL_OR_DOOR_EXERCISES:
        merged['place_kit'] = 'havlu_kapi'
        merged['place_label'] = '🧣 Havlu / Kapı Kenarı'
        merged['equipment_needed'] = TOWEL_OR_DOOR_EXERCISES[slug]
    else:
        merged['place_kit'] = 'zemin'
        merged['place_label'] = '🟢 Sadece Zemin (Sıfır Eşya)'
        merged['equipment_needed'] = 'Ekipmansız (Sadece Zemin/Mat)'

    return merged

