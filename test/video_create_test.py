import sys
import os

# Proje ana dizinini Python yoluna ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.database import db
from models.accounts_module.user import User
from models.accounts_module.channel_base import ChannelModel
from models.content_module.video_base import VideoModel
from controllers.video_controller import VideoController

# Veritabanını Hazırla
db.connect()
db.create_tables([User, ChannelModel, VideoModel])

print("--- 🎬 VİDEO OLUŞTURMA, LİNK VE LİMİT TESTİ BAŞLIYOR ---")

# Kullanıcı Oluştur
user = User.create(
    username="TestYonetmeni", 
    email="director@test.com", 
    password_hash="123"
)

# Kanal Oluştur
print(">> Kanal oluşturuluyor...")
channel = ChannelModel.create(
    channel_owner=user,
    channel_name="Minik Dahiler",
    channel_category="Education",
    channel_type="Kid",
    channel_status="active",
    channel_upload_limit=2,
)
print(f"✅ Kanal Hazır: {channel.channel_name} (Limit: {channel.channel_upload_limit})")


# Controller Başlat
video_controller = VideoController()

# Test 1: Standard Video Oluşturma ve Link Kontrolü
print("\n--- [TEST 1] İlk Video (Standard) ---")
sonuc1 = video_controller.create_video(
    current_user=user,
    channel_id=channel.id,
    video_title="Python Ders 1",
    video_description="Giriş",
    video_duration=120,
    video_type_input="Standard"
)
print(sonuc1)

if "dek.video/v/" in str(sonuc1):
    print(">> ✅ BAŞARILI: Video linki oluşturuldu!")
else:
    print(">> ❌ HATA: Video linki yok!")

# Test 2: Livestream Video Oluşturma
print("\n--- [TEST 2] İkinci Video (LiveStream) ---")
sonuc2 = video_controller.create_video(
    current_user=user,
    channel_id=channel.id,
    video_title="Canlı Yayın",
    video_description="Test Yayını",
    video_duration=3600,
    video_type_input="LiveStream"
)
print(sonuc2)

# Test 3: Limit Aşımı Denemesi
print("\n--- [TEST 3] Limit Aşımı Denemesi ---")
sonuc3 = video_controller.create_video(
    current_user=user,
    channel_id=channel.id,
    video_title="Yasaklı Video",
    video_description="Bu yüklenmemeli",
    video_duration=50,
    video_type_input="Short"
)

print(sonuc3)

if "Yükleme limiti aşıldı" in str(sonuc3):
    print(">> ✅ BAŞARILI: Limit sistemi doğru çalıştı, video engellendi!")
else:
    print(">> ❌ HATA: Limit sistemi devreye girmedi!")

print("\n--- TEST BİTTİ ---")