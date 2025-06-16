import requests
import hashlib
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from password_manager import PasswordManager

class SecurityMonitor:
    def __init__(self, password_manager: PasswordManager):
        """
        Güvenlik izleyiciyi başlatır.
        
        Args:
            password_manager (PasswordManager): Parola yöneticisi
        """
        self.password_manager = password_manager
        self.breach_cache = {}
        self.last_check = None
        self.check_interval = timedelta(hours=24)  # 24 saatte bir kontrol

    def check_password_breach(self, password: str) -> bool:
        """
        Parolanın veri ihlallerinde açığa çıkıp çıkmadığını kontrol eder.
        
        Args:
            password (str): Kontrol edilecek parola
            
        Returns:
            bool: Parola ihlal edilmiş mi
        """
        # SHA-1 hash'ini hesapla
        password_hash = hashlib.sha1(password.encode()).hexdigest().upper()
        prefix = password_hash[:5]
        suffix = password_hash[5:]

        # Önbellekte kontrol et
        if prefix in self.breach_cache:
            return suffix in self.breach_cache[prefix]

        try:
            # Have I Been Pwned API'sini kullan
            response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
            if response.status_code == 200:
                hashes = response.text.splitlines()
                self.breach_cache[prefix] = [h.split(':')[0] for h in hashes]
                return suffix in self.breach_cache[prefix]
        except Exception as e:
            print(f"İhlal kontrolü hatası: {e}")

        return False

    def check_all_passwords(self) -> Dict:
        """
        Tüm parolaları ihlal kontrolünden geçirir.
        
        Returns:
            Dict: İhlal raporu
        """
        if (self.last_check and 
            datetime.now() - self.last_check < self.check_interval):
            return {"error": "Son kontrol çok yakın zamanda yapıldı"}

        report = {
            "checked_at": str(datetime.now()),
            "total_checked": 0,
            "breached_passwords": [],
            "weak_passwords": [],
            "reused_passwords": []
        }

        all_passwords = set()
        for service, entries in self.password_manager.passwords.items():
            for entry in entries:
                report["total_checked"] += 1
                password = entry["password"]

                # İhlal kontrolü
                if self.check_password_breach(password):
                    report["breached_passwords"].append({
                        "service": service,
                        "username": entry["username"],
                        "breached_at": str(datetime.now())
                    })

                # Zayıf parola kontrolü
                strength = self.password_manager.analyzer.analyze_password(password)
                if strength["strength_score"] < 60:
                    report["weak_passwords"].append({
                        "service": service,
                        "username": entry["username"],
                        "strength_score": strength["strength_score"]
                    })

                # Yeniden kullanım kontrolü
                if password in all_passwords:
                    report["reused_passwords"].append({
                        "service": service,
                        "username": entry["username"]
                    })
                all_passwords.add(password)

        self.last_check = datetime.now()
        return report

    def generate_security_report(self) -> Dict:
        """
        Kapsamlı bir güvenlik raporu oluşturur.
        
        Returns:
            Dict: Güvenlik raporu
        """
        # Parola güçlülük raporu
        strength_report = self.password_manager.get_password_strength_report()
        
        # İhlal raporu
        breach_report = self.check_all_passwords()
        
        # Genel güvenlik durumu
        security_score = 100
        if strength_report["weak_passwords"] > 0:
            security_score -= 20
        if breach_report.get("breached_passwords"):
            security_score -= 30
        if strength_report["reused_passwords"] > 0:
            security_score -= 15

        return {
            "generated_at": str(datetime.now()),
            "security_score": max(0, security_score),
            "strength_report": strength_report,
            "breach_report": breach_report,
            "recommendations": self._generate_recommendations(
                strength_report, breach_report
            )
        }

    def _generate_recommendations(self, strength_report: Dict, 
                                breach_report: Dict) -> List[str]:
        """
        Güvenlik önerileri oluşturur.
        
        Args:
            strength_report (Dict): Güçlülük raporu
            breach_report (Dict): İhlal raporu
            
        Returns:
            List[str]: Öneriler
        """
        recommendations = []

        # Zayıf parolalar için öneriler
        if strength_report["weak_passwords"] > 0:
            recommendations.append(
                f"{strength_report['weak_passwords']} zayıf parola bulundu. "
                "Bu parolaları güçlü parolalarla değiştirin."
            )

        # İhlal edilmiş parolalar için öneriler
        if breach_report.get("breached_passwords"):
            recommendations.append(
                f"{len(breach_report['breached_passwords'])} parola veri ihlallerinde "
                "açığa çıkmış. Bu parolaları hemen değiştirin."
            )

        # Yeniden kullanılan parolalar için öneriler
        if strength_report["reused_passwords"] > 0:
            recommendations.append(
                f"{strength_report['reused_passwords']} parola birden fazla serviste "
                "kullanılıyor. Her servis için benzersiz parolalar kullanın."
            )

        # Genel öneriler
        if strength_report["total_passwords"] < 10:
            recommendations.append(
                "Parola yöneticinizde çok az parola var. Tüm hesaplarınızı "
                "parola yöneticisine ekleyin."
            )

        return recommendations

    def monitor_continuously(self, interval: int = 3600):
        """
        Sürekli güvenlik izlemesi yapar.
        
        Args:
            interval (int): Kontrol aralığı (saniye)
        """
        while True:
            try:
                report = self.generate_security_report()
                print("\nGüvenlik Raporu:")
                print(f"Güvenlik Puanı: {report['security_score']}/100")
                print("\nÖneriler:")
                for rec in report["recommendations"]:
                    print(f"- {rec}")
                
                time.sleep(interval)
            except KeyboardInterrupt:
                print("\nİzleme durduruldu.")
                break
            except Exception as e:
                print(f"Hata: {e}")
                time.sleep(60)  # Hata durumunda 1 dakika bekle

def main():
    # Test
    manager = PasswordManager("master_password123")
    monitor = SecurityMonitor(manager)
    
    # Örnek parolalar ekle
    manager.add_password("gmail", "user@gmail.com", "password123")
    manager.add_password("github", "user", "password123")  # Yeniden kullanım
    
    # Güvenlik raporu oluştur
    report = monitor.generate_security_report()
    
    print("Güvenlik Raporu:")
    print(f"Güvenlik Puanı: {report['security_score']}/100")
    print("\nÖneriler:")
    for rec in report["recommendations"]:
        print(f"- {rec}")

if __name__ == "__main__":
    main() 