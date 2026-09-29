# TÜBİTAK 2209-A Gereksinim Yeniden Denetimi

> **Güncellik uyarısı:** Aşağıdaki satırlar 1 Eylül 2026 tarihlidir. Model o
> tarihten sonra 29 sınıftan 130 sınıfa çıkarıldı ve tarama zincirinde bir
> hata giderildi. Değişenler dosyanın sonundaki **9 Eylül 2026 eki**
> bölümündedir; eylül satırları bilerek olduğu gibi bırakılmıştır.

**Yeniden denetim tarihi:** 1 Eylül 2026
**Temel alınan snapshot:** `docs/audit/tubitak_requirement_traceability.md` (17 Temmuz 2026)
**Denetlenen sürüm:** `main` dalı, commit `fa2a8ac`

## Bu belge neden ayrı

17 Temmuz matrisi yerinde güncellenmedi. İki gerekçe var:

1. O belge kendini açıkça snapshot ilan ediyor. Bulgularının üzerine yazmak,
   denetimin hangi tarihte neyi gördüğünü ortadan kaldırır.
2. PDF'in `OZ-08` gereksinimi "uzman ve kullanıcı geri bildirimiyle iteratif
   geliştirme" kanıtı istiyor. İki tarihli denetimin farkı, tam olarak bu
   iterasyonun kanıtıdır. Snapshot'ı silmek, istenen kanıtı silmek olurdu.

Bu yüzden temmuz matrisi olduğu gibi durur; bu belge yalnız **değişen satırları**
kaydeder. Değişmeyen satırlar için temmuzdaki durum ve gerekçe geçerlidir.

## Değerlendirme kuralı

Temmuz matrisinin kuralları aynen geçerlidir. Özellikle: bir dosyanın veya
sınıfın varlığı tek başına "Tam" sayılmaz. Aşağıdaki her durum değişikliği,
kanıt sütununda gösterilen çalışan test, CI işi veya üretilmiş artefakta
dayanır.

## Yönetici özeti

Temmuzda 62 gereksinimden yalnız 1'i "Tam" idi. Bu denetimde 6 gereksinim
"Tam"a, 6 gereksinim daha zayıf bir durumdan "Kısmi"ye taşındı. Temmuzdaki 6
"Çelişkili" bulgunun 4'ü çözüldü; mobil istemci ile backend arasındaki
sözleşme uyuşmazlığı giderildi ve sözleşme artık CI'da sapma kontrolüyle
korunuyor. Kalan iki çelişki (`IZ-07` sonuç raporu, `BT-02` bütçe kalemi)
kod dışıdır. Ayrıca iOS kaynağı ilk kez gerçekten derlendi; `YN-09`'daki
platform çelişkisi bu sayede kapandı.

**2 Eylül günü içinde eklenen:** projenin kendi görüntü tanıma modeli eğitildi
ve mühürlü testle değerlendirildi (`OZ-06`, `YN-11`). Besin tanıma artık yalnız
dış sağlayıcıya bağlı değildir; cihaz üstünde çalışan 29 sınıflık bir model
uygulamaya paketlenmiştir.

Buna karşılık saha çalışması, etik kurul kararı ve ham veri bulunmadığından
`YN-01`–`YN-07`, `IZ-05`–`IZ-09` ve tüm `YE-*` satırları temmuzdaki durumlarını
korur. Bu satırlar kodla kapatılamaz.

## Durum dağılımı

`YN-09` temmuzda tek bir kutuya girmediği ("Kısmi/Çelişkili") için her iki
sütunda da dışarıda tutuldu; durumu aşağıdaki tabloda ayrıca ele alınıyor.
Kalan 61 gereksinim:

| Durum | 17 Temmuz | 1 Eylül |
|---|---|---|
| Tam | 1 | 7 |
| Kısmi | 19 | 22 |
| Kanıtsız | 30 | 25 |
| Eksik | 5 | 5 |
| Çelişkili | 6 | 2 |

## Değişen satırlar

