"""Bütçe harcama kaydını denetler ve plan/gerçekleşen mutabakatını yazar.

Denetim bulguları BT-01…BT-04 kod dışıdır: harcama belgesi olmadan
kapatılamaz. Bu betik belgeyi üretmez; girilen kaydın onaylı bütçeyle
aritmetik olarak tutarlı, kalem eşleşmeli ve yer tutucusuz olmasını zorunlu
kılar. Boş kayıt geçerlidir ("harcama girilmedi"); tutarsız kayıt geçerli
değildir.

Kullanım:
    python scripts/qa/butce_mutabakat.py
    python scripts/qa/butce_mutabakat.py --kayit docs/butce/harcama_kaydi.ornek.json

Çıkış kodu 0: tutarlı. 1: en az bir kural ihlali.
Yalnız standart kütüphane kullanır.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
VARSAYILAN_BUTCE = REPO_ROOT / "docs" / "butce" / "onayli_butce.json"
VARSAYILAN_KAYIT = REPO_ROOT / "docs" / "butce" / "harcama_kaydi.json"

KURUS = Decimal("0.01")
ISO_TARIH = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")

# Gerçek kayıtta bulunmaması gereken doldurulmamış değerler.
YER_TUTUCULAR = (
    "ornek", "örnek", "xxx", "tbd", "todo", "doldurulacak",
    "placeholder", "degistirilecek", "değiştirilecek",
)

ZORUNLU_ALANLAR = (
    "id", "kalem_kodu", "aciklama", "saglayici", "belge_turu", "belge_no",
    "belge_tarihi", "adet", "birim_fiyat_tl", "kdv_orani",
    "tutar_kdv_haric_tl", "tutar_kdv_dahil_tl", "butceye_sayilan_tutar_tl",
    "odeme_turu", "odeme_tarihi", "belge_dosya_adi", "teslim_alindi",
)


class Bulgu(list):
    def ekle(self, kimlik: str, mesaj: str) -> None:
        self.append(f"{kimlik}: {mesaj}")


def _para(deger, alan: str, kimlik: str, bulgular: Bulgu) -> Decimal | None:
    try:
        return Decimal(str(deger)).quantize(KURUS)
    except (InvalidOperation, TypeError, ValueError):
        bulgular.ekle(kimlik, f"{alan} sayı değil: {deger!r}")
        return None


def _tarih(deger, alan: str, kimlik: str, bulgular: Bulgu) -> date | None:
    if not isinstance(deger, str) or not ISO_TARIH.match(deger):
        bulgular.ekle(kimlik, f"{alan} YYYY-AA-GG biçiminde değil: {deger!r}")
        return None
    try:
        return date.fromisoformat(deger)
    except ValueError:
        bulgular.ekle(kimlik, f"{alan} geçersiz tarih: {deger!r}")
        return None


def _yer_tutucu_mu(deger) -> bool:
    if not isinstance(deger, str):
        return False
    kucuk = deger.strip().lower()
    return any(iz in kucuk for iz in YER_TUTUCULAR)


def butce_dogrula(butce: dict, bulgular: Bulgu) -> dict[str, dict]:
    """Onaylı bütçenin kendi içinde tutarlı olduğunu kontrol eder."""
    kalemler: dict[str, dict] = {}
    toplam = Decimal("0.00")
    for kalem in butce["kalemler"]:
        kod = kalem["kod"]
        planlanan = _para(kalem["planlanan_tutar_tl"], "planlanan_tutar_tl", f"bütçe/{kod}", bulgular)
        if planlanan is None:
            continue
        toplam += planlanan
        alt_toplam = Decimal("0.00")
        alt_eksik = False
        for alt in kalem.get("alt_kalemler", []):
            if alt.get("planlanan_tutar_tl") is None:
                alt_eksik = True
                continue
            deger = _para(alt["planlanan_tutar_tl"], "alt kalem tutarı", f"bütçe/{kod}", bulgular)
            if deger is not None:
                alt_toplam += deger
        if kalem.get("alt_kalemler") and not alt_eksik and alt_toplam != planlanan:
            bulgular.ekle(
                f"bütçe/{kod}",
                f"alt kalem toplamı {alt_toplam} TL, kalem tutarı {planlanan} TL ile eşit değil",
            )
        kalemler[kod] = {
            "ad": kalem["ad"],
            "planlanan": planlanan,
            "alt_adlar": [alt["ad"] for alt in kalem.get("alt_kalemler", [])],
            "alt_eksik": alt_eksik,
        }
    beyan = _para(butce["toplam_tl"], "toplam_tl", "bütçe", bulgular)
    if beyan is not None and beyan != toplam:
        bulgular.ekle("bütçe", f"kalem toplamı {toplam} TL, beyan edilen toplam {beyan} TL")
    return kalemler


def harcama_dogrula(
    harcama: dict, kalemler: dict[str, dict], kayit: dict, donem: dict, bulgular: Bulgu
) -> tuple[str, Decimal] | None:
    kimlik = harcama.get("id") or "<id yok>"
    gercek = kayit["kayit_turu"] == "GERCEK"

    eksik = [alan for alan in ZORUNLU_ALANLAR if alan not in harcama]
    if eksik:
        bulgular.ekle(kimlik, f"zorunlu alan eksik: {', '.join(eksik)}")
        return None

    if gercek:
        for alan, deger in harcama.items():
            if _yer_tutucu_mu(deger):
                bulgular.ekle(kimlik, f"{alan} hâlâ yer tutucu değer taşıyor: {deger!r}")

    kod = harcama["kalem_kodu"]
    kalem = kalemler.get(kod)
    if kalem is None:
        bulgular.ekle(kimlik, f"kalem_kodu onaylı bütçede yok: {kod!r}")
        return None
    if kalem["planlanan"] == 0:
        bulgular.ekle(kimlik, f"{kalem['ad']} kaleminde onaylı bütçe yok; harcama işlenemez")

    # Alt kalemi olan bir kalemde harcama hangi donanıma ait olduğunu söylemeli.
    # BT-02 çelişkisi tam olarak bu ayrımın yapılmamış olmasıydı.
    if kalem["alt_adlar"]:
        alt = harcama.get("alt_kalem")
        if alt not in kalem["alt_adlar"]:
            bulgular.ekle(
                kimlik,
                f"alt_kalem {alt!r} onaylı alt kalemlerden biri değil: {kalem['alt_adlar']}",
            )

    adet = _para(harcama["adet"], "adet", kimlik, bulgular)
    birim = _para(harcama["birim_fiyat_tl"], "birim_fiyat_tl", kimlik, bulgular)
    haric = _para(harcama["tutar_kdv_haric_tl"], "tutar_kdv_haric_tl", kimlik, bulgular)
    dahil = _para(harcama["tutar_kdv_dahil_tl"], "tutar_kdv_dahil_tl", kimlik, bulgular)
    sayilan = _para(harcama["butceye_sayilan_tutar_tl"], "butceye_sayilan_tutar_tl", kimlik, bulgular)
    kdv = _para(harcama["kdv_orani"], "kdv_orani", kimlik, bulgular)
    if None in (adet, birim, haric, dahil, sayilan, kdv):
        return None

    if adet <= 0 or birim <= 0:
        bulgular.ekle(kimlik, "adet ve birim fiyat sıfırdan büyük olmalı")
    if (adet * birim).quantize(KURUS) != haric:
        bulgular.ekle(kimlik, f"adet × birim fiyat {(adet * birim).quantize(KURUS)} TL, KDV hariç tutar {haric} TL")
    if (haric * (Decimal("1") + kdv)).quantize(KURUS) != dahil:
        bulgular.ekle(kimlik, f"KDV hesabı tutmuyor: {haric} × (1+{kdv}) ≠ {dahil}")

    kural = kayit.get("butceye_sayilan_tutar_kurali")
    beklenen = {"kdv_dahil": dahil, "kdv_haric": haric}.get(kural)
    if beklenen is None:
        bulgular.ekle("kayıt", f"butceye_sayilan_tutar_kurali 'kdv_dahil' veya 'kdv_haric' olmalı: {kural!r}")
    elif sayilan != beklenen:
        bulgular.ekle(kimlik, f"butceye_sayilan_tutar_tl {sayilan} TL, {kural} kuralına göre {beklenen} TL olmalı")

    belge_tarihi = _tarih(harcama["belge_tarihi"], "belge_tarihi", kimlik, bulgular)
    odeme_tarihi = _tarih(harcama["odeme_tarihi"], "odeme_tarihi", kimlik, bulgular)
    if belge_tarihi and odeme_tarihi and odeme_tarihi < belge_tarihi:
        bulgular.ekle(kimlik, "ödeme tarihi belge tarihinden önce olamaz")

    baslangic = donem.get("baslangic")
    bitis = donem.get("bitis")
    if belge_tarihi and baslangic and bitis:
        alt_sinir = _tarih(baslangic, "proje_donemi.baslangic", "bütçe", bulgular)
        ust_sinir = _tarih(bitis, "proje_donemi.bitis", "bütçe", bulgular)
        if alt_sinir and ust_sinir and not (alt_sinir <= belge_tarihi <= ust_sinir):
            bulgular.ekle(kimlik, f"belge tarihi proje dönemi dışında ({baslangic} – {bitis})")

    ozet = harcama.get("belge_sha256")
    if ozet is not None and not SHA256.match(str(ozet)):
        bulgular.ekle(kimlik, "belge_sha256 64 haneli küçük harf hex değil")
    elif gercek and ozet is not None and set(str(ozet)) == {"0"}:
        bulgular.ekle(kimlik, "belge_sha256 yalnız sıfır; gerçek belgenin özeti hesaplanmamış")
    if gercek and harcama.get("teslim_alindi") is not True:
        bulgular.ekle(kimlik, "teslim alınmamış harcama mali rapora giremez")

    return kod, sayilan


def calistir(butce_yolu: Path, kayit_yolu: Path) -> int:
    butce = json.loads(butce_yolu.read_text(encoding="utf-8"))
    kayit = json.loads(kayit_yolu.read_text(encoding="utf-8"))
    bulgular = Bulgu()

    if kayit.get("kayit_turu") not in {"GERCEK", "ORNEK"}:
        bulgular.ekle("kayıt", "kayit_turu 'GERCEK' veya 'ORNEK' olmalı")

    kalemler = butce_dogrula(butce, bulgular)
    donem = butce.get("proje_donemi", {})

    gerceklesen = {kod: Decimal("0.00") for kod in kalemler}
    kimlikler: set[str] = set()
    belgeler: set[tuple] = set()

    for harcama in kayit.get("harcamalar", []):
        kimlik = harcama.get("id")
        if kimlik in kimlikler:
            bulgular.ekle(str(kimlik), "id tekrar ediyor")
        kimlikler.add(kimlik)
        anahtar = (harcama.get("belge_turu"), harcama.get("belge_no"))
        if anahtar in belgeler:
            bulgular.ekle(str(kimlik), f"aynı belge iki kez kaydedilmiş: {anahtar}")
        belgeler.add(anahtar)

        sonuc = harcama_dogrula(harcama, kalemler, kayit, donem, bulgular)
        if sonuc:
            kod, tutar = sonuc
            gerceklesen[kod] = gerceklesen.get(kod, Decimal("0.00")) + tutar

    for kod, kalem in kalemler.items():
        if gerceklesen.get(kod, Decimal("0.00")) > kalem["planlanan"]:
            bulgular.ekle(
                f"kalem/{kod}",
                f"gerçekleşen {gerceklesen[kod]} TL, onaylı {kalem['planlanan']} TL tutarını aşıyor",
            )

    _tablo_yaz(kayit, kalemler, gerceklesen, donem)

    if bulgular:
        print("\nBULGULAR")
        for satir in bulgular:
            print(f"  - {satir}")
        print(f"\nSONUÇ: {len(bulgular)} kural ihlali. Kayıt mali rapora hazır değil.")
        return 1

    if kayit["kayit_turu"] == "ORNEK":
        print("\nSONUÇ: Örnek kayıt tutarlı. Bu dosya mali beyanda kullanılamaz.")
    elif not kayit.get("harcamalar"):
        print("\nSONUÇ: Harcama girilmedi. Kayıt boş ve tutarlı; BT-01…BT-04 hâlâ açık.")
    else:
        print("\nSONUÇ: Kayıt tutarlı.")
    return 0


def _tablo_yaz(kayit: dict, kalemler: dict, gerceklesen: dict, donem: dict) -> None:
    print(f"Kayıt türü : {kayit.get('kayit_turu')}")
    print(f"Durum      : {kayit.get('durum')}")
    print(f"Tutar kuralı: {kayit.get('butceye_sayilan_tutar_kurali')}")
    if not (donem.get("baslangic") and donem.get("bitis")):
        print("UYARI      : proje_donemi doldurulmadığı için tarih kapısı çalışmadı.")
    print()
    print(f"{'Kalem':<28}{'Planlanan':>12}{'Gerçekleşen':>14}{'Kalan':>12}")
    print("-" * 66)
    toplam_plan = Decimal("0.00")
    toplam_ger = Decimal("0.00")
    for kod, kalem in kalemler.items():
        ger = gerceklesen.get(kod, Decimal("0.00"))
        toplam_plan += kalem["planlanan"]
        toplam_ger += ger
        print(f"{kalem['ad']:<28}{kalem['planlanan']:>12}{ger:>14}{kalem['planlanan'] - ger:>12}")
    print("-" * 66)
    print(f"{'TOPLAM':<28}{toplam_plan:>12}{toplam_ger:>14}{toplam_plan - toplam_ger:>12}")


def main() -> int:
    ayristirici = argparse.ArgumentParser(description="Bütçe harcama kaydı mutabakatı")
    ayristirici.add_argument("--butce", type=Path, default=VARSAYILAN_BUTCE)
    ayristirici.add_argument("--kayit", type=Path, default=VARSAYILAN_KAYIT)
    argumanlar = ayristirici.parse_args()
    return calistir(argumanlar.butce, argumanlar.kayit)


if __name__ == "__main__":
    raise SystemExit(main())
