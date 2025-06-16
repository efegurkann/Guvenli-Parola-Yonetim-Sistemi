<div align="center">
  <img src="https://img.shields.io/github/languages/count/efegurkan/projem?style=flat-square&color=blueviolet" alt="Language Count">
  <img src="https://img.shields.io/github/languages/top/efegurkan/projem?style=flat-square&color=1e90ff" alt="Top Language">
  <img src="https://img.shields.io/github/last-commit/efegurkan/projem?style=flat-square&color=ff69b4" alt="Last Commit">
  <img src="https://img.shields.io/github/license/efegurkan/projem?style=flat-square&color=yellow" alt="License">
  <img src="https://img.shields.io/badge/Status-Active-green?style=flat-square" alt="Status">
  <img src="https://img.shields.io/badge/Contributions-Welcome-brightgreen?style=flat-square" alt="Contributions">
</div>

# Güvenli Parola Yönetim Sistemi

Bu proje, modern parola güvenliği prensiplerini uygulayan kapsamlı bir parola yönetim sistemi sunar.

## Features / *Özellikler*

### 1. Parola Güçlülük Analizi
- Makine öğrenimi tabanlı güçlülük tahmini
- Entropi hesaplama ve karakter çeşitliliği analizi
- Yaygın parola kalıplarını tespit etme
- Detaylı güçlülük raporu ve öneriler

### 2. Güvenli Parola Üretimi
- Rastgele güçlü parolalar
- Anımsanabilir parola öbekleri
- Telaffuz edilebilir parolalar
- Özelleştirilebilir parola kuralları

### 3. Parola Yönetimi
- Şifrelenmiş parola depolama
- Parola geçmişi ve versiyonlama
- Otomatik parola doldurma
- Parola arama ve filtreleme

### 4. Güvenlik İzleme
- Veri ihlali kontrolü
- Sürekli güvenlik izleme
- Güvenlik raporları
- Otomatik güvenlik önerileri

## Team / *Ekip*

- **Efe Gürkan (2320191037)** - Proje Sahibi
  - Parola güvenliği araştırması
  - Sistem tasarımı ve geliştirme
  - Dokümantasyon

## Research / *Araştırmalar*

Proje, aşağıdaki temel araştırma alanlarına dayanmaktadır:

### 1. Modern Kimlik Doğrulama Teknolojileri
- Passkeys ve FIDO2/WebAuthn entegrasyonu
- Çok faktörlü kimlik doğrulama (MFA)
- Biyometrik entegrasyon

### 2. Güvenlik Altyapısı
- Gelişmiş parola yöneticileri
- Risk tabanlı uyarlanabilir kimlik doğrulama
- Adversarial makine öğrenimi

### 3. Kullanıcı Davranışı
- Davranış biyometrisi
- Güvenlik nudging
- Farkındalık eğitimi

### 4. Düzenleyici Uyumluluk
- NIST standartları
- GDPR uyumluluğu
- Endüstri en iyi uygulamaları

## Installation / *Kurulum*

1. **Clone the Repository / *Depoyu Klonlayın***:  
   ```bash
   git clone https://github.com/efegurkan/projem.git
   cd projem
   ```

2. **Set Up Virtual Environment / *Sanal Ortam Kurulumu*** (Recommended):  
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies / *Bağımlılıkları Yükleyin***:  
   ```bash
   pip install -r src/requirements.txt
   ```

## Usage / *Kullanım*

### Temel Kullanım

```python
from src.password_manager import PasswordManager
from src.security_monitor import SecurityMonitor

# Parola yöneticisini başlat
manager = PasswordManager("ana_parola")

# Yeni parola ekle
manager.add_password("gmail", "kullanici@gmail.com", "güçlü_parola123")

# Güvenlik izleyiciyi başlat
monitor = SecurityMonitor(manager)

# Güvenlik raporu al
report = monitor.generate_security_report()
print(f"Güvenlik Puanı: {report['security_score']}/100")

# Sürekli izleme başlat
monitor.monitor_continuously()
```

### Güvenlik Özellikleri

- Tüm parolalar şifrelenerek saklanır
- Ana parola asla düz metin olarak saklanmaz
- Parola ihlalleri düzenli olarak kontrol edilir
- Zayıf ve yeniden kullanılan parolalar tespit edilir
- Güvenlik önerileri otomatik olarak oluşturulur

## Contributing / *Katkıda Bulunma*

We welcome contributions! To help:  
1. Fork the repository.  
2. Clone your fork (`git clone git@github.com:efegurkan/projem.git`).  
3. Create a branch (`git checkout -b feature/your-feature`).  
4. Commit changes with clear messages.  
5. Push to your fork (`git push origin feature/your-feature`).  
6. Open a Pull Request.  

Follow our coding standards (see [CONTRIBUTING.md](CONTRIBUTING.md)).  

*Topluluk katkılarını memnuniyetle karşılıyoruz! Katkıda bulunmak için yukarıdaki adımları izleyin ve kodlama standartlarımıza uyun.*

## License / *Lisans*

Licensed under the [MIT License](LICENSE.md).  
*MIT Lisansı altında lisanslanmıştır.*

## Contact / *İletişim*

Project Maintainer: Efe Gürkan -   
Found a bug? Open an issue.  

*Proje Sorumlusu: Efe Gürkan - Hata bulursanız bir sorun bildirin.*
