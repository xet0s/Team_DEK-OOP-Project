import sys
import os

# Mevcut dosyanın yolunu al, bir üst klasöre (parent directory) çık ve onu Python yoluna ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from models.database import db
from models.accounts_module.user import User
from models.accounts_module.channel_base import ChannelModel
from controllers.channel_controller import ChannelController

# 1. Veritabanı Bağlantısı ve Tablolar
db.connect()
db.create_tables([User, ChannelModel])

print("--- 🎬 KANAL OLUŞTURMA TESTİ BAŞLIYOR ---")

# 2. Kanal Sahibi Olacak Kullanıcıyı Seç (Yoksa Oluştur)
user, created = User.get_or_create(
    username="YazilimciGenc",
    defaults={
        'email': "create_test@dek.com",
        'password_hash': "12345"
    }
)
print(f"👤 Kullanıcı Hazır: {user.username}")

# 3. Controller'ı (Müdür) Başlat
controller = ChannelController()

# 4. Kanal Oluşturma Emrini Ver
# Senin fonksiyonundaki parametre isimlerine birebir uyarak gönderiyorum:
sonuc_mesaji = controller.create_channel(
    channel_owner=user,
    channel_name="Python Eğitim Kampı",
    channel_category="Education",
    channel_status="active", 
    channel_type="Personal"  # Burayı 'Brand' veya 'Kid' yapıp limitin değiştiğini görebilirsin
)

print("\n--- 📝 SONUÇ ÇIKTISI ---")
print(sonuc_mesaji)