| ID | Gereksinim | Temmuz | Eylül | Neyin değiştiği ve kanıtı |
|---|---|---|---|---|
| OZ-02 | Kamera görüntüsü YZ ile besin olarak tanınmalı. | Çelişkili | Kısmi | Sözleşme uyuşmazlığı giderildi: istemci `lib/core/constants/app_constants.dart` üzerinden kanonik `/api/v1/analyze-food` yolunu çağırıyor. `contracts/openapi.json` CI'daki sapma kontrolüyle korunuyor. Ayrıca cihaz üstünde çalışan kendi modelimiz uygulamaya paketlendi; kullanıcı sunucuya hiç gitmeden tarama yapabiliyor. **Kısmi kalma sebebi:** gerçek kullanıcıyla saha kanıtı yok. |
| OZ-04 | Besin adı, miktar, tarih-saat ve kalori kaydedilmeli. | Kısmi | Tam | `_MockFoodLog` tamamen kaldırıldı (kod tabanında 0 eşleşme). Kayıt backend testleriyle, görüntüleme `integration_test/p0_fixture_journey_test.dart` ile doğrulanıyor; bu test CI'da gerçek Android emülatöründe koşuyor. |
| OZ-05 | Kayıt/rapor e-posta veya SMS ile diyetisyene iletilmeli. | Kanıtsız | Kısmi | Her iki kanal da sağlayıcı mesaj kimliği üretiyor. E-posta Mailpit ile, SMS `local_outbox` sağlayıcısıyla kanıtlandı (`backend/tests/test_sms_local_outbox.py`, 7 test). **Kısmi kalma sebebi:** hiçbir mesaj gerçek operatöre çıkmadı; Twilio kimlikleri yok. |
| OD-01 | Besin tanıma, kalori ve sesli geri bildirim tek akışta birleşmeli. | Çelişkili | Kısmi | URL/şema ayrışması giderildi; zincir P0 yolculuk testinde uçtan uca koşuyor. **Kısmi kalma sebebi:** test sentetik taşıma katmanı kullanır, canlı backend'e karşı gerçek cihaz kanıtı yoktur. |
| OD-02 | Diyetisyene otomatik veri iletimi sağlanmalı. | Kısmi | Tam | `Future.delayed` simülasyonu kaldırıldı. Karşılıklı onaya dayalı atama akışı uygulandı: bekleyen istek listesi, kabul, red ve iptal uçları `backend/app/routers/food_router.py` içinde; `dietitian_accepted_at` / `rejected_at` alanları `b1c2d3e4f5a6` göçüyle eklendi. Hasta yalnız onayladığı diyetisyene rapor gönderebiliyor. |
| AH-02 | Kamera ile besin tanıma yapılmalı. | Çelişkili | Kısmi | `OZ-02` ile aynı gerekçe. |
| AH-03 | Kalori bilgisi hızlı ve erişilebilir verilmelidir. | Kanıtsız | Kısmi | Sonuç kartı kamera önizlemesinden bağımsız çiziliyor; önizleme yokken sonucun gizlendiği hata giderildi ve P0 testiyle korunuyor. **Kısmi kalma sebebi:** gerçek cihazda süre ölçümü yok. |
| AH-05 | Rapor e-posta/SMS ile otomatik iletilmeli. | Kanıtsız | Kısmi | `OZ-05` ile aynı kanıt. |
| AH-06 | Sesli komutlarla kullanım sağlanmalı. | Kısmi | Kısmi | Durum değişmedi ama kanıt güçlendi: ekrana dokunmadan başlatma için sallama algılama eklendi (`lib/shared/services/shake_detector.dart`, 8 birim testi; yürüme ve masaya bırakma senaryoları dahil). **Kısmi kalma sebebi:** görme engelli kullanıcıyla gerçek cihaz denemesi yok. |
| AH-07 | Kullanıcı sonucu onayladıktan sonra rapor oluşturulmalı. | Kısmi | Tam | Karar akışı (`FoodAnalysisDecisionRequest`/`Response`) backend'de zorunlu; onaysız kayıt oluşmuyor. P0 yolculuk testi "tarama onayı" adımını emülatörde geçiyor. |
| YN-06 | t-testi, varsayımlar sağlanıyorsa yapılmalı. | Çelişkili | Kanıtsız | Çelişki giderildi: sapma artık ön-kayıtlı. `analysis/PRE_ANALYSIS_PLAN.md` ana testin Wilcoxon signed-rank olduğunu, paired t-testin ancak protokol değişikliğiyle kabul edilebileceğini yazıyor. **Kanıtsız kalma sebebi:** gerçek veri yok. |
| YN-10 | Backend/veri katmanında MySQL kullanılmalı. | Kanıtsız | Tam | `backend/docker-compose.yml` MySQL 8.4 kullanıyor; Alembic göçleri CI'da boş veritabanında up/down/up olarak doğrulanıyor. SQLite yolu kaldırıldı. |
| YN-09 | Android ve iOS desteklenmeli. | Kısmi/Çelişkili | Kısmi | Çelişki giderildi. Temmuzda iOS kaynağı hazırdı ama hiç derlenmemişti; `scripts/qa/ios_release_checks.py` kendi belgesinde Xcode derlemesi iddia etmediğini yazıyordu. CI'ya macOS runner üzerinde imzasız derleme yapan `iOS Derleme` işi eklendi ve ilk koşuda geçti (koşu `33510763349`). Android tarafı emülatörde P0 yolculuk testiyle zaten kanıtlı. **Kısmi kalma sebebi:** imzalı arşiv, TestFlight dağıtımı ve gerçek iPhone/VoiceOver kanıtı yok; imzalama sertifikası gerekiyor. |
| OZ-06 | Etiketli veri seti ve makine öğrenmesi kullanılmalı. | Kanıtsız | Tam | 29 sınıflık model eğitildi ve mühürlü testle değerlendirildi (deney `20260902T090009Z-7871b6adb5`). Test accuracy 0,8375; macro F1 0,8268; top-3 0,9497. Veri kaynakları TurkishFoods-25 (Apache-2.0) ve Food-101; 17.051 görsel. Metrikler, karar dosyası ve provenance `ml/runs/` altında depodadır. |
| YN-11 | Python/TensorFlow ile YZ geliştirilmelidir. | Kanıtsız | Tam | TensorFlow 2.18 ile eğitim çalıştırıldı; `provenance.json` sürümü, platformu ve kilit dosyası özetini kaydeder. Model TFLite float16 olarak uygulamaya paketlendi. |
| KVKK-01 | *(yeni satır)* Sağlık verisi ve yurtdışı aktarım açık rızaya bağlanmalı. | — | Kısmi | KVKK m.6 ve m.9 gereği rıza artık uygulanabilir bir kapıdır: `image_cross_border_transfer` rızası yoksa `/analyze-food` 403 döner. Rıza kayıtları `/consents` uçlarıyla saklanır ve geri alınabilir. **Kısmi kalma sebebi:** aydınlatma metni yayımlanmadı (`privacy_notice_version=taslak-yayinlanmadi`). |

