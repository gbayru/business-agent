# BRD RAG Wiki İçerik Rehberi

> **Bu sayfa, BRD oluşturma sürecinde RAG sisteminin kullanacağı tüm bilgileri içerir.**
> 
> **Kullanım:** Bu sayfayı Confluence'de oluşturun ve RAG sistemine ekleyin. Sistem otomatik olarak ilgili bilgileri çekecektir.

---

## 📋 1. Background (Mevcut Durum ve Problem)

**RAG Arama Terimleri:** `problem statement current situation pain point background`

### Problem Tanımlama Örnekleri

- **Örnek 1:** Mevcut ödeme sisteminde timeout sorunları yaşanıyor. Özellikle peak saatlerde (18:00-20:00) ödeme işlemlerinin %15'i timeout veriyor ve kullanıcılar işlemi tekrar yapmak zorunda kalıyor.

- **Örnek 2:** Mobil uygulamada kayıt süreci 8 adımdan oluşuyor ve kullanıcıların %40'ı süreci yarıda bırakıyor. Bu durum müşteri kazanım oranını düşürüyor.

- **Örnek 3:** Call center'da müşteri sorgulama işlemi 3 farklı sistemden bilgi çekiyor ve ortalama 5 dakika sürüyor. Müşteri memnuniyeti düşük.

### Mevcut Sistem Durumu (As-Is)

- **Ödeme Sistemi:** Legacy sistem, günlük 500K transaction kapasitesi, ortalama response time 3 saniye
- **Kayıt Süreci:** 8 adımlı form, SMS doğrulama, email aktivasyon
- **Müşteri Sorgulama:** 3 farklı backend sistem entegrasyonu, manuel veri birleştirme

### Pain Point Kataloğu

| Pain Point | Etki | Örnek Senaryo |
|------------|------|---------------|
| Timeout Sorunları | Yüksek | Peak saatlerde ödeme işlemlerinin %15'i başarısız |
| Uzun Süreçler | Orta | Kayıt sürecinde %40 drop-off oranı |
| Sistem Entegrasyonu | Yüksek | Müşteri sorgulama 5 dakika sürüyor |
| Performans Sorunları | Orta | Response time 3 saniyenin üzerinde |

---

## 🎯 2. Expected Results (Beklenen Sonuçlar)

**RAG Arama Terimleri:** `expected results success metrics KPI target measurable`

### KPI ve Metrik Tanımları

- **Performans Metrikleri:**
  - Response time: 2 saniye altı
  - Timeout oranı: %5'in altı
  - Sistem uptime: %99.9

- **İş Metrikleri:**
  - Transaction başarı oranı: %95'in üzeri
  - Kullanıcı memnuniyeti: 4.5/5
  - İşlem hacmi: Günlük 1M transaction kapasitesi

- **Kullanıcı Deneyimi:**
  - Kayıt tamamlama oranı: %80'in üzeri
  - Form doldurma süresi: 3 dakika altı
  - Hata oranı: %2'nin altı

### Ölçülebilir Hedef Formatları

✅ **İyi Örnekler:**
- "Response time'ı 3 saniyeden 2 saniyenin altına düşürmek"
- "Timeout oranını %15'ten %5'in altına indirmek"
- "Günlük transaction kapasitesini 500K'dan 1M'a çıkarmak"
- "Kayıt tamamlama oranını %60'tan %80'e yükseltmek"
- "Müşteri sorgulama süresini 5 dakikadan 30 saniyeye düşürmek"

❌ **Kötü Örnekler (Kaçınılmalı):**
- "Sistemi hızlandırmak" (ölçülebilir değil)
- "Daha iyi performans" (belirsiz)
- "Kullanıcı deneyimini iyileştirmek" (somut değil)

### Başarı Kriterleri Şablonu

1. **Metrik:** [Metrik adı]
2. **Mevcut Durum:** [Sayısal değer]
3. **Hedef:** [Sayısal değer]
4. **Ölçüm Yöntemi:** [Nasıl ölçülecek]
5. **Zaman Çerçevesi:** [Ne zaman ölçülecek]

**Örnek:**
- **Metrik:** Ödeme işlemi response time
- **Mevcut Durum:** 3 saniye
- **Hedef:** 2 saniye altı
- **Ölçüm Yöntemi:** APM tool ile gerçek zamanlı ölçüm
- **Zaman Çerçevesi:** 3 ay içinde

---

## 👥 3. Target Customer Group (Hedef Müşteri Grubu)

**RAG Arama Terimleri:** `customer segment prepaid postpaid SME consumer target group`

