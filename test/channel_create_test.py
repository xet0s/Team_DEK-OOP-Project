import os
import random
from models.database import db
from models.accounts_module.user import User
from models.accounts_module.channel_base import ChannelModel
from controllers.channel_controller import ChannelController

# --- 1. ADIM: TEMİZ BAŞLANGIÇ (DB SIFIRLAMA) ---
# Veritabanı dosyanın adı neyse buraya yaz.
db_file = "DEK.db"  

# Eğer eski dosya varsa sil ki yeni sütunlar (upload_limit) sorunsuzca oluşsun.
if os.path.exists(db_file):
    os.remove(db_file)
    print("🧹 Eski veritabanı temizlendi ve sıfırdan oluşturuluyor...")

# Veritabanı bağlantısı ve tablo kurulumu
db.init(db_file)
db.connect()
db.create_tables([User, ChannelModel])

print("-" * 50)
print("🚀 KANAL OLUŞTURMA TESTİ BAŞLIYOR")
print("-" * 50)

# --- 2. ADIM: KULLANICI OLUŞTURMA ---
# Rastgele sayı üreteci (Benzersiz olması için)
rnd = random.randint(1000, 9999)

# Kanal Sahibi (Owner) Objesini Oluşturuyoruz
# DİKKAT: create_channel fonksiyonuna bu 'owner' değişkenini vereceğiz.
owner, _ = User.get_or_create(
    username=f"TestKullanici_{rnd}", 
    defaults={'email': f"user{rnd}@test.com", 'password_hash': "123456"}
)
print(f"👤 Kullanıcı Hazır: {owner.username} (ID: {owner.id})")


# --- 3. ADIM: CONTROLLER'I BAŞLATMA ---
controller = ChannelController()


# --- SENARYO A: KİŞİSEL KANAL (Limit: 5 Olmalı) ---
print("\n--- [TEST 1] 'Personal' Kanal Açılıyor ---")

sonuc_personal = controller.create_channel(
    channel_owner=owner,            # <--- Objenin kendisi gidiyor (Doğrusu bu)
    channel_name=f"Vlog Kanalım {rnd}",
    channel_category="LifeStyle",
    channel_type="Personal"         # <--- Fabrika buna bakıp Limit: 5 verecek
)
print(sonuc_personal)

# Doğrulama: Veritabanından kontrol edelim
kanal_p = ChannelModel.get(ChannelModel.channel_name == f"Vlog Kanalım {rnd}")
if kanal_p.channel_upload_limit == 5:
    print(">> ✅ DOĞRULAMA BAŞARILI: Veritabanına Limit '5' olarak kaydedilmiş.")
else:
    print(f">> ❌ HATA: Limit yanlış kaydedilmiş! ({kanal_p.channel_upload_limit})")


# --- SENARYO B: MARKA KANALI (Limit: 10000 Olmalı) ---
print("\n--- [TEST 2] 'Brand' Kanal Açılıyor ---")

sonuc_brand = controller.create_channel(
    channel_owner=owner,
    channel_name=f"Holding Resmi Hesap {rnd}",
    channel_category="Business",
    channel_type="Brand"            # <--- Fabrika buna bakıp Limit: 10000 verecek
)
print(sonuc_brand)

# Doğrulama
kanal_b = ChannelModel.get(ChannelModel.channel_name == f"Holding Resmi Hesap {rnd}")
if kanal_b.channel_upload_limit == 10000:
    print(">> ✅ DOĞRULAMA BAŞARILI: Veritabanına Limit '10000' olarak kaydedilmiş.")
else:
    print(f">> ❌ HATA: Limit yanlış kaydedilmiş! ({kanal_b.channel_upload_limit})")

print("\n" + "-" * 50)
print("🏁 TÜM TESTLER TAMAMLANDI")