import re
import string
import hashlib
from typing import Dict, List, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

class PasswordStrengthAnalyzer:
    def __init__(self):
        self.common_passwords = self._load_common_passwords()
        self.vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(1, 3))
        self.classifier = RandomForestClassifier(n_estimators=100)
        self._train_classifier()

    def _load_common_passwords(self) -> List[str]:
        """Yaygın parolaları yükler."""
        # Gerçek uygulamada bu liste bir dosyadan yüklenebilir
        return [
            "password", "123456", "qwerty", "admin", "welcome",
            "letmein", "monkey", "dragon", "baseball", "football"
        ]

    def _train_classifier(self):
        """ML modelini eğitir."""
        # Örnek eğitim verileri
        weak_passwords = ["password123", "qwerty", "123456", "admin123"]
        strong_passwords = ["P@ssw0rd!2024", "Xk9#mP2$vL5", "Tr0ub4dor&3", "correct horse battery staple"]
        
        X = self.vectorizer.fit_transform(weak_passwords + strong_passwords)
        y = [0] * len(weak_passwords) + [1] * len(strong_passwords)
        
        self.classifier.fit(X, y)

    def analyze_password(self, password: str) -> Dict:
        """
        Parolanın güçlülüğünü analiz eder.
        
        Args:
            password (str): Analiz edilecek parola
            
        Returns:
            Dict: Analiz sonuçları
        """
        if not password:
            return {"error": "Parola boş olamaz"}

        results = {
            "length": len(password),
            "has_uppercase": bool(re.search(r'[A-Z]', password)),
            "has_lowercase": bool(re.search(r'[a-z]', password)),
            "has_digit": bool(re.search(r'\d', password)),
            "has_special": bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password)),
            "is_common": password.lower() in self.common_passwords,
            "entropy": self._calculate_entropy(password),
            "ml_score": self._get_ml_score(password),
            "strength_score": 0,
            "recommendations": []
        }

        # Güçlülük puanı hesaplama
        results["strength_score"] = self._calculate_strength_score(results)
        
        # Öneriler oluşturma
        results["recommendations"] = self._generate_recommendations(results)

        return results

    def _calculate_entropy(self, password: str) -> float:
        """Parolanın entropisini hesaplar."""
        if not password:
            return 0

        # Karakter seti boyutunu belirle
        charset_size = 0
        if any(c in string.ascii_lowercase for c in password):
            charset_size += 26
        if any(c in string.ascii_uppercase for c in password):
            charset_size += 26
        if any(c in string.digits for c in password):
            charset_size += 10
        if any(c in string.punctuation for c in password):
            charset_size += 32

        # Entropi hesaplama
        entropy = len(password) * np.log2(charset_size)
        return entropy

    def _get_ml_score(self, password: str) -> float:
        """ML modeli kullanarak parola güçlülük puanı hesaplar."""
        X = self.vectorizer.transform([password])
        return float(self.classifier.predict_proba(X)[0][1])

    def _calculate_strength_score(self, results: Dict) -> int:
        """Parola güçlülük puanını hesaplar (0-100 arası)."""
        score = 0
        
        # Uzunluk puanı (maksimum 40 puan)
        length_score = min(results["length"] * 2, 40)
        score += length_score
        
        # Karakter çeşitliliği puanı (maksimum 30 puan)
        if results["has_uppercase"]: score += 7.5
        if results["has_lowercase"]: score += 7.5
        if results["has_digit"]: score += 7.5
        if results["has_special"]: score += 7.5
        
        # Entropi puanı (maksimum 20 puan)
        entropy_score = min(results["entropy"] / 2, 20)
        score += entropy_score
        
        # ML puanı (maksimum 10 puan)
        ml_score = results["ml_score"] * 10
        score += ml_score
        
        # Yaygın parola cezası
        if results["is_common"]:
            score = max(0, score - 30)
        
        return min(100, int(score))

    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Parola güçlendirme önerileri oluşturur."""
        recommendations = []
        
        if results["length"] < 12:
            recommendations.append("Parolanızı en az 12 karakter uzunluğunda yapın")
        
        if not results["has_uppercase"]:
            recommendations.append("Büyük harfler ekleyin")
        
        if not results["has_lowercase"]:
            recommendations.append("Küçük harfler ekleyin")
        
        if not results["has_digit"]:
            recommendations.append("Rakamlar ekleyin")
        
        if not results["has_special"]:
            recommendations.append("Özel karakterler ekleyin (!@#$%^&*(),.?\":{}|<>)")
        
        if results["is_common"]:
            recommendations.append("Yaygın parolalardan kaçının")
        
        if results["entropy"] < 50:
            recommendations.append("Daha rastgele ve tahmin edilmesi zor bir parola seçin")
        
        return recommendations

def main():
    analyzer = PasswordStrengthAnalyzer()
    
    # Test parolaları
    test_passwords = [
        "password123",
        "P@ssw0rd!2024",
        "123456",
        "correct horse battery staple",
        "qwerty123"
    ]
    
    for password in test_passwords:
        print(f"\nParola: {password}")
        results = analyzer.analyze_password(password)
        print(f"Güçlülük Puanı: {results['strength_score']}/100")
        print("Öneriler:")
        for rec in results["recommendations"]:
            print(f"- {rec}")

if __name__ == "__main__":
    main() 