## Değişmeyen kritik satırlar

Aşağıdaki satırlar temmuzdaki durumlarını **aynen korur**. Hiçbiri kodla
kapatılamaz; her biri sende olmayan bir kaynağa veya senin bir kararına bağlıdır.

| ID | Gereksinim | Durum | Neden kapanmadı |
|---|---|---|---|
| OD-03 | Hipotez: sesli geri bildirim öğrenmeyi hızlandırır. | Kanıtsız | Ham veri, ön-kayıtlı analiz çıktısı yok. `analysis/results_manifest.json` çalıştırma kimliğini `NO-REAL-DATA-...` olarak veriyor. |
| YN-01, YN-02, YN-13, YN-14 | Anket, kullanılabilirlik testi, etik onam. | Kanıtsız / Eksik | Etik kurul kararı yok; katılımcı çalışması başlatılamaz. |
| IZ-05 – IZ-09 | Saha testi, sonuç raporu, konferans, paylaşım. | Kanıtsız / Çelişkili | Saha çalışması yapılmadı. |
| BT-01 – BT-04 | Bütçe kalemleri. | Kanıtsız / Çelişkili | Satın alma ve harcama belgeleri depoda değil. |
| YE-01 – YE-07 | Yaygın etki taahhütleri. | Kanıtsız | Çıktılar üretilmedi. |
| KY-01 | Kaynakça en az 20 çalışmayı desteklemeli. | Eksik | Depoda literatür tarama belgesi bulunamadı. |

