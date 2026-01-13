# BRD Knowledge Base

> Bu sayfa BRD oluşturma sürecinde RAG sisteminin kullanacağı tüm bilgileri içerir.
> Placeholder'ları ([X], [Y], [Segment Adı] gibi) kendi gerçek verilerinizle değiştirin.

---

# 1. Background (Mevcut Durum ve Problem)

## Problem Tanımları

**Problem 1: [Problem Adı]**

Mevcut durumda yaşanan problem. Spesifik ol, sayısal değerler kullan.

Örnek:
- Mevcut sistemde timeout sorunları yaşanıyor
- Peak saatlerde işlemlerin %[X]'i başarısız oluyor
- Günlük [Y] işlem etkileniyor

**Problem 2: [Problem Adı]**

Başka bir problem varsa buraya ekle.

## Mevcut Sistem Durumu

**Sistem Adı: [Sistem]**
- Durum: [Legacy/Mevcut/Yeni]
- Kapasite: Günlük [X] transaction, [Y] kullanıcı
- Response Time: Ortalama [Z] saniye
- Error Rate: %[X]
- Son Güncelleme: [Tarih]

## Pain Point'ler

Pain Point | Etki | Frekans | Detay
--- | --- | --- | ---
[Timeout sorunları] | Yüksek/Orta/Düşük | Günlük/Haftalık | [Açıklama]
[Uzun süreçler] | Yüksek/Orta/Düşük | Her işlem | [Açıklama]
[Manuel işlemler] | Yüksek/Orta/Düşük | [Frekans] | [Açıklama]

---

# 2. Expected Results (Beklenen Sonuçlar)

## Finansal Hedefler

**Revenue Impact:**
- Yıllık Incremental Gelir: +[X] TL/M TL
- EBITDA Impact: [Y] TL
- Cost Saving: [Z] TL

## KPI ve Metrikler

**Performans Metrikleri:**
- Response Time: [Mevcut] → [Hedef] saniye
- Error Rate: [Mevcut] → [Hedef] %
- System Uptime: [Mevcut] → [Hedef] %
- Timeout Oranı: [Mevcut] → [Hedef] %

**İş Metrikleri:**
- Transaction Success Rate: [Mevcut] → [Hedef] %
- Conversion Rate: [Mevcut] → [Hedef] %
- Customer Satisfaction: [Mevcut] → [Hedef] / 5
- Processing Time: [Mevcut] → [Hedef] saniye

**Operasyonel Metrikler:**
- Manual Process Reduction: %[X] azalma
- Agent Productivity: %[Y] artış
- Cost per Transaction: %[Z] düşüş

## Ölçülebilir Hedef Örnekleri

**İyi Örnekler:**
- Response time'ı [X] saniyeden [Y] saniyenin altına düşürmek
- Error oranını %[X]'ten %[Y]'in altına indirmek
- Günlük transaction kapasitesini [X]'den [Y]'a çıkarmak
- Conversion rate'i %[X]'ten %[Y]'e yükseltmek
- [Z] ay içinde

**Kötü Örnekler (Kaçının):**
- Sistemi hızlandırmak
- Daha iyi performans
- Kullanıcı deneyimini iyileştirmek
- Optimizasyon yapmak

---

# 3. Target Customer Group (Hedef Müşteri Grubu)

## Segment 1: [Segment Adı - örn: Postpaid]

**Tanım:** [Segment açıklaması]

**Özellikler:**
- Yaş Grubu: [X-Y]
- Gelir Seviyesi: [Düşük/Orta/Yüksek]
- Kullanım Davranışı: [Mobil/Web/Call Center tercihi]
- Tercihler: [Self-service / Assisted / etc.]

**İstatistikler:**
- Toplam Müşteri: [X]M veya [X]K
- Günlük Aktif: [Y]M veya [Y]K
- Aylık Transaction: [Z]M
- Ortalama Transaction Değeri: [A] TL
- Churn Rate: [B]% / yıl

**Davranış Özellikleri:**
- [Davranış 1]
- [Davranış 2]
- [Davranış 3]

## Segment 2: [Segment Adı - örn: Prepaid]

