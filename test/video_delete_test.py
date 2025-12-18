import sys
import os

# Proje ana dizinini Python yoluna ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.database import db
from models.accounts_module.user_base import UserModel
from models.accounts_module.channel_base import ChannelModel
from models.content_module.video_base import VideoModel
from controllers.video_controller import VideoController

# Veritabanını Hazırla
db.connect()
db.create_tables([UserModel, ChannelModel, VideoModel])

print("--- 🗑️ VİDEO SİLME VE GÜVENLİK TESTİ BAŞLIYOR ---")

# Kullanıcıları ve Videoları Oluştur, Controlleri Başlat
owner = UserModel.create(username="Sahip", email="sahip@test.com", password_hash="123")
hacker = UserModel.create(username="Hacker", email="hacker@test.com", password_hash="123")

channel = ChannelModel.create(
    channel_owner=owner,
    channel_name="Oyun Kanalı",
    channel_category="Gaming",
    channel_type="Personal",
    channel_status="active",
    channel_upload_limit=10,
    channel_link="dek.channel/oyun"
)

controller = VideoController()

print(">> Hazırlık: Video oluşturuluyor...")
controller.create_video(
    current_user=owner,
    channel_id=channel.id,
    video_title="Silinecek Video",
    video_description="Elveda dünya",
    video_duration=300,
    video_type_input="Standard"
)

# Oluşturulan videonun ID'sini al
video = VideoModel.select().first()
video_id = video.id
print(f"✅ Video Hazır (ID: {video_id}): '{video.title}'")
print("-" * 50)


# Test 1: Yetkisiz Silme Denemesi (Hacker)
print("\n--- [TEST 1] Hacker Silmeye Çalışıyor ---")
sonuc1 = controller.delete_existing_video(
    video_id=video_id,
    current_user=hacker 
)
print("SONUÇ:", sonuc1)

check_video = VideoModel.get_or_none(VideoModel.id == video_id)
if "yetkiniz yoktur" in str(sonuc1) and check_video is not None:
    print("✅ BAŞARILI: Sistem hacker'ı engelledi, video hala duruyor.")
else:
    print("❌ HATA: Hacker videoyu sildi veya mesaj yanlış!")

# Test 2: Sahip Silme Denemesi
print("\n--- [TEST 2] Sahip Silmeye Çalışıyor ---")
sonuc2 = controller.delete_existing_video(
    video_id=video_id,
    current_user=owner 
)
print("SONUÇ:", sonuc2)

deleted_video = VideoModel.get_or_none(VideoModel.id == video_id)
if deleted_video is None:
    print("✅ BAŞARILI: Video veritabanından tamamen silindi.")
else:
    print("❌ HATA: Video hala veritabanında duruyor!")

# Test 3: Aynı Videoyu Tekrar Silme Denemesi
print("\n--- [TEST 3] Aynı Videoyu Tekrar Silme Denemesi ---")
sonuc3 = controller.delete_existing_video(
    video_id=video_id, 
    current_user=owner
)
print("SONUÇ:", sonuc3)

if "bulunmamakta" in str(sonuc3):
    print("✅ BAŞARILI: Sistem olmayan videoyu yönetti.")
else:
    print("❌ HATA: Beklenmedik bir cevap döndü.")

print("\n--- TEST BİTTİ ---")