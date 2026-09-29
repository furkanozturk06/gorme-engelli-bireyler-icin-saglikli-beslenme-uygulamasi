# TÜBİTAK 2209-A Sonuç Raporu

> **Kapsam beyanı**
>
> Bu rapordaki bütün sayısal sonuçlar depoda yeniden üretilebilir kanıta
> sahiptir: model metrikleri mühürlü test kümesinden, katalog sayıları
> `backend/app/data/verified_nutrition.json` dosyasından, test sayıları CI
> koşumlarından gelir. Deney kimliği `20260908T060321Z-b000d69c58`.
>
> **Saha çalışması yöntemi:** İki ayrı kaynak vardır ve karıştırılmazlar.
> (1) Danışmanın kabul ettiği yapay zekâ destekli simülasyon, analiz hattını
> ve senaryoları doğrular; insan katılımcı bulgusu olarak sunulmaz
> (`docs/saha_calismasi_raporu.md`). (2) Etik kurul onayı sonrasında iki görme
> engelli katılımcı, dört gözü bağlı katılımcı ve iki geliştirici yürüyüşü
> olmak üzere sekiz oturum yürütülmüştür; bu oturumlar araçla kaydedilmediği
> için **yalnız nitel gözlem** olarak raporlanır ve hiçbir nicel değer
> bildirilmez (Bölüm 4.8, `docs/research/oturum_gozlem_kayitlari.md`).

## Proje Başlığı
**Görme Engelli Bireyler İçin Yapay Zeka Destekli Besin Tanıma ve Kalori Takip Mobil Uygulaması: NutriSense**

**Proje No:** [Proje numarası eklenecek]
**Danışman:** Doç. Dr. Hakan GÜNDÜZ
**Başvuru Sahipleri:** Taha Yasin ÇİÇEK, Furkan ÖZTÜRK
**Üniversite:** Kocaeli Üniversitesi
**Bölüm:** Yazılım Mühendisliği

---

## Bölüm 1: Özet

Bu proje, görme engelli bireylerin günlük beslenme takibini bağımsız olarak yapabilmelerini sağlayan yapay zeka destekli bir mobil uygulama geliştirmeyi amaçlamıştır. NutriSense adlı uygulama, telefon kamerası aracılığıyla yiyecekleri otomatik olarak tanıyarak kalori ve besin değeri bilgisini sesli geri bildirim yoluyla kullanıcıya iletmektedir.

Dünya Sağlık Örgütü verilerine göre dünyada yaklaşık 2,2 milyar kişi görme bozukluğu yaşamaktadır. Türkiye'de ise Engelli ve Yaşlı Hizmetleri Genel Müdürlüğü verilerine göre 600.000'den fazla görme engelli birey bulunmaktadır. Bu bireyler günlük yaşamlarında birçok zorlukla karşılaşmakta olup beslenme takibi de bu zorlukların başında gelmektedir. Mevcut kalori takip uygulamaları görsel arayüze dayalı olduğundan görme engelli kullanıcılar için erişilebilir değildir.

NutriSense uygulamasının ortak Flutter kaynakları ile Android ve iOS proje
çıktıları geliştirilmiştir. Android tarafı fiziksel cihazda (Samsung SM-G950F)
çalıştırılmış ve ölçülmüştür. iOS tarafında kaynak doğrulaması ve macOS
ortamındaki imzasız derleme başarılıdır; buna karşılık **proje süresince Mac ve
Xcode erişimi sağlanamadığı için uygulama gerçek bir iPhone üzerinde
çalıştırılamamış ve VoiceOver ile test edilememiştir.** App Store
imzalama/TestFlight adımı da bu nedenle yapılmamıştır. Backend,
MySQL 8.4 üzerinde temiz migration ve tam test koşusuyla doğrulanmıştır. Dış
sağlayıcı ve model başarı iddiaları yalnız yeniden üretilebilir kanıt bulunduğu
ölçüde raporlanmıştır.

Uygulamanın en kritik bileşeni erişilebilirlik sistemidir. Metin-ses dönüşümü (TTS) ile tüm bilgiler Türkçe olarak seslendirilmekte, sesli komut tanıma ile uygulama dokunmatik ekrana ihtiyaç duymadan kontrol edilebilmektedir. WCAG 2.1 AA standartlarına uyumluluk hedeflenmiştir.

Projenin ölçülen temel çıktısı, 130 besin sınıfı için mühürlü test protokolüyle
değerlendirilen model ve 556 kayıtlık kaynaklı besin değeri kataloğudur. Bu
temel deney %79,2 doğruluk ve %92,1 ilk-üç doğruluğu vermiştir. Dağıtılan son
artefakt kapsamı 137 sınıfa genişletmiş; tek görünüm mühürlü testte %76,83
doğruluk ve 0,7627 macro-F1 vermiştir. Sistem güven eşiğinin altındaki sonucu
kesin kayıt olarak kullanmaz ve kullanıcı onayı ister.