**Tanım:** [Segment açıklaması]

**Özellikler:**
- [Yukarıdaki format ile doldur]

**İstatistikler:**
- [Yukarıdaki format ile doldur]

## Segment 3: [Segment Adı - örn: SME/Corporate]

**Tanım:** [Segment açıklaması]

**Özellikler:**
- Firma Tipi: [10-250 çalışan / 250+ çalışan]
- Sektör: [Perakende, hizmet, üretim, vb.]
- API Kullanımı: [Var/Yok]
- Raporlama İhtiyacı: [Yüksek/Orta/Düşük]

## Segment Impact Matrix

Segment | Bu Proje İçin Hedef | Öncelik | Tahmin Edilen Etki
--- | --- | --- | ---
[Segment 1] | Evet/Hayır | Yüksek/Orta/Düşük | [Açıklama]
[Segment 2] | Evet/Hayır | Yüksek/Orta/Düşük | [Açıklama]
[Segment 3] | Evet/Hayır | Yüksek/Orta/Düşük | [Açıklama]

---

# 4. Impacted Channels (Etkilenen Kanallar)

## Kanal 1: Mobile App (iOS/Android)

**Teknik Detaylar:**
- Platform: iOS [versiyon], Android [versiyon]
- Teknoloji: [Swift/Kotlin/React Native/Flutter]
- API Version: [v2.x]
- Authentication: [OAuth 2.0 / JWT / etc.]

**Kullanım İstatistikleri:**
- Günlük Aktif Kullanıcı: [X]M
- Peak Transaction: [Y]/dakika (saat [HH:MM])
- Ortalama Session: [Z] dakika
- Crash Rate: [A]%

**Limitasyonlar:**
- Offline mode: [Var/Yok / Sınırlı]
- Max request size: [X] MB
- Request timeout: [Y] saniye
- Rate limit: [Z] request/dakika per user