### Müşteri Segmentleri

#### Prepaid Segmenti
- **Tanım:** Ön ödemeli hat kullanan müşteriler
- **Özellikler:**
  - Yaş grubu: 18-35
  - Gelir seviyesi: Düşük-Orta
  - Mobil uygulama kullanımı: Yüksek (%85)
  - Web kullanımı: Düşük (%15)
- **İstatistikler:**
  - Toplam müşteri: 15M
  - Günlük aktif: 8M
  - Aylık transaction: 120M
  - Ortalama transaction değeri: 50 TL

#### Postpaid Segmenti
- **Tanım:** Faturalı hat kullanan müşteriler
- **Özellikler:**
  - Yaş grubu: 25-55
  - Gelir seviyesi: Orta-Üst
  - Mobil uygulama kullanımı: Orta (%60)
  - Web kullanımı: Yüksek (%40)
  - Call center tercihi: Yüksek
- **İstatistikler:**
  - Toplam müşteri: 20M
  - Günlük aktif: 12M
  - Aylık transaction: 200M
  - Ortalama transaction değeri: 150 TL

#### SME (KOBİ) Segmenti
- **Tanım:** Küçük ve orta ölçekli işletmeler
- **Özellikler:**
  - Kurumsal ihtiyaçlar
  - API entegrasyonu tercih eder
  - Raporlama ihtiyacı yüksek
  - Web ve API kullanımı: Yüksek
- **İstatistikler:**
  - Toplam müşteri: 500K
  - Günlük aktif: 300K
  - Aylık transaction: 50M
  - Ortalama transaction değeri: 500 TL

#### Consumer Segmenti
- **Tanım:** Bireysel tüketiciler (prepaid + postpaid)
- **Özellikler:**
  - Geniş kullanıcı tabanı
  - Mobil-first yaklaşım
  - Self-service tercih eder
- **İstatistikler:**
  - Toplam müşteri: 35M
  - Günlük aktif: 20M

### Segment Seçim Kriterleri

| Kriter | Prepaid | Postpaid | SME | Consumer |
|--------|---------|----------|-----|----------|
| Mobil App | ✅ Yüksek | ⚠️ Orta | ❌ Düşük | ✅ Yüksek |
| Web Portal | ❌ Düşük | ✅ Yüksek | ✅ Yüksek | ⚠️ Orta |
| Call Center | ❌ Düşük | ✅ Yüksek | ✅ Yüksek | ⚠️ Orta |
| API | ❌ Yok | ⚠️ Orta | ✅ Yüksek | ❌ Yok |

---

## 📱 4. Impacted Channels (Etkilenen Kanallar)

**RAG Arama Terimleri:** `channels app web call center store API impacted channels`

### Kanal Envanteri

#### Mobil Uygulama (iOS/Android)
- **Teknik Detaylar:**
  - iOS: Swift, minimum iOS 13
  - Android: Kotlin, minimum Android 8.0
  - API Version: v2.1
- **Kullanım İstatistikleri:**
  - Günlük aktif: 15M kullanıcı
  - Peak transaction: 5,000/dakika
- **Limitasyonlar:**
  - Offline mod desteklenmiyor
  - Maksimum request size: 1MB
  - Timeout: 30 saniye

#### Web Portal
- **Teknik Detaylar:**
  - Frontend: React 18
  - Backend API: REST v2.0
  - Browser desteği: Chrome, Safari, Edge (son 2 versiyon)
- **Kullanım İstatistikleri:**
  - Günlük aktif: 8M kullanıcı
  - Peak transaction: 2,000/dakika
- **Limitasyonlar:**
  - Session timeout: 30 dakika
  - Maksimum dosya upload: 10MB

#### Call Center
- **Teknik Detaylar:**
  - CRM entegrasyonu: Salesforce
  - Telefon sistemi: Avaya
  - Agent sayısı: 2,000
- **Kullanım İstatistikleri:**
  - Günlük çağrı: 100K
  - Ortalama bekleme süresi: 2 dakika
- **Limitasyonlar:**
  - Peak saatlerde kapasite: 5,000 eşzamanlı çağrı
  - Maksimum bekleme: 10 dakika

#### Mağaza (Store)
- **Teknik Detaylar:**
  - POS sistemi: Verifone
  - Entegrasyon: SOAP API v1.5
  - Mağaza sayısı: 5,000
- **Kullanım İstatistikleri:**
  - Günlük transaction: 200K
  - Peak saatler: 12:00-14:00, 18:00-20:00
