import sys
import os

# Mevcut dosyanın yolunu al, bir üst klasöre (parent directory) çık ve onu Python yoluna ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.database import db
from models.accounts_module.user import User
from models.accounts_module.channel_base import ChannelModel
from controllers.channel_controller import ChannelController

# 1. Veritabanı Hazırlığı
db.connect()
db.create_tables([User, ChannelModel])

print("--- 🛡️ GÜVENLİ SİLME TESTİ BAŞLIYOR ---")

# 2. İki Farklı Kullanıcı Oluşturalım (Biri Sahip, Biri Hırsız)
owner_user, _ = User.get_or_create(
    username="KanalSahibi", 
    defaults={'email': "owner@test.com", 'password_hash': "123"}
)

hacker_user, _ = User.get_or_create(
    username="Hacker", 
    defaults={'email': "hacker@test.com", 'password_hash': "123"}
)

# 3. Controller'ı Başlat
controller = ChannelController()

# 4. Test İçin Bir Kanal Oluşturalım
# Not: create_channel string döndüğü için ID'yi veritabanından çekeceğiz
controller.create_channel(
    channel_owner=owner_user,
    channel_name="Silinecek Kanal",
    channel_category="Test",
    channel_type="Personal"
)

# Oluşan kanalın ID'sini bulalım (Test için gerekli)
test_channel = ChannelModel.get(ChannelModel.channel_name == "Silinecek Kanal")
channel_id = test_channel.id
print(f"✅ Test Kanalı Oluşturuldu. ID: {channel_id}, Sahibi: {owner_user.username}")
print("-" * 50)

# --- SENARYO 1: YETKİSİZ SİLME DENEMESİ ---
print(f"\nTEST 1: {hacker_user.username} (Hacker) kanalı silmeye çalışıyor...")
sonuc1 = controller.delete_existing_channel(channel_id, hacker_user)
print("SONUÇ:", sonuc1) 
# Beklenen: "Yetkiye sahip değilsiniz"

# --- SENARYO 2: YETKİLİ SİLME DENEMESİ ---
print(f"\nTEST 2: {owner_user.username} (Sahip) kanalı silmeye çalışıyor...")
sonuc2 = controller.delete_existing_channel(channel_id, owner_user)
print("SONUÇ:", sonuc2)
# Beklenen: "Başarıyla silindi"

# --- SENARYO 3: OLMAYAN KANALI SİLME ---
print(f"\nTEST 3: Aynı kanalı tekrar silmeye çalışıyoruz (Artık yok)...")
sonuc3 = controller.delete_existing_channel(channel_id, owner_user)
print("SONUÇ:", sonuc3)
# Beklenen: "Böyle bir kanal bulunmamakta"