# Hasta Takibi İçin Kritik Sıcaklık ve Nem Uyarı Sistemi

Bu proje, hastane veya ev ortamında kritik sıcaklık/nem takibi yapmak amacıyla geliştirilmiş **Arduino ve Python** tabanlı bir IoT prototipidir. Sensör verilerini anlık olarak izler, kritik eşik (37.5°C) aşıldığında görsel uyarı verir ve verileri Excel (CSV) formatında kaydeder.

##  Özellikler
* **Gerçek Zamanlı İzleme:** Arduino'dan gelen veriler Python arayüzünde (Tkinter) saniyelik olarak görüntülenir.
* **Otomatik Kayıt:** Veriler `sicaklik_nem_kayitlari.csv` dosyasına tarih ve saat etiketiyle kaydedilir.
* **Görsel Alarm:** Sıcaklık 37.5°C'yi geçtiğinde arayüz rengi değişerek "KRİTİK" uyarısı verir.
* **Donanım:** Arduino Uno, DHT11 Sensör.
* **Yazılım:** Python (Pandas, Tkinter, PySerial).

##  Kurulum
1. Arduino kodunu kartınıza yükleyin.
2. Python kütüphanelerini yükleyin:
   `pip install pyserial tk`
3. `main.py` dosyasını çalıştırın.
