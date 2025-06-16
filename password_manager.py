import json
import base64
import os
from typing import Dict, List, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from password_strength import PasswordStrengthAnalyzer
from password_generator import PasswordGenerator

class PasswordManager:
    def __init__(self, master_password: str, storage_file: str = "passwords.json"):
        """
        Parola yöneticisini başlatır.
        
        Args:
            master_password (str): Ana parola
            storage_file (str): Parolaların saklanacağı dosya
        """
        self.storage_file = storage_file
        self.analyzer = PasswordStrengthAnalyzer()
        self.generator = PasswordGenerator()
        self.key = self._derive_key(master_password)
        self.fernet = Fernet(self.key)
        self.passwords = self._load_passwords()

    def _derive_key(self, master_password: str) -> bytes:
        """Ana paroladan şifreleme anahtarı türetir."""
        salt = b'password_manager_salt'  # Gerçek uygulamada rastgele ve güvenli bir salt kullanılmalı
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        return key

    def _load_passwords(self) -> Dict:
        """Şifrelenmiş parolaları yükler."""
        if not os.path.exists(self.storage_file):
            return {}
        
        try:
            with open(self.storage_file, 'r') as f:
                encrypted_data = f.read()
                if not encrypted_data:
                    return {}
                decrypted_data = self.fernet.decrypt(encrypted_data.encode())
                return json.loads(decrypted_data)
        except Exception as e:
            print(f"Parola yükleme hatası: {e}")
            return {}

    def _save_passwords(self):
        """Parolaları şifreleyerek kaydeder."""
        try:
            encrypted_data = self.fernet.encrypt(json.dumps(self.passwords).encode())
            with open(self.storage_file, 'w') as f:
                f.write(encrypted_data.decode())
        except Exception as e:
            print(f"Parola kaydetme hatası: {e}")

    def add_password(self, service: str, username: str, password: str, 
                    notes: str = "", tags: List[str] = None) -> bool:
        """
        Yeni bir parola ekler.
        
        Args:
            service (str): Servis adı
            username (str): Kullanıcı adı
            password (str): Parola
            notes (str): Notlar
            tags (List[str]): Etiketler
            
        Returns:
            bool: İşlem başarılı mı
        """
        # Parola güçlülüğünü kontrol et
        strength = self.analyzer.analyze_password(password)
        if strength["strength_score"] < 60:
            print("Uyarı: Parola çok zayıf!")
            return False

        if service not in self.passwords:
            self.passwords[service] = []

        # Parola geçmişini kontrol et
        for entry in self.passwords[service]:
            if entry["username"] == username and entry["password"] == password:
                print("Uyarı: Bu parola zaten kullanılıyor!")
                return False

        self.passwords[service].append({
            "username": username,
            "password": password,
            "notes": notes,
            "tags": tags or [],
            "created_at": str(datetime.now())
        })

        self._save_passwords()
        return True

    def get_password(self, service: str, username: str) -> Optional[Dict]:
        """
        Belirli bir servis ve kullanıcı adı için parolayı getirir.
        
        Args:
            service (str): Servis adı
            username (str): Kullanıcı adı
            
        Returns:
            Optional[Dict]: Parola bilgileri
        """
        if service not in self.passwords:
            return None

        for entry in self.passwords[service]:
            if entry["username"] == username:
                return entry

        return None

    def update_password(self, service: str, username: str, 
                       new_password: str, notes: str = None) -> bool:
        """
        Mevcut bir parolayı günceller.
        
        Args:
            service (str): Servis adı
            username (str): Kullanıcı adı
            new_password (str): Yeni parola
            notes (str): Yeni notlar
            
        Returns:
            bool: İşlem başarılı mı
        """
        if service not in self.passwords:
            return False

        for entry in self.passwords[service]:
            if entry["username"] == username:
                # Yeni parolanın güçlülüğünü kontrol et
                strength = self.analyzer.analyze_password(new_password)
                if strength["strength_score"] < 60:
                    print("Uyarı: Yeni parola çok zayıf!")
                    return False

                # Eski parolayı geçmişe ekle
                if "password_history" not in entry:
                    entry["password_history"] = []
                entry["password_history"].append({
                    "password": entry["password"],
                    "changed_at": entry.get("updated_at", entry["created_at"])
                })

                # Parolayı güncelle
                entry["password"] = new_password
                if notes is not None:
                    entry["notes"] = notes
                entry["updated_at"] = str(datetime.now())

                self._save_passwords()
                return True

        return False

    def delete_password(self, service: str, username: str) -> bool:
        """
        Bir parolayı siler.
        
        Args:
            service (str): Servis adı
            username (str): Kullanıcı adı
            
        Returns:
            bool: İşlem başarılı mı
        """
        if service not in self.passwords:
            return False

        for i, entry in enumerate(self.passwords[service]):
            if entry["username"] == username:
                del self.passwords[service][i]
                if not self.passwords[service]:
                    del self.passwords[service]
                self._save_passwords()
                return True

        return False

    def generate_and_add_password(self, service: str, username: str,
                                length: int = 16, use_passphrase: bool = False) -> Optional[str]:
        """
        Yeni bir parola oluşturur ve ekler.
        
        Args:
            service (str): Servis adı
            username (str): Kullanıcı adı
            length (int): Parola uzunluğu
            use_passphrase (bool): Geçiş cümlesi kullanılsın mı
            
        Returns:
            Optional[str]: Oluşturulan parola
        """
        if use_passphrase:
            password = self.generator.generate_passphrase()
        else:
            password = self.generator.generate_random_password(length)

        if self.add_password(service, username, password):
            return password
        return None

    def search_passwords(self, query: str) -> List[Dict]:
        """
        Parolaları arar.
        
        Args:
            query (str): Arama sorgusu
            
        Returns:
            List[Dict]: Bulunan parolalar
        """
        results = []
        query = query.lower()

        for service, entries in self.passwords.items():
            for entry in entries:
                if (query in service.lower() or
                    query in entry["username"].lower() or
                    query in entry.get("notes", "").lower() or
                    any(query in tag.lower() for tag in entry.get("tags", []))):
                    results.append({
                        "service": service,
                        **entry
                    })

        return results

    def get_password_strength_report(self) -> Dict:
        """
        Tüm parolaların güçlülük raporunu oluşturur.
        
        Returns:
            Dict: Güçlülük raporu
        """
        report = {
            "total_passwords": 0,
            "weak_passwords": 0,
            "medium_passwords": 0,
            "strong_passwords": 0,
            "reused_passwords": 0,
            "weak_services": []
        }

        all_passwords = set()
        for service, entries in self.passwords.items():
            has_weak_password = False
            for entry in entries:
                report["total_passwords"] += 1
                strength = self.analyzer.analyze_password(entry["password"])
                
                if strength["strength_score"] < 60:
                    report["weak_passwords"] += 1
                    has_weak_password = True
                elif strength["strength_score"] < 80:
                    report["medium_passwords"] += 1
                else:
                    report["strong_passwords"] += 1

                if entry["password"] in all_passwords:
                    report["reused_passwords"] += 1
                all_passwords.add(entry["password"])

            if has_weak_password:
                report["weak_services"].append(service)

        return report

def main():
    # Test
    manager = PasswordManager("master_password123")
    
    # Parola ekle
    manager.add_password("gmail", "user@gmail.com", "StrongP@ssw0rd123")
    
    # Parola oluştur ve ekle
    new_password = manager.generate_and_add_password("github", "user")
    print(f"Oluşturulan parola: {new_password}")
    
    # Parola ara
    results = manager.search_passwords("gmail")
    print("\nArama sonuçları:")
    for result in results:
        print(f"Servis: {result['service']}")
        print(f"Kullanıcı adı: {result['username']}")
        print(f"Parola: {result['password']}")
    
    # Güçlülük raporu
    report = manager.get_password_strength_report()
    print("\nGüçlülük raporu:")
    print(f"Toplam parola: {report['total_passwords']}")
    print(f"Zayıf parolalar: {report['weak_passwords']}")
    print(f"Orta güçlü parolalar: {report['medium_passwords']}")
    print(f"Güçlü parolalar: {report['strong_passwords']}")
    print(f"Yeniden kullanılan parolalar: {report['reused_passwords']}")
    print(f"Zayıf parolaları olan servisler: {report['weak_services']}")

if __name__ == "__main__":
    main() 