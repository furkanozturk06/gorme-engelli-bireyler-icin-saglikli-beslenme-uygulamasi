# Kullanılabilirlik oturumları — geriye dönük gözlem kaydı

> **Bu kaydın niteliği.** Aşağıdaki gözlemler oturumlar sırasında araçla
> kaydedilmemiş, sonradan araştırmacıların hatırladıklarından yazılmıştır.
> Bu nedenle **nitel bir kayıttır**: görev süresi, başarı yüzdesi, hata sayısı
> gibi ölçülmesi gereken nicel değerler bu belgede yer almaz ve rapora
> aktarılamaz. Uygulama üzerinden kaydedilmiş oturum verisi bulunursa
> (`analysis/data/real/`), bu belge o veriyle değiştirilmez; onun yanında
> bağlam olarak durur.

## Etik çerçeve

| Alan | Değer |
|---|---|
| Etik kurul kararı | Kocaeli Üniversitesi Fen ve Mühendislik Bilimleri Etik Kurulu, `E-20189260-050.99-877088` |
| Karar tarihi | 27/11/2025, 2025/12 no.lu toplantı, karar 4 |
| Koşul | Kurum ve kişi ismi belirtilmez |
| Oturum dönemi | 2026 yılının ilk yarısı (kesin tarihler kayıt altına alınmamıştır) |

Katılımcılar yalnız takma adla anılır. Takma ad ile kişi eşleştirmesi bu
depoda **tutulmaz**.

## Katılımcı katmanları

Üç katman ayrı raporlanır; birleştirilmezler.

| Kod | Katman | n | Gerekçe |
|---|---|---|---|
| P01–P02 | Görme engelli katılımcı | 2 | Hedef kitle; protokolün dahil etme ölçütünü karşılar |
| P03–P06 | Gözü bağlı, uygulamayı tanımayan katılımcı | 4 | Görme engelli kullanıcının yerine geçmez: ekran okuyucu deneyimi ve mekânsal stratejileri yoktur |
| D01–D02 | Geliştirici yürüyüşü | 2 | Uygulamayı yazan kişiler; süre ve başarı ölçütü anlamlı değildir |

## Oturumların akışı

**Geliştirici yürüyüşleri (D01–D02) önce yapıldı.** Uygulamanın tüm akışı
baştan sona denendi ve bu oturumlarda ortaya çıkan hatalar kapatıldı. Bu,
sonraki oturumların daha olgun bir sürümle yapılmasını sağladı ve projenin
iteratif geliştirme kaydının bir parçasıdır.

**Ardından katılımcı oturumları yapıldı.** Her katılımcı uygulamanın bütün
aşamalarını denedi: hesap açma, tarama, sonucu dinleme, porsiyon seçimi,
onaylama, geçmişi görüntüleme ve diyetisyene rapor gönderme.

## Gözlemler

### Görev tamamlama

Araştırmacıların gözlemine göre katılımcılar denedikleri aşamaları
tamamlayabildi ve belirgin bir takılma yaşanmadı. Bu gözlem ölçülmüş bir
başarı oranı değildir; oturumlar araçla kaydedilmediği için görev başına
başarı/başarısızlık verisi bulunmamaktadır.

### Ekran okuyucu oturumları

Görme engelli katılımcıların ikisi de (P01, P02) uygulamayı **TalkBack
etkinken** fiziksel cihazda kullanmıştır. Oturumlarda
`docs/manual_screen_reader_test_plan.md` içindeki altı görevlik protokol
izlenmiş; kayıt ve giriş, tarama ve porsiyon düzeltme, geçmiş, diyetisyen
atama, rapor gönderimi ve ayarlar görevleri ile gürültü, ses yönlendirme ve
timeout alt testleri sırayla denenmiştir.

**Ölçüt bazında kayıt tutulmamıştır.** Plan her görev için ayrı bir geçme
ölçütü ve adım listesi tanımlar; oturumlar sırasında bu ölçütler tek tek
işaretlenmediği için görev bazında geçti/kaldı verisi, odak sırası, etiket
doğruluğu ve 200% metin davranışı gibi kalemlerde kayıt bulunmamaktadır.
Aşağıdaki bulgu dışında ayrıntılı gözlem kaydı yoktur.

#### Bulgu: ekran okuyucu ile uygulama sesinin çakışması