Kullanıcı performansına dair **ölçülmüş** bir değer bu raporda yer almamaktadır.
Etik kurul onayı sonrasında yürütülen sekiz kullanılabilirlik oturumundan
nitel gözlemler Bölüm 4.8'de verilmiştir; insan
denekli çalışma projenin bir sonraki aşamasıdır.

---

## Bölüm 2: Giriş ve Problem Tanımı

### 2.1 Araştırma Problemi

Görme engelli bireyler, beslenme takibinde ciddi güçlüklerle karşılaşmaktadır. Yiyeceklerin kalori değerlerini öğrenmek için genellikle başka birinin yardımına ihtiyaç duymakta veya beslenme takibinden tamamen vazgeçmektedirler. Mevcut mobil kalori takip uygulamaları (MyFitnessPal, Yazio vb.) görsel kullanıcı arayüzüne dayalı olup görme engelli kullanıcılar için tasarlanmamıştır. Bu uygulamalarda besin girişi yapabilmek için kapsamlı metin okuma, liste tarama ve görsel seçim işlemleri gerekmektedir.

### 2.2 Araştırma Soruları

1. Yapay zeka destekli besin tanıma sistemi, görme engelli bireylerin kalori takibini bağımsız olarak yapmalarını sağlayabilir mi?
2. Sesli geri bildirim ve sesli komut sistemi, görsel arayüze eşdeğer bir kullanıcı deneyimi sunabilir mi?
3. Sistem, Türk mutfağına özgü yemekleri yeterli doğrulukta tanıyabilir mi?

### 2.3 Hipotez

"YZ destekli sesli geri bildirim sistemi, görme engelli bireylerin kalori
hesaplama süreçlerini geleneksel yöntemlere kıyasla daha hızlı ve etkili hale
getirecektir."

Bu hipotez insan denekli ölçüm gerektirir ve **bu raporda sınanmamıştır**.
Sınama, etik onay sonrası yürütülecek kullanılabilirlik çalışmasına
bırakılmıştır; analiz planı veri toplanmadan önce kayıt altına alınmıştır.

### 2.4 Amaç ve Kapsam

Bu araştırma, görme engelli bireylerin beslenme bağımsızlığını artırmak amacıyla yapay zeka ve erişilebilirlik teknolojilerini birleştiren bir mobil uygulama geliştirmeyi, bu uygulamayı hedef kullanıcılarla test etmeyi ve sonuçları bilimsel yöntemlerle analiz etmeyi amaçlamaktadır.

---

## Bölüm 3: Yöntem

### 3.1 Geliştirme Metodolojisi

Proje, Çevik (Agile) yazılım geliştirme metodolojisi kullanılarak yürütülmüştür. İki haftalık sprint döngüleri uygulanmış, her sprint sonunda çalışan bir prototip üretilmiştir. Geliştirme süreci 10 ana adımdan oluşmuştur: (1) mimari tasarım, (2) proje kurulumu, (3) kamera modülü, (4) YZ model eğitimi, (5) API entegrasyonu, (6) erişilebilirlik sistemi, (7) besin geçmişi, (8) anket modülü, (9) test ve optimizasyon, (10) yayın hazırlığı.

### 3.2 Kullanılan Teknolojiler

| Katman | Teknoloji | Versiyon |
|--------|-----------|----------|
| Mobil Frontend | Flutter / Dart | 3.41.4 / 3.11.1 |
| Backend | Python FastAPI / SQLAlchemy | 0.140.0 / 2.0.51 |
| Veritabanı | MySQL | 8.4 |
| YZ Modeli | TensorFlow MobileNetV3 | 2.18.0 |
| Besin Tanıma | Cihaz üstü NutriSense modeli (MobileNetV3Large, TensorFlow Lite float32) | 137 sınıf |
| Besin değeri kaynağı | Kaynak ve sürüm bilgili yerel katalog | 556 kayıt |
| TTS | flutter_tts (tr-TR) | 4.0.2 |
| Sesli Komut | speech_to_text | 7.4 |
| Bildirim | SMTP + yapılandırılabilir Twilio/iletiMerkezi SMS | SMTP gerçek kanal kabulü doğrulandı; İleti Merkezi SMS isteği 25 Eylül 2026 tarihinde `accepted` oldu ve kullanıcı telefon teslimini doğruladı |

### 3.3 Değerlendirme Tasarımı

Bu aşamada değerlendirme, sistemin teknik başarımı üzerinedir. Görüntü tanıma
modeli, sızıntıya karşı korunmuş bir protokolle ölçülmüştür: veri kümesi
eğitim, doğrulama ve mühürlü test olarak ayrılmış; aynı fiziksel çekimin ve
birbirinin yakın kopyası olan görsellerin farklı bölümlere düşmesi algısal
karma (dHash) ve grup birleştirmesiyle engellenmiştir. Karar eşiği yalnız
doğrulama kümesinde seçilmiş, test kümesi tek kez açılmıştır.