**Bu Projede Etki:**
- [Hangi özellik etkilenecek]
- [Hangi ekran değişecek]
- [Hangi API call'lar eklenecek]

## Kanal 2: Web Portal

**Teknik Detaylar:**
- Frontend: [React/Angular/Vue]
- Backend API: [REST/GraphQL] [versiyon]
- Browser: [Chrome, Safari, Edge - son X versiyon]
- Responsive: [Tablet/Desktop/Mobile]

**Kullanım İstatistikleri:**
- Günlük Aktif Kullanıcı: [X]M
- Peak Transaction: [Y]/dakika
- Ortalama Session: [Z] dakika
- Bounce Rate: [A]%

**Limitasyonlar:**
- Session timeout: [X] dakika
- Max file upload: [Y] MB
- Concurrent sessions: [Z] per user

**Bu Projede Etki:**
- [Hangi sayfa etkilenecek]
- [Hangi feature eklenecek]

## Kanal 3: Call Center

**Teknik Detaylar:**
- CRM: [Salesforce/SAP/Custom]
- Telefon Sistemi: [Sistem adı]
- Agent Desktop: [Teknoloji]
- Integration: [REST API/SOAP]

**Kullanım İstatistikleri:**
- Agent Sayısı: [X]
- Günlük Çağrı: [Y]K
- Ortalama Bekleme: [Z] dakika
- Ortalama Konuşma: [A] dakika

**Bu Projede Etki:**
- [Agent'lar yeni ekran görecek mi?]
- [Yeni sorgu tipi eklenecek mi?]

## Kanal 4: Store (Mağaza)

**Teknik Detaylar:**
- POS Sistemi: [Sistem adı]
- Integration: [REST/SOAP API]
- Connectivity: [4G/Wifi/Hybrid]
- Mağaza Sayısı: [X]

**Kullanım İstatistikleri:**
- Günlük Transaction: [Y]K
- Peak Saatler: [HH:MM-HH:MM]
- Ortalama İşlem Süresi: [Z] dakika

**Bu Projede Etki:**
- [Mağazada yeni işlem yapılacak mı?]

## Kanal 5: API Gateway

**Teknik Detaylar:**
- Protocol: [REST/GraphQL]
- Authentication: [OAuth 2.0/API Key]
- Rate Limit: [X] request/dakika per client
- Documentation: [Swagger/OpenAPI]

**Kullanım İstatistikleri:**
- Günlük API Call: [X]M
- Aktif Client: [Y]K
- Success Rate: [Z]%

**Bu Projede Etki:**
- Yeni endpoint: [Var/Yok]
- Endpoint'ler: [Liste]

## Kanal Etki Matrisi

Feature/Değişiklik | Mobile | Web | Call Center | Store | API
--- | --- | --- | --- | --- | ---
[Özellik 1] | Evet | Evet | Hayır | Hayır | Evet
[Özellik 2] | Evet | Hayır | Evet | Evet | Hayır
[Özellik 3] | Hayır | Evet | Hayır | Hayır | Evet

---

# 5. Impacted Journey (Etkilenen Journey)

## Mevcut Journey'ler (Existing)

**1. Journey Adı: [örn: Payment Journey]**
- Açıklama: [Kullanıcının ne yaptığı]
- Adımlar: [Adım 1] → [Adım 2] → [Adım 3] → [Adım 4]
- Durum: Aktif/Passive
- Versiyon: [X.Y]
- Son Güncelleme: [X ay/yıl önce]
- Bu projede: Etkilenecek / Etkilenmeyecek

**2. Journey Adı: [örn: Registration Journey]**
- [Yukarıdaki format ile doldur]

**3. Journey Adı: [örn: Query Journey]**
- [Yukarıdaki format ile doldur]

## Yeni Journey'ler (New)

**1. Yeni Journey Adı: [örn: New Feature Journey]**
- Açıklama: [Ne yapacak]
- Adımlar: [Taslak adımlar]
- Durum: Yeni geliştirilecek
- Target Completion: [Tarih]

## Journey Kategorileri

**Financial Journeys:**
- [Journey 1]
- [Journey 2]

**Onboarding Journeys:**
- [Journey 1]
- [Journey 2]

**Service Journeys:**
- [Journey 1]
- [Journey 2]

**Self-Service Journeys:**
- [Journey 1]
- [Journey 2]

---

# 6. Journeys Description (As-Is / To-Be Akış)

## Journey 1: [Journey Adı] - Detaylı

**As-Is (Mevcut Durum):**

**Adım 1: [Adım Adı]** (Süre: [X] saniye)
- Kullanıcı [ne yapar]
- Sistem [ne gösterir]
- [Sorun varsa belirt]

**Adım 2: [Adım Adı]** (Süre: [Y] saniye)
- [Detay]
- [Sorun varsa]

**Adım 3: [Adım Adı]** (Süre: [Z] saniye)
- [Detay]

**Adım 4: [Adım Adı]** (Süre: [A] saniye)
- [Detay]

**Toplam Süre:** ~[X] saniye

**Başarı Oranı:** [Y]%

**Sorunlar:**
- [Sorun 1]
- [Sorun 2]
- [Sorun 3]

---

**To-Be (Hedef Durum):**

**Adım 1: [Optimize Edilmiş Adım]** (Hedef: [X] saniye)
- [İyileştirme detayı]

**Adım 2: [Optimize Edilmiş Adım]** (Hedef: [Y] saniye)
- [İyileştirme detayı]

**Adım 3: [Optimize Edilmiş Adım]** (Hedef: [Z] saniye)
- [İyileştirme detayı]

**Hedef Toplam Süre:** ~[X] saniye

**Hedef Başarı Oranı:** [Y]%

**İyileştirmeler:**
- Adım sayısı [X] → [Y]
- [İyileştirme 1]
- [İyileştirme 2]

---

## Edge Case Kataloğu

**1. Timeout Senaryoları**

Senaryo: [Ne zaman timeout oluyor]
- Çözüm: [Retry mekanizması / Kullanıcıya bilgi / etc.]
- Örnek: "İşleminiz devam ediyor, lütfen bekleyin..."

**2. Error Handling**

Senaryo: [Hangi hata]
- Mesaj: "[Kullanıcıya gösterilecek mesaj]"
- Aksiyon: [Kullanıcı ne yapmalı]

**3. Duplicate İşlemler**

Senaryo: [Kullanıcı aynı işlemi 2 kere yaparsa]
- Çözüm: [Idempotency key / Button disable / etc.]
- Sonuç: [Tek işlem yapılır]

**4. Network Sorunları**

Senaryo: [Bağlantı kesilirse]
- Çözüm: [Offline queue / Sync mekanizması]
- Kullanıcı Deneyimi: [Ne görür]

**5. Validation Hataları**

Senaryo: [Hangi validasyon]
- Kontrol: [Real-time validation / Submit validation]
- Mesaj: "[Hata mesajı]"

---

## Before/After Karşılaştırma

Metrik | Before (As-Is) | After (To-Be) | İyileştirme
--- | --- | --- | ---
Toplam Süre | [X] saniye | [Y] saniye | [Z]% azalma
Başarı Oranı | [A]% | [B]% | [C]% artış
Error Oranı | [D]% | [E]% | [F]% azalma
Adım Sayısı | [G] adım | [H] adım | [I] adım azalma
User Satisfaction | [J]/5 | [K]/5 | [L]% artış
Conversion Rate | [M]% | [N]% | [O]% artış

---

# 7. Reports Needed (Rapor İhtiyaçları)

## Mevcut Raporlar

**1. [Rapor Adı - örn: Transaction Report]**
- Kullanıcılar: [İş Analisti, Product Manager, etc.]
- Metrikler:
  - [Metrik 1: Günlük transaction sayısı]
  - [Metrik 2: Başarı oranı]
  - [Metrik 3: Hata oranı]
- Format: [Excel, PDF, Dashboard]
- Frekans: [Günlük/Haftalık/Aylık]
- Delivery: [Email (09:00) / Dashboard / etc.]

**2. [Rapor Adı - örn: User Activity Report]**
- [Yukarıdaki format ile doldur]

**3. [Rapor Adı - örn: Performance Report]**
- [Yukarıdaki format ile doldur]

---

## Yeni Rapor İhtiyaçları

Rapor Adı | Kullanıcı | Metrikler | Format | Frekans | Öncelik
--- | --- | --- | --- | --- | ---
[Rapor 1] | [Kim] | [Metrikler] | Excel/Dashboard | Günlük/Haftalık | Yüksek/Orta/Düşük
[Rapor 2] | [Kim] | [Metrikler] | Excel/Dashboard | Günlük/Haftalık | Yüksek/Orta/Düşük
[Rapor 3] | [Kim] | [Metrikler] | Excel/Dashboard | Günlük/Haftalık | Yüksek/Orta/Düşük

---

# 8. Traffic Forecast (Trafik Tahmini)

## Trafik Tahmin Metodolojisi

**1. Tarihsel Veri Analizi**
- Son [X] ay verisi kullanıldı
- Trend analizi yapıldı
- Seasonality tespiti: [Var/Yok]

**2. Büyüme Trendi**
- Aylık büyüme oranı: [X]%
- Yıllık büyüme oranı: [Y]%
- Compound growth: [Var/Yok]

**3. Sezonsal Faktörler**
- [Bayram günleri: +X% trafik]
- [Tatil günleri: -Y% trafik]
- [Ayın ilk günleri: +Z% trafik]
- [Diğer faktörler]

**4. Kampanya Etkisi**
- [Marketing kampanyası: +X% trafik]
- [TV reklamı: +Y% trafik]
- [Sosyal medya: +Z% trafik]

**5. External Faktörler**
- [Rakip kampanyaları: -X% trafik]
- [Ekonomik durum: Etki]
- [Sezon etkileri: Detay]

---

## Mevcut Trafik Değerleri (Baseline)

Metrik | Normal Gün | Peak Gün | Notlar
--- | --- | --- | ---
Günlük Transaction | [X]M | [Y]M | Peak: [Bayram/Maaş günleri]
Saatlik Ortalama | [A]K | [B]K | Peak saat: [HH:MM-HH:MM]
Dakikalık Peak | [C] | [D] | En yüksek: [HH:MM]
Aylık Toplam | [E]M | [F]M | [X]% aylık büyüme
Yıllık Toplam | [G]M | - | Trend: [Artış/Azalış/Stabil]

---

## Kanal Bazlı Trafik

Kanal | Günlük | Peak Saat | Percentage
--- | --- | --- | ---
Mobile App | [X]M | [Y]K/saat | [Z]%
Web | [A]K | [B]K/saat | [C]%
Call Center | [D]K | [E]K/saat | [F]%
Store | [G]K | [H]K/saat | [I]%
API | [J]M | [K]M/saat | [L]%

---

## Trafik Tahmin Örneği

**Örnek 1: Yeni Özellik Launch**

- Metrik: Günlük transaction
- Mevcut: [X]M
- Tahmin: [Y]M (3 ay içinde)
- Büyüme: [Z]%
- Zaman: 3 ay
- Varsayımlar:
  - Yeni özellik launch
  - Marketing kampanyası ([X] TL budget)
  - TV reklamı ([Y] hafta)
  - Mevcut [Z]% aylık büyüme devam

**Örnek 2: Sezonsal Peak**

- Metrik: Günlük transaction
- Mevcut: [X]M
- Tahmin: [Y]M (bayramda)
- Büyüme: [Z]%
- Zaman: [Bayram günleri - X gün]
- Varsayımlar:
  - Tarihsel bayram verisi
  - [Diğer faktörler]

---

## API Call Forecast

API | Mevcut (calls/day) | Launch Week | Launch Month | Steady State | Peak (calls/sec)
--- | --- | --- | --- | --- | ---
[API 1] | [X]K | [Y]K | [Z]K | [A]K | [B]
[API 2] | [X]K | [Y]K | [Z]K | [A]K | [B]
[API 3] | [X]K | [Y]K | [Z]K | [A]K | [B]

---

## Kapasite Planlaması

**Mevcut Kapasite:**
- Backend Server: [X] requests/sec capacity ([Y]% kullanımda)
- Database: [A] TPS capacity ([B]% kullanımda)
- Cache: [C] GB ([D]% kullanımda)
- Storage: [E] TB ([F]% kullanımda)

**Gerekli Kapasite (Launch Week):**
- Backend Server: [X] requests/sec needed → [Yeterli / Scale gerekli]
- Database: [Y] TPS needed → [Yeterli / Scale gerekli]
- Cache: [Z] GB needed → [Yeterli / Scale gerekli]

**Scaling Plan:**
- IF capacity yetersiz:
  - [Horizontal scaling: +X nodes]
  - [Vertical scaling: Y GB RAM artışı]
  - [Caching layer ekleme]
  - [Load balancer konfigürasyonu]
- Load test: [Tarih] - simulate [X]x expected traffic
- Auto-scaling: [Enable / Disable]

---

## Geçmiş Proje Trafik Verileri

Proje | Launch Öncesi | 1 Ay Sonra | 3 Ay Sonra | 6 Ay Sonra | Artış
--- | --- | --- | --- | --- | ---
[Proje 1] | [X]K/gün | [Y]K | [Z]K | [A]K | [B]%
[Proje 2] | [X]K/gün | [Y]K | [Z]K | [A]K | [B]%
[Proje 3] | [X]K/gün | [Y]K | [Z]K | [A]K | [B]%

---

# Best Practices

## İyi BRD Yazım Kuralları

**Yapılması Gerekenler:**
- Somut ve ölçülebilir hedefler yaz
- Sayısal değerler kullan (%, TL, saniye, kullanıcı sayısı)
- Edge case'leri düşün
- Kanal bazlı yaklaş
- Segment bazlı detaylandır

**Kaçınılması Gerekenler:**
- Belirsiz ifadeler: "uygun", "hızlı", "optimum", "mümkün"
- Genel tanımlar: "tüm müşteriler", "her kanal"
- Ölçülemez hedefler: "daha iyi", "iyileştir", "geliştir"
- Teknik detay eksikliği

---

**Son Güncelleme:** [Tarih]

**Versiyon:** 1.0

**Hazırlayan:** [İsim/Ekip]
