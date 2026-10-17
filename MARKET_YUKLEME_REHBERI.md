# 📱 Evde Spor — A'dan Z'ye Google Play Store & Apple App Store Yükleme Rehberi

Uygulamanız hiçbir mevcut özelliği bozulmadan **Google Play Store** ve **Apple App Store**'un tüm teknik, görsel ve yasal standartlarına %100 uyumlu hale getirilmiştir.

---

## ✅ 1. Hazırlanan Market Altyapısı (Otomatik Aktif)

| Gereksinim | Durum | Canlı Adres / Dosya |
| :--- | :--- | :--- |
| **Web App Manifest (PWABuilder 100/100)** | ✅ Hazır | `https://ev-sporu-app.vercel.app/manifest.json` |
| **Çevrimdışı (Offline) Çalışma & Service Worker** | ✅ Hazır | `https://ev-sporu-app.vercel.app/sw.js` ve `/offline` |
| **Gizlilik Politikası (Kamera & KVKK/GDPR Beyanı)** | ✅ Hazır | `https://ev-sporu-app.vercel.app/gizlilik-politikasi` |
| **Kullanım Koşulları & Tıbbi Sorumluluk Reddi** | ✅ Hazır | `https://ev-sporu-app.vercel.app/kullanim-kosullari` |
| **Hesap ve Veri Silme Sayfası (Apple & Google Zorunlu)** | ✅ Hazır | `https://ev-sporu-app.vercel.app/veri-silme` (+ Profil içi tek tıkla silme) |
| **Android Tam Ekran Doğrulaması (Digital Asset Links)** | ✅ Hazır | `https://ev-sporu-app.vercel.app/.well-known/assetlinks.json` |
| **iOS Universal Links Doğrulaması** | ✅ Hazır | `https://ev-sporu-app.vercel.app/.well-known/apple-app-site-association` |
| **Uygulama İkon Seti (48px - 1024px + Maskable)** | ✅ Hazır | `static/images/icons/` |
| **Google Play Özellik Grafiği (1024x500)** | ✅ Hazır | `static/screenshots/google-play-feature-graphic-1024x500.png` |
| **Mağaza Ekran Görüntüleri (1080x1920 & 1920x1080)** | ✅ Hazır | `static/screenshots/` |

---

## 🚀 2. YÖNTEM A: 2 Dakikada Kodsuz Market Paketi Oluşturma (PWABuilder — Önerilen)

Bilgisayarınıza Android Studio kurmadan doğrudan `.aab` (Google Play) ve `.ipa` (App Store) paketi indirmek için:

