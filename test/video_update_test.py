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

print("--- 🔄 VİDEO GÜNCELLEME VE YETKİ TESTİ BAŞLIYOR ---")

# Kullanıcılar Oluştur
owner = UserModel.create(username="Sahip", email="sahip@test.com", password_hash="123")
hacker = UserModel.create(username="Hacker", email="hacker@test.com", password_hash="123")

# Kanal ve Video Oluştur, Controller Başlat
channel = ChannelModel.create(
    channel_owner=owner,
    channel_name="Resmi Kanal",
    channel_category="News",
    channel_type="Brand",
    channel_status="active",
    channel_upload_limit=999,
    channel_link="dek.channel/resmi" 
)

controller = VideoController()

print(">> Hazırlık: Video oluşturuluyor...")
res = controller.create_video(
    current_user=owner,
    channel_id=channel.id,
    video_title="Eski Başlık",
    video_description="Eski Açıklama",
    video_duration=100,
    video_type_input="Standard"
)

# Oluşan videonun ID'sini al
video = VideoModel.select().first()
video_id = video.id

print(f"✅ Video Hazır (ID: {video_id}): '{video.title}'")
print("-" * 50)


# Test 1: Yetkisiz Güncelleme Denemesi (Hacker)
print("\n--- [TEST 1] Hacker Başlığı Değiştirmeye Çalışıyor ---")
sonuc1 = controller.update_existing_video(
    video_id=video_id,
    current_user=hacker,
    new_title="HACKLENDİ"
)
print("SONUÇ:", sonuc1)

if "yetkiniz yoktur" in str(sonuc1):
    print("✅ BAŞARILI: Sistem hacker'ı engelledi.")
else:
    print("❌ HATA: Hacker videoyu değiştirebildi!")


# Test 2: Sahip Tarafından Başlık ve Açıklama Güncelleme
print("\n--- [TEST 2] Sahip Başlığı ve Açıklamayı Güncelliyor ---")
sonuc2 = controller.update_existing_video(
    video_id=video_id,
    current_user=owner,
    new_title="Yeni Süper Başlık",
    new_description="Güncel Açıklama"
)
print(sonuc2)

guncel_video = VideoModel.get_by_id(video_id)
if guncel_video.title == "Yeni Süper Başlık":
    print("✅ BAŞARILI: Veritabanında başlık değişti.")
else:
    print(f"❌ HATA: Başlık değişmedi! (Mevcut: {guncel_video.title})")


# Test 3: Sadece Açıklama Değişikliği (Başlık None)
print("\n--- [TEST 3] Sadece Açıklama Değişiyor (Başlık None) ---")
sonuc3 = controller.update_existing_video(
    video_id=video_id,
    current_user=owner,
    new_description="Sadece burası değişti v2"
    # new_title = None
)
print(sonuc3)

final_video = VideoModel.get_by_id(video_id)
if final_video.description == "Sadece burası değişti v2" and final_video.title == "Yeni Süper Başlık":
    print("✅ BAŞARILI: Sadece açıklama değişti, başlık korundu.")
else:
    print("❌ HATA: Kısmi güncelleme çalışmadı.")

print("\n--- TEST BİTTİ ---")