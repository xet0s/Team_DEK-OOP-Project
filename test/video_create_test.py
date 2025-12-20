import sys
import os
from time import sleep

# Proje ana dizinini Python yoluna ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.database import db
from models.accounts_module.user import User
from models.interaction_module.interaction_base import InteractionModel
from models.accounts_module.channel_base import ChannelModel
from models.content_module.video_base import VideoModel
from controllers.video_controller import VideoController

# Veritabanını Hazırla
db.connect()
db.drop_tables([User, ChannelModel, VideoModel, InteractionModel])
db.create_tables([User, ChannelModel, VideoModel, InteractionModel])

print("--- VİDEO OLUŞTURMA TESTİ ---")
print("-" * 50)

# Kullanıcı Oluştur
print(">> Kullanıcı oluşturuluyor...")
user = User.create(
    username="TestYonetmeni", 
    email="director@test.com", 
    password_hash="123",
    role = "Standard"
)
sleep(0.75)

# Kanal Oluştur
print(">> Kanal oluşturuluyor...")
channel = ChannelModel.create(
    channel_owner=user,
    channel_name="Minik Dahiler",
    channel_category="Education",
    channel_type="Kid",
    channel_status="active",
    channel_upload_limit=2,
    channel_link="dek.channel/minikdahiler"
)
print(f"✅ Kanal Hazır: {channel.channel_name} (Limit: {channel.channel_upload_limit})")
sleep(0.75)

# Controller Başlat
video_controller = VideoController()

# Test 1: Standard Video Oluşturma, Link ve Simülasyon Kontrolü
print("\n--- [TEST 1] İlk Video (Standard) ---")
sonuc1 = video_controller.create_video(
    current_user=user,
    channel_id=channel.id,
    video_title="Python Ders 1",
    video_description="Giriş",
    video_duration=120,
    video_type_input="Standard",
    video_category_input="Education"
)
print(sonuc1)
sleep(0.75)

video= VideoModel.select().first()
if "dek.video/v/" in str(sonuc1):
    print(">> BAŞARILI: Video linki oluşturuldu!")
else:
    print(">> HATA: Video linki yok!")
if video.status == "published":
    print(">> BAŞARILI: Video durumu 'published' olarak ayarlandı!")
else:
    print(">> HATA: Video durumu yanlış!")
sleep(0.75)

# Test 2: Livestream Video Oluşturma
print("\n--- [TEST 2] İkinci Video (Livestream) ---")
sonuc2 = video_controller.create_video(
    current_user=user,
    channel_id=channel.id,
    video_title="Canlı Yayın",
    video_description="Test Yayını",
    video_duration=3600,
    video_type_input="LiveStream",
    video_category_input="General"
)
print(sonuc2)
sleep(0.75)

if "dek.video/v/" in str(sonuc2):
    print(">> BAŞARILI: Canlı yayın linki oluşturuldu!")
else:
    print(">> HATA: Canlı yayın linki yok!")
sleep(0.75)

# Test 3: Limit Aşımı Denemesi
print("\n--- [TEST 3] Limit Aşımı Denemesi ---")
sonuc3 = video_controller.create_video(
    current_user=user,
    channel_id=channel.id,
    video_title="Yasaklı Video",
    video_description="Bu yüklenmemeli",
    video_duration=50,
    video_type_input="Short",
    video_category_input="Gaming"
)
print(sonuc3)
sleep(0.75)

if "limit" in str(sonuc3).lower():
    print(">> BAŞARILI: Limit sistemi doğru çalıştı, video engellendi!")
else:
    print(">> HATA: Limit sistemi devreye girmedi!")
sleep(0.75)

print("\n--- TEST BİTTİ ---")