## Denetim sınırları

- Bu denetim yalnız depodaki koda, testlere ve CI çıktılarına dayanır.
- Gerçek cihaz, gerçek kullanıcı ve gerçek sağlayıcı kanıtı üretilmemiştir.
- "Tam" işaretlenen satırlar, gereksinimin **yazılım tarafının** kanıtlandığını
  gösterir; hiçbiri saha geçerliliği iddia etmez.
- Sır değerleri okunmadı; `.env` yalnız yer tutucu/dolu olarak değerlendirildi.

---

## 9 Eylül 2026 eki

**Kapsam:** Yalnız 1 Eylül'den sonra değişen satırlar. Diğer bütün satırlar
için eylül durumu ve gerekçesi geçerlidir.

### Model kapsamı büyüdü

| ID | Eylül (1) | Ek (9) | Kanıt |
|---|---|---|---|
| OZ-06 | Tam — 29 sınıf, test accuracy 0,8375 | Tam — **130 sınıf**, test accuracy **0,7918**, macro F1 0,7793, top-3 0,9215 | Deney `20260908T060321Z-b000d69c58`, mühürlü test. Sınıf sayısı 4,5 katına çıkarken tek tahmin doğruluğu bir miktar bırakıldı; cevap verdiğinde isabet oranı korundu (0,8969). |
| YN-11 | Tam | Tam | TensorFlow 2.18; MobileNetV3Large (alpha 1,0). `tr222-v1` turu MobileNetV3Small ile kapıyı geçemediği için kapasite büyütüldü. |

1 Eylül metnindeki "29 sınıflık model" ifadesi bu tarihten itibaren geçmiş
bir durumu anlatır.

### Tanıma → kalori zinciri onarıldı

| ID | Eylül (1) | Ek (9) | Neyin değiştiği |
|---|---|---|---|
| OZ-02 / AH-02 | Kısmi | Kısmi (kapsam düzeldi) | Cihaz üstü tanıma sonrası onay akışı, kalori sorgusunu **kullanıcıya okunan Türkçe adı slug'a çevirerek** yapıyordu. `ev köftesi`, `sosisli sandviç`, `sütlaç` gibi 17 sınıfta bu anahtarın katalogda karşılığı yoktu: model doğru tanısa bile kayıt "Besin değeri bulunamadı" ile düşüyordu. Model artık sınıfın katalog anahtarını da taşıyor ve istemci kalori sorgusunu bu anahtarla yapıyor. 130 sınıfın 130'u doğrulanmış bir besin değeri kaydına bağlanmıştır. **Kısmi kalma sebebi değişmedi:** gerçek kullanıcıyla saha kanıtı yok. |
| AH-03 | Kısmi | Kısmi | Aynı düzeltme; kalori artık tanınan her sınıf için getirilebiliyor. Gerçek cihazda süre ölçümü hâlâ yok. |

**Regresyon kapıları:** `ml/tests/test_catalog_contract.py` her etiketin
doğrulanmış bir katalog kaydına çözüldüğünü CI'da doğrular (kayıt doğrulama
kuralları `NutritionixService._validated_local_record` ile aynıdır).
`test/unit/offline_recognizer_test.dart` paketlenen manifestte eksik anahtar
kalmadığını kontrol eder. Tanıyıcı, anahtarı olmayan bir etiket görürse
yüklenmez; sessizce yanlış sonuç üretmez.

### Belge tutarlılığı düzeltmeleri