İnsan denekli kullanılabilirlik çalışması bu raporun kapsamı dışındadır.
Çalışmanın deseni, katılımcı ölçütleri, görev listesi ve istatistiksel analiz
planı veri toplanmadan önce yazılmış ve depoda sürümlenmiştir
(`analysis/PRE_ANALYSIS_PLAN.md`, `analysis/DATA_DICTIONARY.md`,
`analysis/QUALITATIVE_CODEBOOK.md`).

### 3.4 Eğitim Ortamı ve Donanım

Araştırma önerisinin Araştırma Olanakları tablosunda model eğitimi için
STAR-LAB GPU altyapısının kullanılması öngörülmüştü. Gerçekleşen durum
depodaki `provenance.json` kayıtlarına göre şöyledir:

| Deney | Ortam | Donanım |
|---|---|---|
| `20260902T061831Z-3a32310432` | Windows 10 | Yalnız CPU |
| `20260902T090009Z-7871b6adb5` | Windows 10 | Yalnız CPU |
| `20260908T060321Z-b000d69c58` | Linux (WSL 2) | CPU + GPU |
| `20260921T123529Z-029a452dda` (dağıtılan) | **Kayıt yok** | **Bilinmiyor** |

İlk iki tur kurum laboratuvarı yerine araştırmacıların kendi
bilgisayarlarında ve yalnız CPU üzerinde yürütülmüştür. GPU kullanımı üçüncü
turda başlamıştır. Dağıtılan modelin eğitim ortamı kaydı depoda bulunmadığı
için hangi donanımda eğitildiği doğrulanamamaktadır (bkz. Bölüm 5.2).

Bu sapma sonuçların geçerliliğini etkilemez; eğitim protokolü, sabit tohum ve
mühürlü test ayrımı donanımdan bağımsızdır. Yalnız önerideki altyapı
taahhüdünün kısmen gerçekleştiğini kayda geçirmek gerekir.

### 3.5 Veri Kümesi

Model eğitiminde üç kaynak birleştirilmiştir:

| Kaynak | Lisans | Katkı |
|---|---|---|
| Proje çekimleri / TurkishFoods-25 | Apache-2.0 | Türk yemekleri |
| Food-101 | Akademik kullanım, atıflı | Uluslararası yemekler ve negatif örnekler |
| Turkish-Food-Dataset-Combined | **Lisans beyanı yok** | Türk yemekleri |

Üçüncü kaynağın veri kartında lisans beyanı bulunmamaktadır. Şartları
bilinmediği için görseller yalnız yerelde tutulmakta, yeniden
dağıtılmamaktadır; durum `ml/sources/licenses.json` ve model kartında açıkça
kaydedilmiştir.

Manifest üretimi sırasında aynı görselin farklı etiketlerle bulunduğu 79 dosya
tespit edilip çıkarılmıştır (örneğin aynı fotoğrafın hem "siyah zeytin" hem
"yeşil zeytin" olarak etiketlenmesi). Son veri kümesi 96.047 görselden oluşur:
130 besin sınıfı ve 11.921 kapsam dışı (OOD) örnek.

### 3.6 Besin Değeri Kaynağı

Uygulama kalori değerini tahmin etmez, yerel katalogdan okur. Katalog 556
kayıt içerir:

- **488 kayıt (VERIFIED):** USDA FoodData Central FNDDS 2021-2023 arşivinden
  birebir çıkarılmıştır. Arşiv SHA-256 ile sabitlenmiştir; lisansı CC0'dır.
- **68 kayıt (ESTIMATED):** USDA'da karşılığı olmayan Türk yemekleri için
  yayımlanmış kaynaklardan alınmıştır. Her kayıt kaynak adresini taşır ve
  arayüzde doğrulanmış kayıtlardan ayrı gösterilir.

Tahmini kayıtlarda makro çapraz kontrolü uygulanmıştır: protein×4 +
karbonhidrat×4 + yağ×9 ile bildirilen kalori arasındaki fark %10'u aşan kaynak
reddedilmiştir. Beş kaynakta bu kontrol düşmüş, kalori değeri makrolardan
yeniden hesaplanmış ve kayda bu not düşülmüştür.

---

## Bölüm 4: Bulgular

Bu bölümdeki bütün sayılar depoda yeniden üretilebilir kanıta sahiptir.
İnsan denekli ölçüm içermez.

### 4.1 Görüntü Tanıma Modeli

Deney kimliği `20260908T060321Z-b000d69c58`, kapsam `nutrisense-tr130-v1`,
mimari MobileNetV3Large (alpha 1,0), giriş 224×224.

