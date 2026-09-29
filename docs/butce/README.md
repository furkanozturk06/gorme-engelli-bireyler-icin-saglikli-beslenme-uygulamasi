# Bütçe ve harcama kaydı

Bu klasör, başvurudaki 9.000 TL'lik bütçenin (`BT-01`…`BT-04`) gerçekleşme
kaydını tutar. Denetim bu satırları "Kanıtsız"/"Çelişkili" olarak işaretlemişti;
satırlar ancak gerçek belgeyle kapanır. Buradaki dosyalar belgeyi üretmez,
girilen kaydın **tutarlı ve yer tutucusuz** olmasını zorunlu kılar.

| Dosya | Ne işe yarar |
|---|---|
| `onayli_butce.json` | Başvurudaki (ve varsa sözleşmedeki) onaylı bütçe. Referans; harcama girerken değiştirilmez. |
| `harcama_kaydi.json` | **Doldurulacak gerçek kayıt.** Şu an boş. |
| `harcama_kaydi.ornek.json` | Çalışan örnek. Alanların nasıl doldurulduğunu ve mutabakatın nasıl kapandığını gösterir. Mali beyanda kullanılamaz. |
| `scripts/qa/butce_mutabakat.py` | Denetim ve plan/gerçekleşen tablosu. |

## Kullanım

Örneğin nasıl göründüğünü görmek için:

```bash
python scripts/qa/butce_mutabakat.py --kayit docs/butce/harcama_kaydi.ornek.json
```

Kendi kaydınızı denetlemek için:

```bash
python scripts/qa/butce_mutabakat.py
```

Betik yalnız standart kütüphane kullanır; ek kurulum gerektirmez. Çıkış kodu
0 ise kayıt tutarlıdır, 1 ise en az bir kural ihlali vardır ve ihlaller
listelenir. Boş kayıt geçerlidir: "harcama girilmedi" der ve geçer.

## Doldurma sırası

1. **Önce `onayli_butce.json`.** İki alanı siz bilirsiniz:
   - `proje_donemi.baslangic` / `bitis` — destek başlangıcından itibaren 10 ay.
     Doldurulmadan tarih kapısı çalışmaz; dönem dışı fatura yakalanamaz.
   - Sarf kaleminin `alt_kalemler` içindeki `birim_fiyat_tl` ve
     `planlanan_tutar_tl` değerleri. Başvuru formu 16 GB RAM ile 1 TB SSD'yi
     tek 4.500 TL satırında birlikte anıyor ve birim dağılımını vermiyor —
     denetimdeki `BT-02` çelişkisi tam olarak budur. Onaylı bütçedeki dağılımı
     yazın; alt kalem toplamı 4.500 TL'ye eşit olmak zorundadır.
2. **Sonra her harcama için `harcama_kaydi.json` içine bir satır.** Alanlar
   örnek dosyadaki gibidir. `durum` alanını ilk satırı eklerken
   `HARCAMA_GIRILDI` yapın ve `guncelleme_tarihi` yazın.
3. **Her satırı çalıştırıp doğrulayın.** Betik hatayı satır kimliğiyle söyler.

## Kurallar (betiğin zorunlu kıldığı)

- Zorunlu alanların hepsi bulunmalı; gerçek kayıtta "örnek", "XXX",
  "doldurulacak" gibi izler kalamaz.
- `kalem_kodu` onaylı bütçedeki bir kaleme ait olmalı; onaylı bütçesi sıfır
  olan kaleme harcama işlenemez.
- Alt kalemi olan kalemde (sarf) harcama **hangi donanıma ait olduğunu**
  söylemek zorundadır.
- `adet × birim_fiyat = KDV hariç tutar` ve `KDV hariç × (1 + oran) = KDV dahil`.
- `butceye_sayilan_tutar_tl`, kaydın başındaki `butceye_sayilan_tutar_kurali`
  ile (KDV dahil ya da hariç) uyuşmalı. **Hangisinin geçerli olduğunu
  üniversitenizin mali işler birimine doğrulatın**; varsayılan `kdv_dahil`
  seçilmiştir ve bir mevzuat yorumu değildir.
- Ödeme tarihi belge tarihinden önce olamaz; belge tarihi proje dönemi içinde
  olmalı.
- Aynı belge iki kez, aynı `id` iki kez kaydedilemez.
- Kalem bazında ve toplamda onaylı bütçe aşılamaz.
- Gerçek kayıtta teslim alınmamış harcama mali rapora giremez.
- Hizmet alımında (`BT-03`) `teslim_kanidi`, teslim edilen artefaktı adıyla
  yazmalıdır: hangi `.aab`, hangi `.ipa`, hangi SHA-256. "Geliştirme yapıldı"
  ifadesi teslim kanıtı değildir.

## Belgeler nereye konur

Taranmış fatura, dekont ve zimmet tutanakları **Git'e eklenmez** — kişisel ve
mali veri taşırlar ve deponun `.gitignore` ilkesi bunu zaten yasaklar. Bunları
kurumsal ortak alanda veya proje mali klasöründe tutun; `belge_arsivi.konum`
alanına o dizinin yolunu yazın. Kayıtta yalnız dosya adı ve dosyanın SHA-256
özeti bulunur:

```bash
python -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" fatura.pdf
```

Bu özet, mali raporda gösterilen belgeyle arşivdeki belgenin aynı dosya
olduğunu sonradan kanıtlar.

## Neyi kapatır, neyi kapatmaz

Kayıt dolduğunda `BT-01`, `BT-02` (birim dağılımı netleşerek), `BT-03` (teslim
artefaktı adlandırılarak) ve `BT-04` (plan/gerçekleşen mutabakatıyla)
kapanabilir. Kapatan şey bu klasör değil, girdiğiniz belgedir; betik yalnız
belgenin tutarsız girilmesini engeller.

TYBS ekranındaki rakamlar bu dosyalarla çelişirse **TYBS esastır** (başvuru
formunun kendi notu). Çelişki görürseniz `onayli_butce.json` güncellenmeli ve
gerekçe not düşülmelidir.
