import sys
import os

# Mevcut dosyanın yolunu al, bir üst klasöre (parent directory) çık ve onu Python yoluna ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import random
from models.database import db
from models.accounts_module.user import User
from models.accounts_module.channel_base import ChannelModel
from controllers.channel_controller import ChannelController

# 1. Veritabanı Bağlantısı
db.connect()
db.create_tables([User, ChannelModel])

print("--- 🛡️ GELİŞMİŞ GÜNCELLEME TESTİ (Benzersiz Verilerle) ---")

# --- RASTGELE SAYI ÜRETECİ ---
# Her testte farklı sayı üretir (Örn: 5491).
# Böylece "test@test.com" hatası asla almazsın.
rastgele_sayi = random.randint(1000, 99999) 

# 2. Kullanıcıları Oluştur (Benzersiz İsimlerle)
# Kanal Sahibi
owner_username = f"Sahip_{rastgele_sayi}"
owner_email = f"sahip_{rastgele_sayi}@test.com"

owner, _ = User.get_or_create(
    username=owner_username, 
    defaults={'email': owner_email, 'password_hash': "123"}
)
print(f"✅ Kanal Sahibi Oluşturuldu: {owner.username} ({owner.email})")

# Kötü Niyetli Kullanıcı
hacker_username = f"Hacker_{rastgele_sayi}"
hacker_email = f"hacker_{rastgele_sayi}@test.com"

hacker, _ = User.get_or_create(
    username=hacker_username, 
    defaults={'email': hacker_email, 'password_hash': "123"}
)
print(f"✅ Hacker Kullanıcısı Oluşturuldu: {hacker.username} ({hacker.email})")


# 3. Controller Başlat ve Kanal Kur
controller = ChannelController()

kanal_ismi = f"Oyun Kanalı {rastgele_sayi}" # Kanal ismi de benzersiz olsun

controller.create_channel(
    channel_owner=owner,
    channel_name=kanal_ismi,
    channel_category="Gaming",
    channel_type="Personal"
)

# Kanalı ID ile çekelim (En son eklenen)
channel = ChannelModel.select().order_by(ChannelModel.id.desc()).get()
print(f"✅ Test Kanalı Hazır: '{channel.channel_name}' (ID: {channel.id})")
print("-" * 60)


# --- SENARYO 1: SAHİBİ İSİM DEĞİŞTİRİYOR (Başarılı Olmalı) ---
yeni_isim = f"Süper Oyunlar {rastgele_sayi} v2"
print(f"\n[TEST 1] {owner.username} ismini '{yeni_isim}' yapıyor...")

sonuc1 = controller.update_existing_channel(
    channel_id=channel.id, 
    current_user=owner, 
    updated_channel_name=yeni_isim
)
print(f"SONUÇ: {sonuc1}")

# Veritabanı Kontrolü
guncel_kanal = ChannelModel.get_by_id(channel.id)
if guncel_kanal.channel_name == yeni_isim:
    print(">> DOĞRULAMA: Veritabanında isim başarıyla değişti! ✅")
else:
    print(">> DOĞRULAMA: HATA! İsim değişmedi. ❌")


# --- SENARYO 2: HACKER DEĞİŞTİRMEYE ÇALIŞIYOR (Hata Vermeli) ---
print(f"\n[TEST 2] {hacker.username} kanalı ele geçirmeye çalışıyor...")

sonuc2 = controller.update_existing_channel(
    channel_id=channel.id, 
    current_user=hacker, 
    updated_channel_name="HACKED BY HACKER"
)
print(f"SONUÇ: {sonuc2}")


# --- SENARYO 3: BOŞ VERİ (Uyarı Vermeli) ---
print("\n[TEST 3] Değişiklik yapmadan güncelleme isteği gönderiliyor...")

sonuc3 = controller.update_existing_channel(
    channel_id=channel.id, 
    current_user=owner
    # İsim veya durum yollamadık (None)
)
print(f"SONUÇ: {sonuc3}")

print("\n--- TEST BAŞARIYLA TAMAMLANDI ---")