1. **[PWABuilder.com](https://www.pwabuilder.com)** adresine gidin.
2. Arama kutusuna **`https://ev-sporu-app.vercel.app`** yazıp **Start** butonuna tıklayın.
3. Sağ üstteki **Package for Stores** butonuna tıklayın:
   - **Google Play (Android) için:**
     - **Android** altındaki **Generate Package** butonuna tıklayın.
     - **Package ID:** `com.evdespor.app`
     - **App name:** `Evde Spor`
     - **Short name:** `Evde Spor`
     - **Signing Key:** `New` (Yeni anahtar oluştur) seçeneğini işaretleyin ve **Download** deyin.
     - İnen `.zip` dosyasının içindeki:
       - **`.aab` (Android App Bundle)** dosyasını doğrudan Google Play Console'a yükleyin.
       - **`assetlinks.json`** içindeki `sha256_cert_fingerprints` kodunu Vercel ortam değişkenlerine (`ANDROID_SHA256_FINGERPRINT`) ekleyin (böylece uygulama üstte tarayıcı çubuğu olmadan tam ekran açılır).
       - ⚠️ **`signing.keystore`** ve **`signing-key-info.txt`** dosyalarını güvenli bir yerde saklayın (gelecek güncellemeler için gereklidir).
   - **Apple App Store (iOS) için:**
     - **iOS** altındaki **Generate Package** butonuna tıklayın (Mac ve Xcode ile imzalanmaya hazır proje indirilir).

---

## 🛠️ 3. YÖNTEM B: Capacitor ile Native Android Studio / Xcode Projesi (İleri Seviye)

Eğer projeyi doğrudan Android Studio veya Xcode üzerinden derlemek isterseniz dizinde `capacitor.config.json` ve `package.json` hazır bırakılmıştır:

```bash
# 1. Bağımlılıkları yükleyin
npm install

# 2. Android ve iOS klasörlerini oluşturun
npm run cap:init

# 3. Kamera izinlerini AndroidManifest.xml ve Info.plist'e ekleyin:
# Android (android/app/src/main/AndroidManifest.xml):
# <uses-permission android:name="android.permission.CAMERA" />
# <uses-permission android:name="android.permission.INTERNET" />
#
# iOS (ios/App/App/Info.plist):
# <key>NSCameraUsageDescription</key>
# <string>AI Hareket Koçu egzersiz formunuzu gerçek zamanlı analiz etmek ve tekrarlarınızı saymak için kameranızı kullanır. Görüntüleriniz kaydedilmez.</string>

# 4. Android Studio veya Xcode'da açıp imzalayın
npm run android:open
npm run ios:open
```

---

## 📋 4. Google Play Console & App Store Connect Hazır Metinleri (Kopyala-Yapıştır)

### 🏷️ Uygulama Bilgileri
- **Uygulama Adı:** `Evde Spor - AI Fitness & Koç`
- **Kısa Açıklama (80 Karakter - Google Play):**
  `Ekipmansız ev antrenmanları, 60+ egzersiz, AI kamera koçu ve kişisel programlar.`
- **Alt Başlık (30 Karakter - App Store):**
  `Ekipmansız Ev Antrenmanları`
- **Kategori:** `Sağlık ve Fitness` (Health & Fitness)
- **İçerik Derecelendirmesi:** `Herkes / 4+` (Şiddet, kumar veya yetişkin içerik barındırmaz)

### 📝 Tam Açıklama (4000 Karakter Sınırına Uygun)
```text
Spor salonunu evine taşı! Evde Spor, hiçbir ekipmana ihtiyaç duymadan kendi vücut ağırlığınla forma girmen, kas geliştirmen ve yağ yakman için tasarlanmış yapay zeka destekli kişisel antrenman uygulamasıdır.

ÖNE ÇIKAN ÖZELLİKLER:

• 🤖 AI Hareket Koçu (Gerçek Zamanlı Kamera Analizi):
Telefonunun kamerasını karşısına geç; yapay zeka destekli biyomekanik iskelet okuyucu 60'tan fazla egzersizde eklem açılarını gerçek zamanlı analiz etsin, tekrarlarını otomatik saysın ve Türkçe sesli koç ile formunu anında düzeltsin!

• 💪 60+ Ekipmansız Egzersiz Kütüphanesi:
Göğüs, Sırt, Omuz, Kol, Bacak, Kalça, Karın (Core) ve Kardiyo (HIIT) kategorilerinde 3D form rehberli ve adım adım anlatımlı egzersizler.

• 📅 Hedefe Özel Hazır Programlar & Meydan Okumalar:
- 7 Günlük Başlangıç Programı
- 14 Günlük HIIT Yağ Yakımı
- 21 Günlük Karın ve Core
- 30 Günlük Sparta Meydan Okuması
- 30 Gün Çelik Karın Meydan Okuması

• 💧 Su Takibi, Aralıklı Oruç & Nefes Egzersizleri:
Günlük su tüketimini takip et, 16:8 aralıklı oruç sayacı ile beslenmeni düzenle ve antrenman sonrası 4-7-8 / Kutu nefes egzersizleriyle nabzını düşür.

• 🏆 Rozetler, Seri (Streak) ve Liderlik Tablosu:
Antrenman yaptıkça XP kazan, rozetlerin kilidini aç ve haftalık liderlik tablosunda zirveye yerleş!

• 🔒 %100 Kamera Gizliliği:
AI Koç özelliğinde kamera görüntüleriniz yalnızca cihazınızın ekranında anlık olarak işlenir; hiçbir sunucuya gönderilmez ve kaydedilmez.
```

---

## 🛡️ 5. Google Play "Veri Güvenliği" (Data Safety) Formu Yanıtları

Google Play Console'da **Uygulama İçeriği > Veri Güvenliği** bölümünü doldururken aşağıdaki yanıtları işaretleyin:

1. **Gizlilik Politikası URL'si:** `https://ev-sporu-app.vercel.app/gizlilik-politikasi`
2. **Hesap Silme URL'si:** `https://ev-sporu-app.vercel.app/veri-silme`
3. **Uygulamanız gerekli kullanıcı verilerini topluyor veya paylaşıyor mu?** -> **Evet** (Yalnızca üçüncü taraflarla paylaşılmayan temel hesap ve antrenman verileri)
4. **Veriler aktarım sırasında şifreleniyor mu (HTTPS)?** -> **Evet**
5. **Kullanıcılar verilerinin silinmesini talep edebilir mi?** -> **Evet** (`/veri-silme` ve uygulama içi Profil > Hesabımı Sil)
6. **Toplanan Veri Türleri:**
   - **Kişisel Bilgiler -> Ad ve E-posta Adresi:** Toplanıyor (İsteğe bağlı / Hesap oluşturma için), Üçüncü taraflarla **Paylaşılmıyor**.
   - **Sağlık ve Fitness -> Fitness Bilgileri (Boy, kilo, antrenman geçmişi, su takibi):** Toplanıyor (Uygulama işlevselliği ve kişiselleştirme için), Üçüncü taraflarla **Paylaşılmıyor**.
   - **Fotoğraflar ve Videolar (Kamera):** **Toplanmıyor** (Kamera akışı cihaz üzerinde gerçek zamanlı işlenir, kaydedilmez veya sunucuya gönderilmez).