- **Limitasyonlar:**
  - Offline mod: Sınırlı (sadece okuma)
  - Sync interval: 15 dakika

#### API Gateway
- **Teknik Detaylar:**
  - REST API v2.1
  - Authentication: OAuth 2.0
  - Rate limit: 1,000 request/dakika per client
- **Kullanım İstatistikleri:**
  - Günlük API call: 50M
  - Aktif client: 10K
- **Limitasyonlar:**
  - Maksimum payload: 5MB
  - Timeout: 60 saniye
  - Rate limit: Client bazlı

### Kanal Etki Senaryoları

| Değişiklik Tipi | Etkilenen Kanallar | Örnek |
|-----------------|-------------------|-------|
| Ödeme İyileştirmesi | App, Web, Store | Yeni ödeme gateway entegrasyonu |
| Kayıt Süreci | App, Web | Form adımlarının azaltılması |
| Müşteri Sorgulama | Call Center, Web | Tek sistemden sorgulama |
| Raporlama | Web, API | Yeni dashboard eklenmesi |

---

## 🗺️ 5. Impacted Journey (Etkilenen Journey)

**RAG Arama Terimleri:** `journey name existing new impacted journey flow`

### Journey Kataloğu

#### Mevcut Journey'ler (Existing)

1. **Ödeme Journey**
   - Açıklama: Kullanıcının ödeme yapma süreci
   - Adımlar: Sepet → Ödeme → Onay → Tamamlama
   - Durum: Aktif, versiyon 2.1

2. **Kayıt Journey**
   - Açıklama: Yeni kullanıcı kayıt süreci
   - Adımlar: Form → SMS Doğrulama → Email Aktivasyon → Tamamlama
   - Durum: Aktif, versiyon 1.5

3. **Transfer Journey**
   - Açıklama: Para transferi süreci
   - Adımlar: Alıcı Seçimi → Tutar → Onay → Tamamlama
   - Durum: Aktif, versiyon 1.0

4. **Sorgulama Journey**
   - Açıklama: Müşteri bilgi sorgulama
   - Adımlar: Kimlik Doğrulama → Sorgu → Sonuç
   - Durum: Aktif, versiyon 1.2

5. **Fatura Ödeme Journey**
   - Açıklama: Fatura ödeme süreci
   - Adımlar: Fatura Seçimi → Ödeme → Onay
   - Durum: Aktif, versiyon 2.0

#### Yeni Journey'ler (New)

- **Yeni Journey Oluşturma Süreci:**
  1. Journey tasarımı
  2. Teknik analiz
  3. Geliştirme
  4. Test
  5. Production deploy

### Journey Durumları

| Durum | Açıklama | Örnek |
|-------|----------|-------|
| Existing | Mevcut journey, güncelleme yapılacak | Ödeme Journey v2.1 → v2.2 |
| New | Yeni journey oluşturulacak | Yeni Özellik Journey |
| Deprecated | Kullanımdan kaldırılacak | Eski Kayıt Journey |

---

## 🔄 6. Journeys Description (As-Is / To-Be Akış)

**RAG Arama Terimleri:** `as-is to-be before after edge case timeout error duplicate`

### As-Is Journey Şablonu

**Journey Adı:** [Journey Adı]

**Mevcut Akış (As-Is):**
1. Adım 1: [Açıklama] - Süre: [X saniye/dakika]
2. Adım 2: [Açıklama] - Süre: [X saniye/dakika]
3. Adım 3: [Açıklama] - Süre: [X saniye/dakika]

**Toplam Süre:** [X dakika]
**Başarı Oranı:** [%X]
**Sorunlar:** [Liste]

### To-Be Journey Şablonu

**Hedef Akış (To-Be):**
1. Adım 1: [Açıklama] - Hedef Süre: [X saniye/dakika]
2. Adım 2: [Açıklama] - Hedef Süre: [X saniye/dakika]

**Hedef Toplam Süre:** [X dakika]
**Hedef Başarı Oranı:** [%X]
**İyileştirmeler:** [Liste]

### Örnek: Ödeme Journey

**As-Is:**
1. Sepet görüntüleme - 5 saniye
2. Ödeme yöntemi seçimi - 10 saniye
3. Kart bilgileri girme - 30 saniye
4. 3D Secure doğrulama - 20 saniye
5. Ödeme işlemi - 5 saniye (bazen timeout)
6. Onay sayfası - 3 saniye

**Toplam:** ~73 saniye, Başarı: %85

