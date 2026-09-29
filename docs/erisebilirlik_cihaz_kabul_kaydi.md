# Erişilebilirlik cihaz kabul kaydı

## Doğrulanmış durum

| Platform | Kanıt | Sonuç |
|---|---|---|
| Android / Samsung Galaxy S8 SM-G950F | Uygulama kurulumu, kamera ve cihaz üstü model; 20 fiziksel cihaz çıkarım ölçümü | Fiziksel Android yolu doğrulandı |
| Android semantik ve sesli akış | 123 otomatik erişilebilirlik, sesli komut ve rehber testi | Geçti |
| Android model gecikmesi | p50 3138,28 ms; p95 3570,78 ms | Model manifestine işlendi |
| iOS kaynak sınırları | İzinler, plugin kayıtları, ağ ve signing kapıları | `IOS_SOURCE_CHECK=PASS` |
| iOS derleme | GitHub Actions iOS derleme işi 33510763349 | Geçti |
| iOS / VoiceOver senaryo kabulü | Dokuz senaryo masa başında gözden geçirildi | **Fiziksel iPhone oturumu yapılmadı** |

## VoiceOver senaryo gözden geçirmesi (masa başı)

**Bu bir fiziksel iPhone oturumu değildir.** Projede Mac ve Xcode erişimi
olmadığı için uygulama gerçek bir iPhone'a kurulamamış, VoiceOver ile uçtan
uca denenmemiştir. Aşağıdaki tablo, dokuz senaryonun beklenen davranışının
kaynak kod ve otomatik semantik testleri üzerinden masa başında gözden
geçirildiğini kaydeder. Sonuç sütunu kabul değil, gözden geçirme durumudur.

Gerçek cihaz kanıtı `docs/voiceover_manual_test_report.md` dosyasında
`BLOCKED / NOT RUN` olarak durmaktadır ve bir iPhone oturumu yapılmadan
"VoiceOver uyumlu" veya "iOS kabulü tamamlandı" denemez.

| Senaryo | Beklenen | Sonuç |
|---|---|---|
| İlk açılış ve aydınlatma | Başlık, metin ve kabul/ret eylemleri doğru sırada okunur | masa başı gözden geçirildi |
| Kayıt/giriş | Alan adı, hata ve doğrulama kodu seslendirilir | masa başı gözden geçirildi |
| Kamera izni reddi | Sorun ve Ayarlar/manuel giriş alternatifi okunur | masa başı gözden geçirildi |
| Galeriden fotoğraf | Seçim, analiz durumu ve sonuç duyurulur | masa başı gözden geçirildi |
| Besin onayı | Ad, adet/porsiyon, gram ve kalori onaydan önce okunur | masa başı gözden geçirildi |
| Geçmiş ve geri alma | Kayıt, eylem ve geri alma süresi duyurulur | masa başı gözden geçirildi |
| Diyetisyen paylaşımı | Alıcı, kanal, kapsam ve açık onay okunur | masa başı gözden geçirildi |
| TTS/STT kesintisi | Eski ekran konuşması durur; yeni ekran rehberi bir kez başlar | masa başı gözden geçirildi |
| %200 metin ve koyu tema | Kritik içerik kesilmez, eylemler erişilebilir kalır | masa başı gözden geçirildi |

Masa başı gözden geçirmede beklenen davranışa aykırı bir bulgu çıkmamıştır;
bu, senaryoların gerçek cihazda geçtiği anlamına gelmez. Bir Mac ve iPhone
sağlandığında bu tablo `docs/voiceover_manual_test_report.md` ile birlikte
gerçek oturum kaydına çevrilmeli, cihaz modeli, iOS sürümü, tarih ve commit
SHA'sı yazılmalıdır.

