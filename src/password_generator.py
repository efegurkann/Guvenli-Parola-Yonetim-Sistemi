import random
import string
import secrets
from typing import List, Optional
from password_strength import PasswordStrengthAnalyzer

class PasswordGenerator:
    def __init__(self):
        self.analyzer = PasswordStrengthAnalyzer()
        self.word_list = self._load_word_list()

    def _load_word_list(self) -> List[str]:
        """Geçiş cümlesi oluşturmak için kelime listesi yükler."""
        # Gerçek uygulamada bu liste bir dosyadan yüklenebilir
        return [
            "correct", "horse", "battery", "staple", "elephant", "giraffe",
            "penguin", "dolphin", "tiger", "lion", "zebra", "monkey",
            "panda", "koala", "kangaroo", "rhino", "hippo", "gazelle"
        ]

    def generate_random_password(self, length: int = 16, 
                               use_uppercase: bool = True,
                               use_lowercase: bool = True,
                               use_digits: bool = True,
                               use_special: bool = True) -> str:
        """
        Rastgele bir parola oluşturur.
        
        Args:
            length (int): Parola uzunluğu
            use_uppercase (bool): Büyük harf kullanımı
            use_lowercase (bool): Küçük harf kullanımı
            use_digits (bool): Rakam kullanımı
            use_special (bool): Özel karakter kullanımı
            
        Returns:
            str: Oluşturulan parola
        """
        # Karakter setini oluştur
        chars = ""
        if use_uppercase:
            chars += string.ascii_uppercase
        if use_lowercase:
            chars += string.ascii_lowercase
        if use_digits:
            chars += string.digits
        if use_special:
            chars += string.punctuation

        if not chars:
            raise ValueError("En az bir karakter seti seçilmelidir")

        # Parolayı oluştur
        while True:
            password = ''.join(secrets.choice(chars) for _ in range(length))
            # Parolanın güçlülüğünü kontrol et
            if self.analyzer.analyze_password(password)["strength_score"] >= 80:
                return password

    def generate_passphrase(self, word_count: int = 4, 
                          separator: str = " ",
                          capitalize: bool = True,
                          add_number: bool = True,
                          add_special: bool = True) -> str:
        """
        Geçiş cümlesi (passphrase) oluşturur.
        
        Args:
            word_count (int): Kelime sayısı
            separator (str): Kelimeler arası ayraç
            capitalize (bool): Kelimeleri büyük harfle başlatma
            add_number (bool): Sayı ekleme
            add_special (bool): Özel karakter ekleme
            
        Returns:
            str: Oluşturulan geçiş cümlesi
        """
        # Kelimeleri seç
        words = random.sample(self.word_list, word_count)
        
        # Kelimeleri büyük harfle başlat
        if capitalize:
            words = [word.capitalize() for word in words]
        
        # Geçiş cümlesini oluştur
        passphrase = separator.join(words)
        
        # Sayı ekle
        if add_number:
            passphrase += str(random.randint(0, 9999))
        
        # Özel karakter ekle
        if add_special:
            passphrase += random.choice(string.punctuation)
        
        return passphrase

    def generate_pronounceable_password(self, length: int = 12) -> str:
        """
        Telaffuz edilebilir bir parola oluşturur.
        
        Args:
            length (int): Parola uzunluğu
            
        Returns:
            str: Oluşturulan parola
        """
        vowels = "aeiou"
        consonants = "bcdfghjklmnpqrstvwxyz"
        
        password = ""
        while len(password) < length:
            if len(password) % 2 == 0:
                password += random.choice(consonants)
            else:
                password += random.choice(vowels)
        
        # Rastgele bir sayı ve özel karakter ekle
        password += str(random.randint(0, 999))
        password += random.choice(string.punctuation)
        
        return password

def main():
    generator = PasswordGenerator()
    
    print("1. Rastgele Parola:")
    password = generator.generate_random_password()
    print(f"Parola: {password}")
    print(f"Güçlülük Puanı: {generator.analyzer.analyze_password(password)['strength_score']}/100")
    
    print("\n2. Geçiş Cümlesi:")
    passphrase = generator.generate_passphrase()
    print(f"Geçiş Cümlesi: {passphrase}")
    print(f"Güçlülük Puanı: {generator.analyzer.analyze_password(passphrase)['strength_score']}/100")
    
    print("\n3. Telaffuz Edilebilir Parola:")
    pronounceable = generator.generate_pronounceable_password()
    print(f"Parola: {pronounceable}")
    print(f"Güçlülük Puanı: {generator.analyzer.analyze_password(pronounceable)['strength_score']}/100")

if __name__ == "__main__":
    main() 