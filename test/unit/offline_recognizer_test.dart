import 'dart:convert';
import 'dart:typed_data';

import 'package:flutter/services.dart' show rootBundle;
import 'package:flutter_test/flutter_test.dart';
import 'package:nutrisense/features/food_scan/services/offline_recognizer.dart';
import 'package:nutrisense/shared/models/food_analysis_model.dart';

/// Cihaz üstü tanıyıcının sözleşmesi.
///
/// Modelin kendisi TFLite çalışma zamanı gerektirdiği için burada
/// çalıştırılmaz; bu testler modelin yokluğunda ve hatalı girdide sistemin
/// yanlış sonuç üretmeyip manuel girişe yönlendirdiğini doğrular. Modelin
/// başarımı `ml/MODEL_CARD.md` içindeki mühürlü test raporundadır.
void main() {
  test('paketlenen manifestte her etiketin katalog anahtarı var', () async {
    // Katalog anahtarı olmayan etiket tanınsa bile kalori getiremez; kullanıcı
    // "tanındı" duyurusunu duyar ama kayıt "besin değeri bulunamadı" ile düşer.
    // Anahtarın karşılığının katalogda gerçekten bulunduğu ayrıca
    // `ml/tests/test_catalog_contract.py` ile doğrulanır.
    TestWidgetsFlutterBinding.ensureInitialized();
    final manifest = jsonDecode(
      await rootBundle.loadString('assets/models/model_manifest.json'),
    ) as Map<String, dynamic>;
    final labels = (await rootBundle.loadString('assets/models/labels.txt'))
        .split('\n')
        .map((line) => line.trim())
        .where((line) => line.isNotEmpty)
        .toList();
    final catalogKeys = manifest['catalog_keys'] as Map<String, dynamic>;

    expect(labels, isNotEmpty);
    expect(
      labels.where((label) => !catalogKeys.containsKey(label)),
      isEmpty,
      reason: 'Katalog anahtarı olmayan etiket kalori getiremez',
    );
    expect(catalogKeys.values.where((key) => (key as String).isEmpty), isEmpty);
  });

  test('başarılı sonuç katalog anahtarını taşır', () {
    const outcome = OfflineRecognitionOutcome(
      OfflineRecognitionStatus.success,
      'sütlaç olarak tanındı.',
      foodNameTr: 'sütlaç',
      catalogKey: 'rice_pudding',
      confidence: 0.98,
    );

    expect(outcome.foodNameTr, 'sütlaç');
    expect(outcome.catalogKey, 'rice_pudding');
  });

  test('model yüklü değilken sonuç uydurulmaz', () async {
    const recognizer = UnavailableOfflineFoodRecognizer();

    final outcome = await recognizer.recognize(Uint8List(0));

    expect(recognizer.isAvailable, isFalse);
    expect(outcome.status, OfflineRecognitionStatus.unavailable);
    expect(outcome.foodNameTr, isNull);
    expect(outcome.confidence, isNull);
    expect(outcome.message, contains('Manuel giriş'));
  });

  test('başarısız sonuç yemek adı ve güven taşımaz', () {
    const outcome = OfflineRecognitionOutcome(
      OfflineRecognitionStatus.rejected,
      'Yiyecek güvenilir biçimde tanınamadı.',
    );

    expect(outcome.foodNameTr, isNull);
    expect(outcome.confidence, isNull);
  });

  test('başarılı sonuç adı ve güveni birlikte taşır', () {
    const outcome = OfflineRecognitionOutcome(
      OfflineRecognitionStatus.success,
      'baklava olarak tanındı.',
      foodNameTr: 'baklava',
      confidence: 0.98,
    );

    expect(outcome.status, OfflineRecognitionStatus.success);
    expect(outcome.foodNameTr, 'baklava');
    expect(outcome.confidence, greaterThan(0.9));
  });

  test('düşük kesinlikli öneri adı ve güveni kullanıcı onayına taşır', () {
    const outcome = OfflineRecognitionOutcome(
      OfflineRecognitionStatus.suggestion,
      'Olası tahmin baklava.',
      foodNameTr: 'baklava',
      confidence: 0.61,
    );

    expect(outcome.status, OfflineRecognitionStatus.suggestion);
    expect(outcome.foodNameTr, 'baklava');
    expect(outcome.confidence, 0.61);
  });

  test('düşük kesinlikli öneri ilk üç seçeneği kullanıcıya taşır', () {
    const candidates = [
      FoodCandidate(foodName: 'muz', foodNameTr: 'Muz', confidence: 0.61),
      FoodCandidate(foodName: 'misir', foodNameTr: 'Mısır', confidence: 0.21),
      FoodCandidate(foodName: 'kavun', foodNameTr: 'Kavun', confidence: 0.10),
    ];
    const outcome = OfflineRecognitionOutcome(
      OfflineRecognitionStatus.suggestion,
      'Olası tahmin Muz.',
      foodNameTr: 'Muz',
      confidence: 0.61,
      candidates: candidates,
    );

    expect(outcome.candidates, hasLength(3));
    expect(outcome.candidates.first.foodName, 'muz');
    expect(outcome.candidates[1].foodNameTr, 'Mısır');
  });

  test('asset bulunamazsa tanıyıcı hata fırlatmaz, kapalı kalır', () async {
    TestWidgetsFlutterBinding.ensureInitialized();
    final recognizer = TfliteFoodRecognizer(
      modelAsset: 'assets/models/olmayan.tflite',
      labelsAsset: 'assets/models/olmayan.txt',
      manifestAsset: 'assets/models/olmayan.json',
    );

    final outcome = await recognizer.recognize(Uint8List.fromList([1, 2, 3]));

    expect(recognizer.isAvailable, isFalse);
    expect(outcome.status, OfflineRecognitionStatus.unavailable);
    expect(outcome.foodNameTr, isNull);
    await recognizer.dispose();
  });
}