**To-Be:**
1. Sepet + Ödeme yöntemi (birleştirildi) - 8 saniye
2. Kart bilgileri (kayıtlı kartlar) - 10 saniye
3. 3D Secure + Ödeme (optimize) - 15 saniye
4. Onay sayfası - 2 saniye

**Hedef Toplam:** ~35 saniye, Hedef Başarı: %95

### Edge Case Kataloğu

#### Timeout Senaryoları
- **Senaryo:** Ödeme işlemi 30 saniyeden uzun sürerse timeout
- **Çözüm:** Retry mekanizması, kullanıcıya bilgi ver
- **Örnek:** "İşleminiz devam ediyor, lütfen bekleyin" mesajı

#### Error Handling
- **Senaryo:** Backend servis yanıt vermiyor
- **Çözüm:** Fallback mekanizması, cache'den veri göster
- **Örnek:** Ödeme geçmişi cache'den gösterilir

#### Duplicate İşlemler
- **Senaryo:** Kullanıcı aynı işlemi 2 kez yaparsa
- **Çözüm:** Idempotency key kontrolü
- **Örnek:** Aynı transaction ID ile tekrar işlem yapılamaz

#### Network Sorunları
- **Senaryo:** İnternet bağlantısı kesilirse
- **Çözüm:** Offline queue, sync mekanizması
- **Örnek:** İşlem queue'ya alınır, bağlantı gelince gönderilir

#### Validasyon Hataları
- **Senaryo:** Form validasyonu başarısız
- **Çözüm:** Anlık feedback, hata mesajları
- **Örnek:** Kart numarası formatı yanlışsa anında uyarı

### Before/After Karşılaştırma Örnekleri

| Metrik | Before (As-Is) | After (To-Be) | İyileştirme |
|--------|----------------|---------------|-------------|
| Toplam Süre | 73 saniye | 35 saniye | %52 azalma |
| Başarı Oranı | %85 | %95 | %10 artış |
| Timeout Oranı | %15 | %5 | %10 azalma |
| Kullanıcı Memnuniyeti | 3.5/5 | 4.5/5 | %29 artış |

---

## 📊 7. Reports Needed (Rapor İhtiyaçları)

**RAG Arama Terimleri:** `reports dashboard metrics reporting requirements`

### Mevcut Raporlar

1. **Transaction Raporu**
   - **Kullanıcılar:** İş Analisti, Product Manager
   - **Metrikler:** Günlük/haftalık/aylık transaction sayısı, başarı oranı, hata oranı
   - **Format:** Excel, PDF
   - **Frekans:** Günlük

2. **Kullanıcı Aktivite Raporu**
   - **Kullanıcılar:** Marketing, Product Manager
   - **Metrikler:** Aktif kullanıcı sayısı, session süresi, drop-off noktaları
   - **Format:** Dashboard, Excel
   - **Frekans:** Haftalık

3. **Performans Raporu**
   - **Kullanıcılar:** DevOps, Teknik Ekip
   - **Metrikler:** Response time, error rate, system load
   - **Format:** Dashboard, Grafana
   - **Frekans:** Gerçek zamanlı

4. **Müşteri Segment Raporu**
   - **Kullanıcılar:** Business Analyst, Marketing
   - **Metrikler:** Segment bazlı transaction, kullanım istatistikleri
   - **Format:** Excel, Dashboard
   - **Frekans:** Aylık

### Rapor Şablonları

**Rapor İhtiyacı Belirleme:**
- **Rapor Adı:** [Rapor adı]
- **Kullanıcılar:** [Kim kullanacak]
- **Metrikler:** [Hangi metrikler]
- **Format:** [Excel/Dashboard/PDF]
- **Frekans:** [Günlük/Haftalık/Aylık]
- **Öncelik:** [Yüksek/Orta/Düşük]

### Yeni Rapor İhtiyaçları

| Rapor Adı | Kullanıcı | Metrikler | Format | Öncelik |
|-----------|----------|-----------|--------|---------|
| Journey Analiz Raporu | Product Manager | Journey başarı oranı, drop-off noktaları | Dashboard | Yüksek |
| Kanal Performans Raporu | Channel Manager | Kanal bazlı transaction, hata oranı | Excel | Orta |
| Müşteri Memnuniyet Raporu | Customer Success | CSAT skoru, şikayet kategorileri | Dashboard | Yüksek |

---

## 📈 8. Traffic Forecast (Trafik Tahmini)

**RAG Arama Terimleri:** `traffic forecast volume daily transactions growth estimate`

### Trafik Tahmin Metodolojisi

