"""Tanınan her sınıfın kalori kaynağı olmalı.

Model bir sınıfı tanıyıp katalogda karşılığı bulunmazsa kullanıcı önce
"tanındı" duyurusunu duyar, sonra kayıt "besin değeri bulunamadı" ile
düşer. Bu, tarama akışını görme engelli kullanıcı için sessizce kırar.

Kayıt doğrulama kuralları `NutritionixService._validated_local_record`
ile aynıdır; bu test backend bağımlılığı kurmadan çalışsın diye stdlib
ile yeniden yazılmıştır. Kural değişirse iki taraf birlikte güncellenir.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST = REPO_ROOT / "assets" / "models" / "model_manifest.json"
LABELS = REPO_ROOT / "assets" / "models" / "labels.txt"
CATALOG = REPO_ROOT / "backend" / "app" / "data" / "verified_nutrition.json"

PLACEHOLDERS = {"local", "mock data", "unknown", "placeholder"}


@pytest.fixture(scope="module")
def manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def labels() -> list[str]:
    lines = LABELS.read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in lines if line.strip()]


@pytest.fixture(scope="module")
def catalog() -> dict:
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def test_label_file_and_manifest_agree(manifest: dict, labels: list[str]) -> None:
    assert labels == list(manifest["labels_tr"]), "labels.txt ve labels_tr sırası aynı olmalı"
    assert labels == list(manifest["catalog_keys"]), "her etiketin katalog anahtarı olmalı"


def test_notes_state_the_real_class_count(manifest: dict, labels: list[str]) -> None:
    # Kapsam büyüdüğünde kart metninde eski sınıf sayısının kalmasını engeller.
    assert str(len(labels)) in manifest["notes"]


def test_every_label_resolves_to_a_validated_catalog_record(
    manifest: dict, labels: list[str], catalog: dict
) -> None:
    inventory = catalog["_meta"]["source_inventory"]
    unresolved: list[str] = []
    for label in labels:
        key = manifest["catalog_keys"][label]
        record = catalog.get(key)
        if record is None or key == "_meta":
            unresolved.append(f"{label} -> {key}: katalogda yok")
            continue
        problem = _validation_problem(record, inventory)
        if problem:
            unresolved.append(f"{label} -> {key}: {problem}")
    assert not unresolved, "Kalori kaynağı olmayan sınıf(lar):\n" + "\n".join(unresolved)


def test_catalog_keys_survive_backend_slug_normalisation(
    manifest: dict, labels: list[str]
) -> None:
    """Anahtar, backend'in `food_lookup_key` kuralına göre kendine eşit olmalı.

    Backend aramayı slug üzerinden yapar; slug'ı kendinden farklı bir anahtar
    katalogda bulunsa bile sorguda kaçırılır.
    """
    for label in labels:
        key = manifest["catalog_keys"][label]
        assert key == _slug(key), f"{label} -> {key}: slug kararsız"


def _slug(value: str) -> str:
    # `app.domain.nutrition._slug` ile aynı sonucu vermelidir.
    lowered = value.replace("İ", "i").replace("I", "ı").lower()
    for source, target in (
        ("ı", "i"), ("ş", "s"), ("ğ", "g"), ("ü", "u"), ("ö", "o"), ("ç", "c")
    ):
        lowered = lowered.replace(source, target)
    return "".join(
        char if char.isalnum() else "_" for char in lowered
    ).strip("_")


def _validation_problem(record: dict, inventory: dict) -> str | None:
    if record.get("evidence_status") not in {"VERIFIED", "ESTIMATED"}:
        return "evidence_status kabul edilmiyor"
    source_id = record.get("source_item_id")
    source = inventory.get(source_id)
    if source is None:
        return "source_inventory kaydı yok"
    for field in ("license", "attribution", "source_url", "source_item_name"):
        value = source.get(field)
        if not isinstance(value, str) or not value.strip():
            return f"{field} boş"
        if value.strip().lower() in PLACEHOLDERS:
            return f"{field} yer tutucu"
    url = urlsplit(source["source_url"])
    if url.scheme != "https" or not url.hostname:
        return "source_url https değil"
    retrieved = datetime.fromisoformat(source["retrieved_at"].replace("Z", "+00:00"))
    if retrieved.tzinfo is None or retrieved > datetime.now(timezone.utc):
        return "retrieved_at geçersiz"
    for row in record.get("portion_units", []):
        if row.get("source_item_id") != source_id or not row.get("source_measure"):
            return "birim dönüşümünün kendi kanıtı yok"
    return None