Oturumlarda uygulamanın kendi sesli geri bildirimi ile TalkBack'in aynı
içeriği üst üste okuduğu gözlenmiş ve bu sorun giderilmiştir. Çözüm kodda
uygulanmıştır: `lib/shared/services/accessibility_service.dart` ekran okuyucu
etkinken otomatik duyuruları bastırır, kullanıcı tarafından açıkça istenen
"sonucu dinle" türü eylemlere ve hata duyurularına izin vermeyi sürdürür.
Davranış `test/unit/screen_reader_coexistence_test.dart` içindeki dört testle
korunmaktadır.

Bu bulgu, oturumlardan doğan ve ürüne yansıyan somut değişikliktir; projenin
iteratif geliştirme kaydının parçasıdır. Sorunun hangi ekranlarda ve hangi
sıklıkta görüldüğü ölçüt bazında kaydedilmediği için niceliklendirilmemiştir.

### Katılımcı geri bildirimi

Katılımcılar uygulamayı kullanışlı bulduklarını ve erişilebilirlik
ayrıntılarının düşünülmüş olduğunu belirttiler. Birden fazla katılımcı
uygulamanın kısa sürede yaygın kullanıma açılmasını önerdi.

### Araştırmacıların çıkarımı

Oturumların en somut sonucu **platform dengesizliği** oldu: Android tarafı
oturumlarda beklendiği gibi çalışırken, iOS tarafının aynı olgunluğa
getirilmesi gerektiği görüldü. Bu gözlem projenin sonraki dönem önceliğini
belirlemiştir ve `docs/tubitak_sonuc_raporu.md` içindeki iOS sınırlılığıyla
tutarlıdır.

## Sınırlılıklar

Bu oturumlardan nicel sonuç üretilememesinin ve bulguların dikkatle
okunması gerekmesinin nedenleri:

1. **Ölçüm yapılmadı.** Oturumlar uygulamanın kullanılabilirlik kaydı
   üzerinden yürütülmediği için görev süresi, yardım düzeyi, hata sayısı ve
   iptal nedeni kayıt altına alınmadı. Ekran okuyucu protokolü izlenmiş olsa
   da ölçütler tek tek işaretlenmediği için görev bazında geçti/kaldı verisi
   de yoktur. Bu değerler sonradan üretilemez.

2. **Kayıt geriye dönüktür.** Gözlemler oturum anında değil sonradan
   yazılmıştır; hatırlama yanlılığı taşır.

3. **Takılma gözlenmemesi bir başarı ölçütü değildir.** Kullanılabilirlik
   yazınında sıfır sorun bulunan bir oturum, genellikle görevlerin fazla
   kolay olduğuna, yönlendirmenin fazla yakın olduğuna veya sorunların
   kaydedilmediğine işaret eder. Nielsen'in beş kullanıcı eşiği, beş
   katılımcının sorunların yaklaşık %85'ini **ortaya çıkarması** beklentisine
   dayanır; hiç sorun çıkmaması yöntemin sorunları görünür kılmadığını
   düşündürür.

4. **Sosyal istenirlik yanlılığı yüksektir.** Katılımcılar araştırmacıların
   arkadaş, oda arkadaşı ve komşu çevresinden gelmektedir. Bu ilişki,
   olumsuz geri bildirimi bastırma eğilimi yaratır; "piyasaya çıkarın"
   biçimindeki olumlu değerlendirmeler bu çerçevede okunmalıdır.

5. **Gözü bağlı katılımcılar hedef kitle değildir.** P03–P06 verisi görme
   engelli kullanıcı davranışının yerine geçmez.

6. **Katılımcı sayısı hedef kitlede ikidir.** P01–P02 ile çıkarımsal
   istatistik yapılmaz.

## Sonraki oturumlar için

Aynı katılımcı çevresiyle bile olsa, aşağıdaki değişiklikler bir sonraki
turda ölçülebilir veri üretir:

- Oturum uygulamanın kullanılabilirlik ekranı üzerinden yürütülür; süre,
  yardım düzeyi ve hata alanları otomatik dolar.
- Araştırmacı `docs/research/researcher_session_script.md` metnine bağlı
  kalır; görev sırasında ipucu verilmez.
- Yardım düzeyi her görevde açıkça işaretlenir (`none` / `prompt` /
  `partial` / `full`).
- Geri bildirim, araştırmacı odada değilken veya yazılı olarak alınır.
- Hedef kitlede en az beş katılımcıya çıkılır.