**Tahmin Yöntemleri:**
1. **Tarihsel Veri Analizi:** Geçmiş 12 ay verilerine bak
2. **Büyüme Trendi:** Aylık büyüme oranını hesapla
3. **Sezonsal Faktörler:** Bayram, tatil günleri etkisi
4. **Kampanya Etkisi:** Marketing kampanyalarının etkisi
5. **Benchmark Karşılaştırma:** Benzer projelerin trafik verileri

### Mevcut Trafik Değerleri (Benchmark)

| Metrik | Değer | Notlar |
|--------|-------|--------|
| Günlük Toplam Transaction | 1.5M | Peak: 2.5M (18:00-20:00) |
| Saatlik Ortalama | 62.5K | Peak saat: 200K |
| Aylık Toplam | 45M | Büyüme: %5/ay |
| Peak Dakika | 5,000 | Ödeme journey'de |
| Ortalama Transaction/User | 3.2 | Günlük |

### Trafik Tahmin Formatı

**Tahmin Detayları:**
- **Metrik:** [Transaction sayısı / Kullanıcı sayısı]
- **Mevcut Değer:** [Sayısal değer]
- **Tahmin Edilen Değer:** [Sayısal değer]
- **Büyüme Oranı:** [%X]
- **Zaman Çerçevesi:** [3 ay / 6 ay / 1 yıl]
- **Varsayımlar:** [Kampanya, sezonsal faktörler vb.]

**Örnek:**
- **Metrik:** Günlük transaction sayısı
- **Mevcut Değer:** 1.5M
- **Tahmin Edilen Değer:** 2.0M (3 ay içinde)
- **Büyüme Oranı:** %33
- **Zaman Çerçevesi:** 3 ay
- **Varsayımlar:** Yeni özellik launch, marketing kampanyası

### Geçmiş Proje Trafik Verileri

| Proje | Launch Öncesi | Launch Sonrası (3 ay) | Artış |
|-------|---------------|----------------------|-------|
| Ödeme İyileştirme | 500K/gün | 800K/gün | %60 |
| Kayıt Süreci | 50K/gün | 120K/gün | %140 |
| Yeni Özellik | 1M/gün | 1.3M/gün | %30 |

---

## 📝 Genel Best Practices

### İyi BRD Yazım Kuralları

1. **Somut ve Ölçülebilir:**
   - ✅ "Response time'ı 3 saniyeden 2 saniyeye düşürmek"
   - ❌ "Sistemi hızlandırmak"

2. **Sayısal Değerler Kullan:**
   - ✅ "Günlük 50,000 aktif kullanıcı"
   - ❌ "Çok kullanıcı"

3. **Edge Case'leri Düşün:**
   - ✅ "Timeout durumunda retry mekanizması"
   - ❌ "Hata olursa kullanıcıya bildir"

4. **Kanal Bazlı Düşün:**
   - ✅ "Mobil app ve web'de farklı akış"
   - ❌ "Tüm kanallarda aynı"

5. **Segment Bazlı Yaklaşım:**
   - ✅ "Prepaid segment için özel kampanya"
   - ❌ "Tüm müşteriler için"

### Kaçınılması Gerekenler

- ❌ Belirsiz ifadeler: "uygun", "mümkün", "hızlı", "optimum"
- ❌ Genel tanımlar: "tüm müşteriler", "her kanal"
- ❌ Ölçülemez hedefler: "daha iyi", "iyileştir"
- ❌ Teknik detay eksikliği: "sistem entegrasyonu" (hangi sistem?)

---

## 🔍 RAG Sistemi İçin Önemli Notlar

### Anahtar Kelime Kullanımı

Wiki sayfanızda şu terimleri kullanın ki RAG sistemi bulabilsin:

- **Background için:** problem, pain point, current situation, mevcut durum
- **Expected Results için:** KPI, metrics, measurable, target, hedef
- **Customer Group için:** segment, prepaid, postpaid, SME, consumer
- **Channels için:** app, web, call center, store, API, channel
- **Journey için:** journey, flow, process, süreç
- **Journey Description için:** as-is, to-be, before, after, edge case, timeout, error
- **Reports için:** report, dashboard, metrics, rapor
- **Traffic için:** traffic, volume, transaction, forecast, tahmin

### İçerik Yapısı

- ✅ Başlıklar kullanın (H1, H2, H3)
- ✅ Madde işaretleri kullanın
- ✅ Tablolar ekleyin
- ✅ Sayısal değerler verin
- ✅ Örnekler ekleyin

---

**Son Güncelleme:** [Tarih]
**Güncelleyen:** [İsim]
**Versiyon:** 1.0
