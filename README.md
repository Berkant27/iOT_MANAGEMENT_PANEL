# IoT Cihaz Yönetim Paneli

Bu proje, IoT cihazlarını yönetmek için bir web uygulamasıdır. Kullanıcılar cihaz ekleyebilir, durumlarını kontrol edebilir ve cihaz verilerini bir tabloyla görüntüleyebilir.

## Özellikler
- Cihaz ekleme, silme ve durum güncelleme (Açık/Kapalı).
- Sıcaklık verilerini tablo formatında gösterme (manuel veri girişiyle veya MQTT ile).
- Mobil uyumlu arayüz (Bootstrap).
- SQLite ile veri saklama.
- **MQTT ile veri alma ve kontrol**: Test edilmemiştir, manuel kurulum gerektirir.

## Kurulum
1. Depoyu klonlayın veya dosyaları indirin:
   ```bash
   git clone https://github.com/Berkant27/iOT_MANAGEMENT_PANEL
   cd iot_management_panel
