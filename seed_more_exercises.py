from app import create_app
from extensions import db
from models import Exercise

def seed_more_exercises():
    app = create_app()
    with app.app_context():
        exercises_data = [
            # GÖĞÜS & ARKA KOL
            {
                "name": "Diz Üstü Şınav (Knee Push-up)",
                "slug": "diz-ustu-sinav",
                "description": "Şınav çekmekte zorlananlar için ideal bir başlangıç egzersizi.",
                "instructions": "Dizlerinizin üzerinde durun, ellerinizi omuz genişliğinde açın ve gövdenizi düz tutarak yere doğru inip kalkın.",
                "muscle_group": "Göğüs, Arka Kol",
                "difficulty": "Başlangıç",
                "equipment": "Ekipmansız",
                "duration_seconds": 45,
                "calories_estimate": 30
            },
            {
                "name": "Geniş Tutuş Şınav (Wide Push-up)",
                "slug": "genis-tutus-sinav",
                "description": "Göğüs kaslarının dış kısmını daha fazla aktive eden şınav varyasyonu.",
                "instructions": "Normal şınav pozisyonu alın ancak ellerinizi omuz genişliğinden daha fazla açarak hareketi uygulayın.",
                "muscle_group": "Göğüs",
                "difficulty": "Orta",
                "equipment": "Ekipmansız",
                "duration_seconds": 60,
                "calories_estimate": 55
            },
            {
                "name": "Elmas Şınav (Diamond Push-up)",
                "slug": "elmas-sinav",
                "description": "Arka kol (triceps) kaslarını ve göğüsün iç kısmını hedefler.",
                "instructions": "Ellerinizi göğsünüzün tam altında başparmak ve işaret parmaklarınız elmas şekli oluşturacak şekilde birleştirin ve şınav çekin.",
                "muscle_group": "Arka Kol, Göğüs",
                "difficulty": "İleri",
                "equipment": "Ekipmansız",
                "duration_seconds": 60,
                "calories_estimate": 65
            },
            {
                "name": "Sandalye Dipsi (Chair Dips)",
                "slug": "sandalye-dipsi",
                "description": "Arka kolları sıkılaştırmak için evdeki bir sandalyeyi veya koltuğu kullanabileceğiniz harika bir egzersiz.",
                "instructions": "Ellerinizi arkanızda bir sandalyeye dayayın, bacaklarınızı öne uzatın. Kalçanızı yere doğru indirip tekrar kollarınızla kendinizi yukarı itin.",
                "muscle_group": "Arka Kol",
                "difficulty": "Orta",
                "equipment": "Sandalye/Koltuk",
                "duration_seconds": 45,
                "calories_estimate": 40
            },
            
            # SIRT & BEL
            {
                "name": "Superman",
                "slug": "superman",
                "description": "Bel, alt sırt ve kalça kaslarını güçlendiren, duruş bozukluklarına iyi gelen bir hareket.",
                "instructions": "Yüzüstü yere uzanın, kollarınızı ileri doğru uzatın. Aynı anda kollarınızı ve bacaklarınızı yerden kaldırıp 2-3 saniye bekleyin ve yavaşça indirin.",
                "muscle_group": "Sırt, Bel",
                "difficulty": "Başlangıç",
                "equipment": "Ekipmansız",
                "duration_seconds": 45,
                "calories_estimate": 25
            },
            {
                "name": "Havlu ile Kapı Çekişi (Towel Row)",
                "slug": "havlu-ile-kapi-cekisi",
                "description": "Evde sırt kaslarınızı çalıştırmak için barfiks barı olmadan yapabileceğiniz en iyi çekiş hareketi.",
                "instructions": "Sağlam bir kapı koluna veya direğe uzun bir havlu sarın. Havlunun iki ucundan tutarak geriye doğru yaslanın ve kendinizi kapıya doğru çekin.",
                "muscle_group": "Sırt, Pazu (Biceps)",
                "difficulty": "Orta",
                "equipment": "Havlu",
                "duration_seconds": 60,
                "calories_estimate": 45
            },

            # BACAK & KALÇA
            {
                "name": "Lunge (İleri Adım)",
                "slug": "lunge",
                "description": "Üst bacak ve kalça kaslarını izole eden, dengeyi geliştiren temel bacak egzersizi.",
                "instructions": "Ayakta dururken bir bacağınızla öne büyük bir adım atın ve her iki diziniz de 90 derece bükülene kadar çömelin. Tekrar başlangıç pozisyonuna dönüp diğer bacağa geçin.",
                "muscle_group": "Bacak, Kalça",
                "difficulty": "Başlangıç",
                "equipment": "Ekipmansız",
                "duration_seconds": 60,
                "calories_estimate": 50
            },
            {
                "name": "Kalça Köprüsü (Glute Bridge)",
                "slug": "kalca-koprusu",
                "description": "Kalça kaslarını (glutes) sıkılaştırmak ve bel ağrılarını hafifletmek için birebir.",
                "instructions": "Sırtüstü yatın, dizlerinizi bükün ve ayak tabanlarınızı yere basın. Kalçanızı olabildiğince yukarı kaldırın, tepe noktasında sıkın ve yavaşça indirin.",
                "muscle_group": "Kalça, Bel",
                "difficulty": "Başlangıç",
                "equipment": "Ekipmansız",
                "duration_seconds": 60,
                "calories_estimate": 35
            },
            {
                "name": "Bulgarian Split Squat",
                "slug": "bulgarian-split-squat",
                "description": "Tek bacakla yapılan, bacakları ve kalçayı yoğun şekilde yakan ileri seviye bir squat varyasyonu.",
                "instructions": "Arkanızdaki bir sandalyeye tek ayağınızın üstünü koyun. Öndeki bacağınızla çömelerek dizinizin 90 derece olmasını sağlayın ve yukarı itin.",
                "muscle_group": "Bacak, Kalça",
                "difficulty": "İleri",
                "equipment": "Sandalye",
                "duration_seconds": 60,
                "calories_estimate": 70
            },
            {
                "name": "Duvara Oturma (Wall Sit)",
                "slug": "duvara-oturma",
                "description": "Bacak kaslarının dayanıklılığını artıran izometrik (sabit) bir egzersiz.",
                "instructions": "Sırtınızı düz bir duvara yaslayın. Dizleriniz 90 derecelik açı yapana kadar sandalyede oturur gibi aşağı kayın ve bu pozisyonda bekleyin.",
                "muscle_group": "Bacak",
                "difficulty": "Orta",
                "equipment": "Duvar",
                "duration_seconds": 45,
                "calories_estimate": 40
            },

            # KARIN & MERKEZ (CORE)
            {
                "name": "Dağ Tırmanışı (Mountain Climber)",
                "slug": "dag-tirmanisi",
                "description": "Karın kaslarını çalıştırırken aynı zamanda nabzı yükselten dinamik bir hareket.",
                "instructions": "Şınav pozisyonu alın. Hızlı bir tempoda sağ dizinizi göğsünüze çekin, ardından sol dizinizi çekin. Koşar gibi hareketi tekrarlayın.",
                "muscle_group": "Karın, Kardiyo",
                "difficulty": "Orta",
                "equipment": "Ekipmansız",
                "duration_seconds": 45,
                "calories_estimate": 60
            },
            {
                "name": "Rus Burgusu (Russian Twist)",
                "slug": "rus-burgusu",
                "description": "Yan karın kaslarını (oblikler) ve core dengesini hedefler.",
                "instructions": "Yere oturun, dizlerinizi hafif bükün ve ayaklarınızı havaya kaldırın. Gövdenizi hafif arkaya eğin ve ellerinizi birleştirerek vücudunuzu sağa ve sola döndürün.",
                "muscle_group": "Yan Karın",
                "difficulty": "Orta",
                "equipment": "Ekipmansız",
                "duration_seconds": 45,
                "calories_estimate": 40
            },
            {
                "name": "Bisiklet Mekik (Bicycle Crunch)",
                "slug": "bisiklet-mekik",
                "description": "Hem düz hem de yan karın kaslarını aynı anda çalıştıran en etkili karın egzersizlerinden biri.",
                "instructions": "Sırtüstü yatın, ellerinizi başınızın arkasına koyun. Sol dizinizi karnınıza çekerken sağ dirseğinizi dizinize değdirmeye çalışın, ardından diğer tarafa geçin (bisiklet sürer gibi).",
                "muscle_group": "Karın, Yan Karın",
                "difficulty": "Orta",
                "equipment": "Ekipmansız",
                "duration_seconds": 60,
                "calories_estimate": 50
            },

            # KARDİYO & TÜM VÜCUT
            {
                "name": "Burpee",
                "slug": "burpee",
                "description": "Tüm vücudu çalıştıran, yağ yakımını maksimize eden zorlu ama son derece etkili bir kardiyo hareketi.",
                "instructions": "Ayakta başlayın, çömelip ellerinizi yere koyun. Ayaklarınızı arkaya atıp şınav pozisyonu alın. Bir şınav çekin, tekrar ayaklarınızı ellerinize çekin ve ayağa kalkarken yukarı zıplayın.",
                "muscle_group": "Tüm Vücut",
                "difficulty": "İleri",
                "equipment": "Ekipmansız",
                "duration_seconds": 60,
                "calories_estimate": 100
            },
            {
                "name": "Tırtıl Yürüyüşü (Inchworm)",
                "slug": "tirtil-yuruyusu",
                "description": "Hem esnekliği artıran hem de omuz, merkez ve bacak kaslarını çalıştıran bir tam vücut ısınma/çalışma hareketi.",
                "instructions": "Ayakta dururken bacaklarınızı kırmadan ellerinizi yere koyun. Ellerinizi adım adım öne doğru yürüterek şınav pozisyonuna gelin, ardından aynı şekilde geri dönerek ayağa kalkın.",
                "muscle_group": "Tüm Vücut, Esneklik",
                "difficulty": "Orta",
                "equipment": "Ekipmansız",
                "duration_seconds": 60,
                "calories_estimate": 45
            }
        ]

        # Sadece veritabanında olmayanları ekleyelim ki çift kayıt olmasın.
        added_count = 0
        for data in exercises_data:
            existing = Exercise.query.filter_by(slug=data["slug"]).first()
            if not existing:
                new_ex = Exercise(**data)
                db.session.add(new_ex)
                added_count += 1
        
        db.session.commit()
        print(f"Başarıyla {added_count} yeni egzersiz veritabanına eklendi!")

if __name__ == '__main__':
    seed_more_exercises()
