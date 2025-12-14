
import sys
import os
import random

# Proje ana dizinini yola ekleyelim ki import hatası almayalım
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.database import db
from models.accounts_module.user import User
from models.accounts_module.channel_base import ChannelModel
from controllers.channel_controller import ChannelController

# Veritabanını başlat ve tabloları oluştur
db.connect()
db.create_tables([User, ChannelModel])
print("🛠️ Tablolar (User, ChannelModel) yeniden oluşturuldu.\n")

# --- 2. ADIM: KULLANICI OLUŞTURMA ---
rnd = random.randint(1000, 9999) # Benzersizlik için rastgele sayı
owner_username = f"TestUser_{rnd}"
owner_email = f"user_{rnd}@test.com"

# Kullanıcıyı veritabanına kaydediyoruz
# create() metodu direkt objeyi döner.
owner = User.create(
    username=owner_username, 
    email=owner_email, 
    password_hash="secret123"
)
print(f"👤 Kanal Sahibi Oluşturuldu: {owner.username} (ID: {owner.id})")
print("-" * 50)


# --- 3. ADIM: KANAL OLUŞTURMA TESTLERİ ---
controller = ChannelController()

# --- SENARYO A: PERSONAL KANAL (Limit 5 Olmalı) ---
print("\n[TEST 1] 'Personal' Kanal Açılıyor...")
c_name_personal = f"Günlük Vlog {rnd}"

result_personal = controller.create_channel(
    channel_owner=owner,          # DİKKAT: User objesinin kendisini gönderiyoruz!
    channel_name=c_name_personal,
    channel_category="LifeStyle",
    channel_type="Personal"       # Factory buna bakıp limit=5 verecek
)
print(f"Dönüş Mesajı: {result_personal}")

# Veritabanı Kontrolü
saved_p = ChannelModel.get(ChannelModel.channel_name == c_name_personal)
if saved_p.channel_upload_limit == 5:
    print("✅ BAŞARILI: Personal kanal limiti '5' olarak kaydedilmiş.")
else:
    print(f"❌ HATA: Limit yanlış! Beklenen: 5, Gelen: {saved_p.channel_upload_limit}")


# --- SENARYO B: BRAND KANAL (Limit 10000 Olmalı) ---
print("\n[TEST 2] 'Brand' (Marka) Kanal Açılıyor...")
c_name_brand = f"Tech Holding {rnd}"

result_brand = controller.create_channel(
    channel_owner=owner,
    channel_name=c_name_brand,
    channel_category="Business",
    channel_type="Brand"          # Factory buna bakıp limit=10000 verecek
)
print(f"Dönüş Mesajı: {result_brand}")

# Veritabanı Kontrolü
saved_b = ChannelModel.get(ChannelModel.channel_name == c_name_brand)
if saved_b.channel_upload_limit == 10000:
    print("✅ BAŞARILI: Brand kanal limiti '10000' olarak kaydedilmiş.")
else:
    print(f"❌ HATA: Limit yanlış! Beklenen: 10000, Gelen: {saved_b.channel_upload_limit}")

print("\n" + "="*30)
print("🏁 TESTLER TAMAMLANDI")