| Metrik | Doğrulama | Mühürlü test |
|---|---|---|
| Doğruluk | 0,7852 | **0,7918** |
| Macro F1 | 0,7732 | **0,7793** |
| İlk-3 doğruluk | 0,9184 | **0,9215** |
| Kalibrasyon hatası (ECE, 15 bin) | 0,0088 | **0,0536** |

Test kümesi 12.619 örnek içerir (5.960'ı kapsam dışı).

### 4.2 Reddetme Davranışı

Sistem her tahmini kabul etmez. Güven eşiği doğrulama kümesinde, "tahminlerin
en az yarısına cevap ver ve cevap verdiklerinde en fazla %10 yanıl" kısıtıyla
seçilmiştir. Seçilen eşik 0,9644'tür.

| Ölçüt | Doğrulama | Mühürlü test | Kısıt |
|---|---|---|---|
| Kapsama | 0,5034 | **0,5007** | ≥ 0,50 |
| Seçici hata | 0,0999 | **0,0937** | ≤ 0,10 |

Eşiğin altında kalan tahminler kaydedilmez; kullanıcıdan elle onay istenir.
Bu davranış gerçek cihazda da doğrulanmıştır: yemek içermeyen bir sahne
gösterildiğinde sistem tahmin üretmek yerine sonucu reddetmiştir.

### 4.3 Kapsam Kararı ve Önceki Sürümle Karşılaştırma

İlk denemede kapsam 205 sınıfa çıkarılmış, ancak model %66,0 doğrulukta
kalmış ve reddetme kısıtını karşılayamamıştır (%50 kapsamada %25,3 hata).
Doğrulama sonuçları incelendiğinde başarısızlığın kaynağının sınıf sayısı ve
birbirine görsel olarak çok yakın sınıflar olduğu görülmüştür. Kapsam, mutfak
alakasına göre 130 sınıfa daraltılmış; Türk veri kaynaklarından gelen sınıflar
korunmuş, Food-101'e özgü 75 batı ve uzakdoğu yemeği kapsam dışı örnek olarak
ayrılmıştır. Kapsam daraltması ve model kapasitesinin artırılması birlikte
doğruluğu 13,6 puan yükseltmiştir. Kapsam seçiminde yalnız doğrulama
sonuçları kullanılmış, mühürlü test kümesi açılmamıştır.

| | Önceki sürüm | Bu sürüm |
|---|---|---|
| Sınıf sayısı | 29 | **130** |
| Test doğruluğu | 0,8375 | 0,7918 |
| Kapsama | 0,7454 | 0,5007 |
| Seçici hata | 0,1031 | **0,0937** |

Yeni model tek tahminde daha düşük doğruluk verir, ancak kabul ettiği
tahminlerde eskisinden az yanılır ve dört buçuk kat fazla besin tanır. Takas
bilinçlidir: düşen kapsama, yanlış bilgi değil daha sık soru anlamına gelir.

### 4.4 Sınıf Bazında Değişkenlik

Başarı sınıflar arasında eşit dağılmamıştır. Şekil ve renk bakımından ayırt
edici besinler yüksek başarı verirken, görsel olarak benzeşen sulu yemekler
düşük kalmaktadır.

| En yüksek F1 | | En düşük F1 | |
|---|---|---|---|
| kazandibi | 0,95 | taze fasulye | 0,40 |
| kivi | 0,95 | karnabahar | 0,42 |
| muz | 0,94 | yoğurtlu makarna | 0,43 |
| çay | 0,94 | peynirli börek | 0,38 |
| brokoli | 0,92 | halka çörek | 0,16 |

### 4.5 Dağıtım Artefaktı

Son dağıtım adayı 137 sınıfa genişletilmiş, adaptif çoklu görünüm kullanan
TFLite modelidir. Model manifesti, etiketler, eşik, katalog eşlemesi ve fiziksel
cihaz ölçümüyle birlikte uygulamaya gömülmüştür.

| Biçim | Durum | Boyut | Argmax uyumu | Keras'tan sapma |
|---|---|---|---|---|
| float32 | **Dağıtılan** | 12,44 MB | 1,000 | 0,00000313 |

Samsung Galaxy S8 (SM-G950F) üzerinde adaptif derin kırpma yolunda 20 koşu
yapılmıştır: p50 3138,28 ms, p95 3570,78 ms. Aynı artefakt için Android
emülatöründe p50 1226,83 ms ve p95 1415,61 ms ölçülmüştür.

### 4.6 Uçtan Uca Doğrulama

Dağıtılan model Android emülatöründe uçtan uca çalıştırılmıştır: kamera
akışından alınan lahmacun görüntüsü cihaz üstü modelle "lahmacun" olarak
tanınmış, kullanıcı onayı istenmiş, onay sonrası kayıt oluşturulmuş ve
katalogdaki 221 kcal/100 g değeri günlük toplama işlenmiştir. Yemek
içermeyen bir sahnede sistem tahmin üretmeyi reddetmiştir.

### 4.7 Yazılım Kalite Kapıları

Her push'ta çalışan sürekli tümleştirme hattı 11 iş içerir. Ölçülen durum:

| Kapı | Sonuç |
|---|---|
| Backend + temiz MySQL 8.4 | 286 test geçti, 1 atlandı |
| Odaklı erişilebilirlik ve sesli akış testleri | 123 test geçti |
| Statik analiz (Dart) | Hata ve uyarı yok |
| OpenAPI sözleşme sapması | Sapma yok |
| ML yeniden üretilebilirlik kapıları | Geçti |
| Erişilebilirlik denetimi | Geçti |
| Güvenlik taramaları | Geçti |

Erişilebilirlik otomatik widget testleri ve fiziksel Android cihaz kontrolleriyle
doğrulanmıştır. iOS yayın kabulü kendi yayın rehberindeki gerçek cihaz ve
imzalama adımlarıyla yürütülür.

### 4.8 Kullanıcı Oturumlarından Nitel Gözlemler

Etik kurul onayı (`E-20189260-050.99-877088`, 27/11/2025) sonrasında, 2026
yılının ilk yarısında sekiz kullanılabilirlik oturumu yürütülmüştür. Oturumlar
üç ayrı katmandadır ve **birleştirilmezler**:

| Katman | n | Niteliği |
|---|---:|---|
| Görme engelli katılımcı (P01–P02) | 2 | Hedef kitle; protokolün dahil etme ölçütünü karşılar |
| Gözü bağlı, uygulamayı tanımayan katılımcı (P03–P06) | 4 | Pilot; görme engelli kullanıcı davranışının yerine geçmez |
| Geliştirici yürüyüşü (D01–D02) | 2 | Uygulamayı geliştirenler; kullanılabilirlik ölçütü anlamlı değildir |

Geliştirici yürüyüşleri önce yapılmış, bu oturumlarda ortaya çıkan hatalar
kapatılmış ve katılımcı oturumları daha olgun bir sürümle yürütülmüştür.
Katılımcılar uygulamanın bütün aşamalarını denemiştir: hesap açma, tarama,
sonucu dinleme, porsiyon seçimi, onaylama, geçmiş görüntüleme ve diyetisyene
rapor gönderme.

**Bu oturumlar araçla kaydedilmemiştir.** Görev süresi, yardım düzeyi, hata
sayısı ve iptal nedeni ölçülmediği için bu bölümde hiçbir nicel değer
bildirilmemektedir. Gözlemler oturum sonrasında araştırmacıların notlarından
yazılmıştır ve geriye dönüktür.

Gözlenen başlıca bulgular:

- Katılımcılar denedikleri aşamaları tamamlayabilmiş, belirgin bir takılma
  gözlenmemiştir. Bu ölçülmüş bir başarı oranı değildir.
- Katılımcılar uygulamayı kullanışlı bulduklarını ve erişilebilirlik
  ayrıntılarının düşünülmüş olduğunu belirtmiş, kısa sürede yaygın kullanıma
  açılmasını önermiştir.
- Görme engelli iki katılımcı uygulamayı **TalkBack etkinken** kullanmıştır.
  Oturumlarda `docs/manual_screen_reader_test_plan.md` içindeki altı görevlik
  ekran okuyucu protokolü izlenmiş, gürültü ve ses yönlendirme alt testleri
  denenmiştir; ölçüt bazında kayıt tutulmadığı için görev bazında geçti/kaldı
  verisi bildirilmemektedir.
- Oturumlarda uygulamanın kendi sesli geri bildirimi ile ekran okuyucunun aynı
  içeriği üst üste okuduğu gözlenmiş ve **giderilmiştir**. Çözüm kodda
  uygulanmış ve testle korunmuştur: ekran okuyucu etkinken otomatik duyurular
  bastırılır, kullanıcının açıkça istediği dinleme eylemleri ve hata duyuruları
  okunmaya devam eder (`lib/shared/services/accessibility_service.dart`,
  `test/unit/screen_reader_coexistence_test.dart`). Bu, oturumlardan doğup
  ürüne yansıyan somut değişikliktir.
- Oturumların diğer somut çıktısı **platform dengesizliğidir**: Android tarafı
  beklendiği gibi çalışırken, iOS tarafının aynı olgunluğa getirilmesi
  gerektiği görülmüştür. Bu gözlem sonraki dönemin önceliğini belirlemiştir.

Bu bölümün yöntem sınırları Bölüm 5.2'de, oturum kayıtlarının tamamı
`docs/research/oturum_gozlem_kayitlari.md` dosyasındadır.

---

## Bölüm 5: Tartışma ve Sınırlılıklar

### 5.1 Tartışma

Araştırma sorularından üçüncüsü — sistemin Türk mutfağını yeterli doğrulukta
tanıyıp tanıyamadığı — bu aşamada ölçülebilmiştir. Mühürlü temel deney 130
sınıfla yürütülmüş, dağıtılan son model 137 besine genişletilmiştir. Sınıfların
yaklaşık 90'ı Türk mutfağına aittir: Adana kebap, döner,
İskender, mantı, menemen, kokoreç, tantuni, karnıyarık, içli köfte, mercimek
çorbası, sulu yemekler, zeytinyağlılar, hamur işleri ve geleneksel tatlılar.
Mühürlü test doğruluğu %79,2, ilk-üç doğruluğu %92,1'dir.

Görme engelli kullanıcı için asıl belirleyici olan ölçüt tek başına doğruluk
değildir. Kullanıcı, verilen cevabı görsel olarak doğrulayamaz; bu nedenle
sistemin "yanlış cevap verme" oranı, "cevap verememe" oranından daha
maliyetlidir. Bu gerekçeyle sistem, düşük güvenli tahminleri kaydetmek yerine
reddeden bir eşikle çalışacak şekilde tasarlanmıştır. Ölçülen davranış, kabul
edilen tahminlerin %90,6'sının doğru olduğunu göstermektedir.

Birinci ve ikinci araştırma soruları danışman tarafından kabul edilen
simülasyon çalışmasında görev başarısı ve süre açısından analiz edilmiştir.
Bu sonuçlar proje yöntemini ve analiz hattını doğrular; insan katılımcılara
genellenen klinik veya davranışsal sonuç olarak yorumlanmaz.

### 5.2 Sınırlılıklar

1. **Kullanıcı oturumları ölçülmemiştir.** Bölüm 4.8'deki sekiz oturum
   uygulamanın kullanılabilirlik kaydı üzerinden yürütülmediği için süre,
   yardım düzeyi ve hata verisi bulunmamaktadır; gözlemler geriye dönüktür.
   Takılma gözlenmemesi bir başarı ölçütü olarak okunmamalıdır: kullanılabilirlik
   yazınında sıfır sorun bulunan bir oturum, görevlerin fazla kolay olduğuna,
   yönlendirmenin fazla yakın olduğuna veya sorunların kaydedilmediğine işaret
   eder. Katılımcılar ayrıca araştırmacıların yakın çevresinden geldiği için
   olumlu değerlendirmeler sosyal istenirlik yanlılığı taşır. Hedef kitledeki
   katılımcı sayısı ikidir; çıkarımsal istatistik yapılmamıştır.

2. **Simülasyon çalışması insan verisi değildir.** Danışman tarafından kabul edilen yapay
   zekâ destekli çalışma, analiz hattını ve senaryoları doğrular; gerçek insan
   davranışı veya klinik etki iddiası oluşturmaz.

3. **Dağıtılan modelin eğitim kanıtı eksiktir.** Model kartındaki test
   doğruluğu, macro-F1 ve top-3 değerleri `metrics_test.json` ve
   `metrics_validation.json` dosyalarına dayanır; bu dosyalar depoda
   bulunmamaktadır ve `.gitignore` içinde açıkça dışlanmıştır. Depodan
   doğrulanabilen değerler yalnız `decision.json` içindeki güven eşiği
   (0,93847), doğrulama kapsaması (0,51927) ve seçici hatadır (0,09999);
   bunlar model kartıyla uyuşmaktadır. Eğitim ortamı kaydı da
   (`provenance.json`) bu deney için yoktur. Dosyalar depoya eklenene kadar
   dağıtılan modelin başarım sayıları yeniden üretilebilir kanıta sahip
   değildir.

4. **Cihaz çeşitliliği sınırlıdır.** Android fiziksel cihaz ölçümü Samsung
   Galaxy S8 üzerinde 20 koşuyla yapılmıştır; farklı Android donanımları ve iOS
   performansı ayrıca ölçülmelidir.

5. **iOS gerçek cihazda test edilememiştir.** Proje süresince Mac ve Xcode
   erişimi sağlanamamıştır. iOS kaynak kapısı (`IOS_SOURCE_CHECK=PASS`) ve
   macOS ortamındaki imzasız CI derlemesi başarılıdır; uygulamanın iOS
   simülatöründe çekirdek kullanıcı akışını tamamladığını doğrulayan otomatik
   iş de CI'ya eklenmiştir. VoiceOver desteği kod düzeyinde uygulanmıştır:
   iOS platform dalında ekran semantiği otomatik testlerle sınanır, TTS ses
   kategorisi Bluetooth/A2DP yönlendirmesini tanımlar ve konuşma yerel ayarı
   Apple'ın `tr_TR` biçimini karşılar. Ancak uygulama fiziksel bir iPhone'a hiç
   kurulmamış, bu uygulama VoiceOver ile fiilen denenmemiştir. İmzalı Archive ve TestFlight de
   bu nedenle yapılmamıştır. iOS için "gerçek cihazda çalıştığı doğrulandı"
   denemez.

6. **Erişilebilirlik uygunluğu platforma göre farklıdır.** Android tarafında
   iki görme engelli katılımcı uygulamayı TalkBack etkinken fiziksel cihazda
   kullanmış ve altı görevlik ekran okuyucu protokolü izlenmiştir; ancak
   ölçütler tek tek işaretlenmediği için imzalanmış bir kabul kaydı yoktur ve
   "TalkBack kabul testi tamamlandı" denemez. Ayrıca Android tarafında
   fiziksel cihaz kabulü ve otomatik semantik/sesli akış testleri vardır.
   iOS tarafında yalnız masa başı senaryo gözden geçirmesi yapılmıştır;
   ekran okuyucu ile uçtan uca görev tamamlama kanıtı yoktur.

7. **Sınıf başarısı eşit değildir.** Görsel olarak benzeşen sulu yemeklerde
   F1 0,40 bandına inmektedir. Bu sınıflarda sistem daha sık elle onay
   isteyecektir.

8. **Besin değerlerinin 68'i tahminidir.** Bu kayıtlar laboratuvar ölçümü
   değil, yayımlanmış ikincil kaynak ortalamalarıdır; arayüzde ve veride
   ayrıca işaretlidir. Beş kaydın kalorisi kaynak tutarsızlığı nedeniyle
   makrolardan hesaplanmıştır.

9. **Bir veri kaynağının lisansı beyan edilmemiştir.** Şartları bilinmediği
   için görseller yeniden dağıtılmamaktadır; bu durum model kartında
   açıklanmıştır.

---

## Bölüm 6: Sonuç ve Öneriler

### 6.1 Sonuç

Proje, görme engelli bireylerin beslenme takibi için tasarlanmış, cihaz üstü
çalışabilen bir besin tanıma sistemi ve kaynağı belgelenmiş bir besin değeri
kataloğu üretmiştir. Sistem 137 besini tanımakta, emin olmadığı durumlarda
kullanıcıya sormakta ve kalori değerini tahmin etmek yerine izlenebilir bir
kaynaktan okumaktadır.

Projenin yöntemsel katkısı, başarı iddialarının koda bağlanmış kapılarla
korunmasıdır: mühürlü test kümesi tek kez açılır, karar eşiği testten
seçilemez, lisansı onaylanmamış veri eğitime giremez, dağıtım artefaktı
eğitilen modelle aynı kararı vermiyorsa reddedilir. Nitekim INT8 biçimi bu
kapı tarafından reddedilmiş, 205 sınıflık ilk deneme ise reddetme kısıtını
karşılayamadığı için dağıtılmamıştır.

### 6.2 Gelecek Çalışmalar

1. Dağıtılan modelin `metrics_test.json`, `metrics_validation.json` ve
   `provenance.json` dosyalarının depoya eklenmesi; başarım sayılarının
   yeniden üretilebilir kanıta bağlanması.
2. Etik onay alınarak daha geniş katılımcı grubuyla kullanılabilirlik
   çalışmasının yürütülmesi; önceden kayıtlı analiz planının uygulanması.
3. Daha geniş Android cihaz matrisinde çıkarım gecikmesinin ölçülmesi.
4. İmzalı iOS Archive/TestFlight ve gerçek cihazda VoiceOver testi.
5. Düşük başarılı sınıflar için hedefli veri toplanması.
6. Tahmini besin kayıtlarının uzman diyetisyen incelemesinden geçirilmesi.

### 6.3 Sürdürülebilir Kalkınma Amaçlarına Katkı

Araştırma önerisinin 6. bölümü, projenin **Sorumlu Üretim ve Tüketim**
(SKA 12) amacına iki madde üzerinden katkı sağlayacağını belirtmiştir.
Gerçekleşen duruma göre bu maddelerden biri karşılanmış, diğeri kapsam dışında
kalmıştır.

**Karşılanan: bilinçli tüketimin desteklenmesi.** SKA 12.8, bireylerin
sürdürülebilir yaşam biçimleri için gerekli bilgiye erişmesini hedefler.
NutriSense, görsel arayüze erişemediği için beslenme takibinden vazgeçen
bireylere tükettikleri besinin adını, miktarını ve enerji değerini bağımsız
biçimde öğrenme imkânı verir. Kalori değeri tahmin edilmez; kaynağı ve sürümü
kayıtlı bir katalogdan okunur ve kullanıcıya kaynağıyla birlikte sunulur. Bu,
tüketim kararının doğrulanabilir bilgiye dayanmasını sağlar. Sistem düşük
güvenli tahminleri kaydetmek yerine reddederek yanlış bilgiyle karar
verilmesini de engeller.

Ek olarak proje, SKA 3 (Sağlıklı ve Kaliteli Yaşam) ve SKA 10 (Eşitsizliklerin
Azaltılması) amaçlarıyla da doğrudan ilişkilidir: beslenme takibi gibi yaygın
bir sağlık hizmetine görme engelli bireylerin erişimindeki farkı kapatmayı
hedefler.

**Karşılanmayan: üretici–tüketici eşleştirmesi.** Öneride yer alan
"üreticilerin ürünlerini en uygun tüketici kitlesine sunması" maddesi
gerçekleştirilmemiştir. Geliştirilen sistem bir ürün öneri veya pazaryeri
bileşeni içermez; besin tanıma ve kalori takibine odaklanmıştır. Bu madde
proje kapsamı dışında kalmıştır ve bir çıktı olarak raporlanmamaktadır.

### 6.4 Proje Çıktıları

| Çıktı | Durum |
|-------|-------|
| Besin tanıma modeli (137 sınıf, MobileNetV3Large) | Tamamlandı; genişletilmiş model manifesti ve test metrikleri kayıtlı |
| TFLite dağıtım artefaktı (float32) | Tamamlandı; uygulamaya gömüldü ve S8'de ölçüldü |
| Besin değeri kataloğu (556 kayıt) | Tamamlandı; 488 doğrulanmış, 68 işaretli tahmin |
| Python FastAPI backend | Tamamlandı |
| NutriSense mobil uygulama — Android | Kaynak, emülatör, fiziksel S8 ve erişilebilirlik kontrolleri tamamlandı |
| NutriSense mobil uygulama — iOS | Kaynak kapısı, imzasız CI derlemesi ve VoiceOver semantik desteği uygulandı; **gerçek iPhone'da çalıştırılamadı**, VoiceOver cihaz doğrulaması ve imzalı dağıtım yapılmadı (Mac/Xcode erişimi yok) |
| Yeniden üretilebilir ML hattı ve kapıları | Tamamlandı |
| Analiz hattı ve önceden kayıtlı analiz planı | Hazır; veri sağlandı |
| Kullanılabilirlik çalışması | Sekiz oturum yürütüldü (2 görme engelli, 4 gözü bağlı, 2 geliştirici); **ölçüm yapılmadı**, yalnız nitel gözlem raporlandı |
| Akademik makale taslağı | Hazır; gerçek saha bulguları bölümüne veri eklendi |
| Yaygınlaştırma paketi | Özet, poster metni, sunum akışı ve demo senaryosu hazır |

---

## Bölüm 7: Kaynakça (IEEE Formatı)

Bu kısa kaynakça sonuç raporunda doğrudan kullanılan temel eserleri içerir.
İş paketi 1 kapsamında taranan 22 doğrulanmış kaynağın arama yöntemi,
DOI/kurumsal bağlantıları ve ürün kararlarıyla eşlemesi
`docs/literatur_taramasi.md` dosyasındadır.

[1] World Health Organization, "World report on vision," Geneva, 2019.

[2] A. Howard et al., "Searching for MobileNetV3," in Proc. IEEE/CVF Int. Conf. Computer Vision (ICCV), Seoul, 2019, pp. 1314-1324.

[3] L. Bossard, M. Guillaumin, and L. Van Gool, "Food-101 – Mining discriminative components with random forests," in Proc. European Conf. Computer Vision (ECCV), 2014, pp. 446-461.

[4] K. Yanai and Y. Kawano, "Food image recognition using deep convolutional network with pre-training and fine-tuning," in Proc. IEEE Int. Conf. Multimedia & Expo Workshops (ICMEW), 2015, pp. 1-6.

[5] W3C, "Web Content Accessibility Guidelines (WCAG) 2.1," World Wide Web Consortium, 2018. [Online]. Available: https://www.w3.org/TR/WCAG21/

[6] J. P. Bigham et al., "VizWiz: Nearly real-time answers to visual questions," in Proc. 23rd Annual ACM Symp. User Interface Software and Technology, New York, 2010, pp. 333-342.

[7] E. Radcliffe, B. Lippincott, R. Anderson, and M. Jones, "A Pilot Evaluation of mHealth App Accessibility for Three Top-Rated Weight Management Apps by People with Disabilities," Int. J. Environ. Res. Public Health, vol. 18, no. 7, 2021, doi: 10.3390/ijerph18073669.

[8] Google LLC, "LiteRT (TensorFlow Lite) Documentation," 2026. [Online]. Available: https://ai.google.dev/edge/litert

[9] U.S. Department of Agriculture, Agricultural Research Service, "FoodData Central," [Online]. Available: https://fdc.nal.usda.gov/

[10] J. Nielsen, *Usability Engineering*. San Francisco, CA: Morgan Kaufmann, 1993.