| Belge | Sorun | Durum |
|---|---|---|
| `assets/models/model_manifest.json` | `notes` alanı 130 sınıflık modelde "29 sinif" diyordu; `catalog_keys` 58 etiketi kapsıyordu ve istemci bu alanı hiç okumuyordu. | Düzeltildi: 130 anahtar, istemci tarafından kullanılıyor. |
| `ml/MODEL_CARD.md` | Başlık tablosu MobileNetV3Large, mimari bölümü MobileNetV3Small diyordu. | Düzeltildi. |
| `ml/contracts/preprocessing.json` | Dağıtılan modelin "5 sınıf içerdiğini" söylüyordu. | Aşılmış MVP kapsamı olarak işaretlendi. |
| `backend/app/services/sms_templates.py` | Hiçbir yerden çağrılmayan ikinci bir SMS şablonu; gerçek metin `domain/report_messages.py`'den geliyor. | Silindi. |
| `docs/tubitak_sonuc_raporu.md` | Künye alanları yer tutucuydu; kaynakçada doğrulanamayan atıf vardı. | Künye dolduruldu, kaynakça yeniden düzenlendi. |

### Literatür iş paketi

| ID | Eylül (1) | Ek (9) | Kanıt |
|---|---|---|---|
| KY-01 | Eksik — depoda literatür tarama belgesi yok | **Tam** | `docs/literatur_taramasi.md`: künyesi yayıncı sayfası veya DOI üzerinden doğrulanmış 24 kayıt, arama yöntemi, dahil/hariç ölçütleri ve boşluk analizi. Başvurunun "en az 20 çalışma" taahhüdü karşılanmıştır. |

Aynı belge, başvuru kaynakçasındaki 12 kaydın doğrulama durumunu da ayrıca
kaydeder: üçü doğrulandı, dokuzu doğrulanamadı ve rapor kaynakçasında
kullanılmamaktadır. Sonuç raporundaki "Theodoridis vd., ASSETS 2022" atıfı
hiçbir dizinde bulunamadığı için çıkarılmıştır.

### Bütçe kaydı

| ID | Eylül (1) | Ek (9) | Durum |
|---|---|---|---|
| BT-01 – BT-04 | Kanıtsız / Çelişkili | **Değişmedi (Kanıtsız / Çelişkili)** | Harcama belgesi hâlâ yok. Yeni olan yalnız kayıt altyapısı: `docs/butce/onayli_butce.json` başvurudaki 4.500 + 4.500 = 9.000 TL planını referans alır, `docs/butce/harcama_kaydi.json` boş gerçek kayıttır, `scripts/qa/butce_mutabakat.py` kalem eşleşmesi, KDV aritmetiği, tarih sırası, mükerrer belge ve kalem aşımını denetleyip plan/gerçekleşen tablosunu üretir. CI'daki `Bütçe Mutabakatı` işi hem gerçek hem örnek kaydı doğrular ve örnek verinin gerçek kayda kopyalanmasını engeller. |

`BT-02`'nin çelişkisi (16 GB RAM ile 1 TB SSD'nin tek satırda birim dağılımsız
anılması) kayıt şemasında yapısal olarak kapatılmıştır: sarf kalemine işlenen
her harcama hangi alt kaleme ait olduğunu söylemek zorundadır ve alt kalem
toplamı kalem toplamına eşit olmadıkça mutabakat geçmez. `BT-03` için teslim
kanıtı alanı, teslim edilen artefaktın adını ve özetini ister; "geliştirme
yapıldı" ifadesi kabul edilmez.

**Bu satırları kapatan şey depo değil, girilecek faturadır.** Altyapı yalnız
tutarsız veya yer tutucu içeren bir kaydın rapora girmesini engeller.

### Değişmeyen kritik satırlar

`YN-01`–`YN-07`, `IZ-05`–`IZ-09`, `BT-*`, `YE-*` ve `KVKK-01` durumlarını
korur. Bu ek yalnız yazılım ve belge tarafını kapsar; hiçbiri saha
geçerliliği iddia etmez.
